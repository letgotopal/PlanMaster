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
    
'''
    def post(self, request, *args, **kwargs):
        sign_in_name = request.POST.get('SignIn', '')
        if sign_in_name:
            file_path = '/Users/mohamed/Desktop/PlanMaster/frontend/LogInFile/LogIn.txt'
            los_angeles_time = datetime.now()
            timestamp = los_angeles_time.strftime("%m-%d-%Y %H:%M:%S")
            with open(file_path, 'a') as file:
                file.write(f'{sign_in_name} - {timestamp}\n')

        return render(request, self.template_name, {'sign_in_name': sign_in_name})

'''
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
            file_path = '/Users/mohamed/Desktop/PlanMaster/frontend/LogInFile/LogIn.txt'
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

        # set status of grid cells
        # 1 for occupied, 0 for empty, -1 for n/a
        status = [[0]*grid_rows[0].shipcell_set.all().count() for _ in range(grid_rows.count())]
        for i in range(grid_rows.count()):
            row_cells = grid_rows[i].shipcell_set.all()
            for j in range(row_cells.count()):
                if row_cells[j].description == 'NAN':
                    status[i][j] = -1
                elif row_cells[j].description == 'UNUSED':
                    status[i][j] = 0
                else:
                    status[i][j] = 1

        context={
            'status':status,
            'grid_data':grid_data
        }

        return render(request,self.template_name,context)
    
    def post(self,request):
        unload_r = json.loads(request.POST.get('unload_r'))
        unload_c = json.loads(request.POST.get('unload_c'))

        print(unload_r,unload_c)

        grid_data = models.ShipGrid.objects.get(pk=request.session['lu_before_id'])

        # convert model to ship and run ucs
        in_ship = grid_data.to_ship()
        out_ship = luAlg.ucs(in_ship,[(unload_r[i],unload_c[i]) for i in range(len(unload_r))])

        # generate trace to goal ship
        instructs = models.InstructionList.objects.create()
        instructs.read_trace(trace.trace(out_ship))
        instructs.save()
        request.session['lu_instructs_id'] = instructs.pk

        print(request.session['lu_instructs_id'])

        # NOTE: Access the stored instruction list by calling
        # models.InstructionList.objects.get(pk=request.session['lu_instructs_id'])
        # Instruction objects can be referenced by
        # instruction_list.instruction_set.all()[index]

        return render(request,self.template_name)
    
def download_txt(request):
    file_path = "/Users/mohamed/Desktop/PlanMaster/frontend/LogInFile/LogIn.txt"
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
    file_path = "/Users/mohamed/Desktop/PlanMaster/frontend/LogInFile/LogIn.txt"

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
            return redirect('home')
        testManifest = Manifest()
        new_ship = testManifest.read_manifest(test_filename)

        res = balancingAlg.ucs(new_ship)

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

        context = {'moves': moves_data}
        return render(request, 'moves.html', context)
    
    template_name = "moves.html"
    def post(self, request, *args, **kwargs):
        sign_in_name = request.POST.get('SignIn', '')
        if sign_in_name:
            file_path = '/Users/mohamed/Desktop/PlanMaster/frontend/LogInFile/LogIn.txt'
            los_angeles_time = datetime.now()
            timestamp = los_angeles_time.strftime("%m-%d-%Y %H:%M:%S")
            with open(file_path, 'a') as file:
                file.write(f'{sign_in_name} - {timestamp}\n')

        return render(request, self.template_name, {'sign_in_name': sign_in_name})

class MovesLandUView(View):
    def get(self, request):

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
                "origin": (instruction.start_x + 1, instruction.start_y + 1),
                "destination": final_destination,
            }
            moves_data.append(move_info)
        
        moves_data.pop(0)

        context = {'moves': moves_data}
        return render(request, 'movesLandU.html', context)
    
    template_name = "movesLandU.html"
    def post(self, request, *args, **kwargs):
        sign_in_name = request.POST.get('SignIn', '')
        if sign_in_name:
            file_path = '/Users/mohamed/Desktop/PlanMaster/frontend/LogInFile/LogIn.txt'
            los_angeles_time = datetime.now()
            timestamp = los_angeles_time.strftime("%m-%d-%Y %H:%M:%S")
            with open(file_path, 'a') as file:
                file.write(f'{sign_in_name} - {timestamp}\n')

        return render(request, self.template_name, {'sign_in_name': sign_in_name})
    
class TutorialPageView(TemplateView):
    template_name = "tutorialpage.html"


