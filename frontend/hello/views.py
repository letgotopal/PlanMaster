from django.views.generic import TemplateView
from .forms import UploadFileForm
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from django.http import HttpResponse
from django.conf import settings
from django.utils import timezone
import json
from . import models
import os
import sys
sys.path.append("..")
from backend.manifest import Manifest
from backend.ship import Ship
from backend import luAlg, trace, balancingAlg, manifest, loadAlg
from .models import InstructionList, Instruction
    

class SharedData:
    upload_path = None

class HomePageView(View):
    template_name = "homepage.html"

    def get(self, request, *args, **kwargs):
        form = UploadFileForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        if 'file' in request.FILES:
            return self.handle_file_upload(request)
        elif 'SignIn' in request.POST:
            return self.handle_sign_in(request)

        return render(request, self.template_name, {'form': UploadFileForm()})

    def handle_file_upload(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            
            # Process the uploaded file as needed
            # For example, save the file to a specific location
            os.makedirs('ManifestUploads',exist_ok=True)
            upload_path = os.path.join('ManifestUploads', uploaded_file.name)
            with open('ManifestUploads/' + uploaded_file.name, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)

            if not request.session.session_key:
                request.session.create()

            # parse and process file
            m = manifest.Manifest()
            ship = m.read_manifest('ManifestUploads/' + uploaded_file.name)
            ship_grid = models.ShipGrid.objects.create()
            ship_grid.read_bay(ship)
            ship_grid.save()
            request.session['lu_before_id'] = ship_grid.pk

            SharedData.upload_path = upload_path

            # Render the template with a success message and uploaded file name
            return render(request, self.template_name, {'form': form, 'upload_success': True, 'uploaded_file_name': uploaded_file.name})
        return render(request, self.template_name, {'form': form})

    def handle_sign_in(self, request):
        sign_in_name = request.POST.get('SignIn', '')
        if sign_in_name:
            file_path = os.path.join('LogInFile', 'LogIn.txt')
           # file_path = '/Users/mohamed/Desktop/PlanMaster/frontend/LogInFile/LogIn.txt'
            los_angeles_time = datetime.now()
            timestamp = los_angeles_time.strftime("%m-%d-%Y %H:%M:%S")
            with open(file_path, 'a') as file:
                file.write(f'{sign_in_name} - {timestamp}\n')

        return render(request, self.template_name, {'sign_in_name': sign_in_name})
    

class LogPageView(TemplateView):
    template_name = "logdownloadpage.html"

class ManagePageView(TemplateView):
    template_name = "managepage.html"

class GridPageView(TemplateView):
    template_name = "gridpage.html"

    def get(self,request):

        grid_data = models.ShipGrid.objects.get(pk=request.session['lu_before_id'])
        grid_rows = grid_data.shiprow_set.all()

        # set status of grid cells and descriptions
        # 1 for occupied, 0 for empty, -1 for n/a
        status = [[0]*grid_rows[0].shipcell_set.all().count() for _ in range(grid_rows.count())]
        grid_descr = [[None]*grid_rows[0].shipcell_set.all().count() for _ in range(grid_rows.count())]
        for i in range(grid_rows.count()):
            row_cells = grid_rows[i].shipcell_set.all()
            for j in range(row_cells.count()):
                if row_cells[j].description == 'NAN':
                    status[i][j] = -1
                elif row_cells[j].description == 'UNUSED':
                    status[i][j] = 0
                else:
                    status[i][j] = 1
                    grid_descr[i][j] = row_cells[j].description[:5]

        context={
            'status':status,
            'grid_data':grid_data,
            'grid_descr':json.dumps(grid_descr)
        }

        return render(request,self.template_name,context)
    
    def post(self,request):
        unload_r = json.loads(request.POST.get('unload_r'))
        unload_c = json.loads(request.POST.get('unload_c'))
        load_list = [(int(e[0]),e[1]) for e in json.loads(request.POST.get('load_list'))]
        
        print(unload_r,unload_c)
        print(load_list)

        grid_data = models.ShipGrid.objects.get(pk=request.session['lu_before_id'])

        # convert model to ship and run ucs
        in_ship = grid_data.to_ship()
        out_ship = luAlg.ucs(in_ship,[(unload_r[i],unload_c[i]) for i in range(len(unload_r))])
        out_ship_load = loadAlg.load(out_ship,load_list)

        # save out ship model for manifest access (maybe can be skipped
        # if we write manifest immediately)
        out_grid = models.ShipGrid.objects.create()
        out_grid.read_bay(out_ship_load)
        out_grid.save()
        request.session['lu_after_id'] = out_grid.pk

        # write outbound manifest
        test_filename = SharedData.upload_path
        if SharedData.upload_path is None:
            return redirect('homepage')
        outbound_manifest = Manifest.write_manifest(self,out_ship_load,test_filename)

        # generate trace to goal ship
        instructs = models.InstructionList.objects.create()
        instructs.read_trace(trace.trace(out_ship_load))
        instructs.save()
        request.session['lu_instructs_id'] = instructs.pk

        print(request.session['lu_instructs_id'])

        # NOTE: Access the stored instruction list by calling
        # models.InstructionList.objects.get(pk=request.session['lu_instructs_id'])
        # Instruction objects can be referenced by
        # instruction_list.instruction_set.all()[index]

        return render(request, self.template_name)
    
def download_txt(request):
    file_path = os.path.join('LogInFile', 'LogIn.txt')
    # Check if the file exists
    if os.path.exists(file_path):
        # Open the file and read its content
        with open(file_path, 'r') as file:
            content = file.read()

        response = HttpResponse(content, content_type='text/plain; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(file_path)}'
        return response
    else:
        return HttpResponse("File not found")
    
def clear_txt(request):
    file_path = os.path.join('LogInFile', 'LogIn.txt')

    if os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write("")

        return HttpResponse("File cleared successfully")

def home(request):
    return render(request, 'homepage.html') 

class MovesView(View):
    def get(self, request):
        test_filename = SharedData.upload_path
        if SharedData.upload_path is None:
            return redirect('homepage')
        testManifest = Manifest()
        new_ship = testManifest.read_manifest(test_filename)

        res = balancingAlg.ucs(new_ship)

        outbound_manifest = Manifest.write_manifest(self, res, test_filename)

        moves_data = []

        while True:
            move_info = {
            "origin": tuple(x + 1 for x in res.lastMove[0]),
            "destination": tuple(x + 1 for x in res.lastMove[1]),
                }
            moves_data.append(move_info)

            if res.parent is None:
                break

            res = res.parent

        moves_data.pop()
        moves_data.reverse() 

        la_time = datetime.now()
        timestamp = la_time.strftime("%m-%d-%Y %H:%M:%S")

        moves_with_timestamps = [
            f"{move['origin']} to {move['destination']} at {la_time}"
            for move in moves_data
        ]

        save_moves_to_file(moves_with_timestamps)

        context = {'moves': moves_data}
        return render(request, 'moves.html', context)
    
    template_name = "moves.html"
    def post(self, request, *args, **kwargs):
        sign_in_name = request.POST.get('SignIn', '')
        if sign_in_name:
            file_path = os.path.join('LogInFile', 'LogIn.txt')
            los_angeles_time = datetime.now()
            timestamp = los_angeles_time.strftime("%m-%d-%Y %H:%M:%S")
            with open(file_path, 'a') as file:
                file.write(f'{sign_in_name} - {timestamp}\n')

        return render(request, self.template_name, {'sign_in_name': sign_in_name})
    
def Outbound_txt(request):
    test_filename = SharedData.upload_path
    outbound_file = test_filename.replace(".txt", "_OUTBOUND.txt")
    if os.path.exists(outbound_file):
        # Open the file and read its content
        with open(outbound_file, 'r') as file:
            content = file.read()

        response = HttpResponse(content, content_type='text/plain; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename={os.path.basename(outbound_file)}'
        return response
    else:
        return HttpResponse("File not found")
    

class MovesLandUView(View):
    def get(self, request):

        print('GOT')

        instruction_list = get_object_or_404(InstructionList, pk=request.session['lu_instructs_id'])

        instructions = instruction_list.instruction_set.all()

        moves_data = []

        for instruction in instructions:
            initial_destination = (instruction.start_x + 1, instruction.start_y + 1)
            final_destination = (instruction.end_x + 1, instruction.end_y + 1)

            if initial_destination == (0,0):
                initial_destination = (instruction.description)

            if final_destination == (0,0):
                final_destination = "truck"
            

            move_info = {
                "origin": initial_destination,
                "destination": final_destination,
            }
            moves_data.append(move_info)
        
        moves_data.pop(0)

        la_time = datetime.now()
        timestamp = la_time.strftime("%m-%d-%Y %H:%M:%S")

        moves_with_timestamps = [
            f"Moved {move['origin']} to {move['destination']} at {la_time}"
            for move in moves_data
        ]

        save_moves_to_file(moves_with_timestamps)

        context = {'moves': moves_data}
        return render(request, 'movesLandU.html', context)
    
    template_name = "movesLandU.html"
    def post(self, request, *args, **kwargs):
        sign_in_name = request.POST.get('SignIn', '')
        if sign_in_name:
            file_path = os.path.join('LogInFile', 'LogIn.txt')
            los_angeles_time = datetime.now()
            timestamp = los_angeles_time.strftime("%m-%d-%Y %H:%M:%S")
            with open(file_path, 'a') as file:
                file.write(f'{sign_in_name} - {timestamp}\n')

        return render(request, self.template_name, {'sign_in_name': sign_in_name})
    
class TutorialPageView(TemplateView):
    template_name = "tutorialpage.html"

def save_moves_to_file(moves):
    file_path = os.path.join('LogInFile', 'LogIn.txt')
    with open(file_path, 'a') as ship_file:
        for move in moves:
            ship_file.write(move + '\n') 