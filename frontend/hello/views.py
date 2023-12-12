from django.views.generic import TemplateView
from .forms import UploadFileForm
from django.views import View
from django.shortcuts import render
from datetime import datetime
from django.http import HttpResponse
import os
from backend.manifest import Manifest
from backend import balancingAlg
from backend.ship import Ship
from backend import luAlg


class HomePageView(View):
    template_name = "homepage.html"

    def get(self, request, *args, **kwargs):
        form = UploadFileForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            # Process the uploaded file as needed
            # For example, save the file to a specific location
            with open('ManifestUploads/' + uploaded_file.name, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            # Render the template with a success message and uploaded file name
            return render(request, self.template_name, {'form': form, 'upload_success': True, 'uploaded_file_name': uploaded_file.name})
        return render(request, self.template_name, {'form': form})
    

    def post(self, request, *args, **kwargs):
        sign_in_name = request.POST.get('SignIn', '')
        if sign_in_name:
            file_path = '/Users/mohamed/Desktop/PlanMaster/frontend/LogInFile/LogIn.txt'
            timestamp = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
            with open(file_path, 'a') as file:
                file.write(f'{sign_in_name} - {timestamp}\n')

        return render(request, self.template_name, {'sign_in_name': sign_in_name})

class LogPageView(TemplateView):
    template_name = "logdownloadpage.html"

class ManagePageView(TemplateView):
    template_name = "managepage.html"

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
        test_filename = "backend/ShipCase4.txt"
        testManifest = Manifest()
        new_ship = testManifest.read_manifest(test_filename)

        res = balancingAlg.ucs(new_ship)

        moves_data = []

        while True:
            move_info = {
            "origin": res.lastMove[0],
             "destination": res.lastMove[1],
                }
            moves_data.append(move_info)

            if res.parent is None:
                break

            res = res.parent

        moves_data.pop()
        moves_data.reverse() 

        context = {'moves': moves_data}
        return render(request, 'moves.html', context)
    
class MovesLandUView(View):
    def get(self, request):
        test_filename = "backend/ShipCase1.txt"
        testManifest = Manifest()
        new_ship = testManifest.read_manifest(test_filename)
        anylist = [(1,3)]

        res = luAlg.ucs(new_ship, anylist)

        moves_data = []

        while True:
            move_info = {
            "origin": res.lastMove[0],
             "destination": res.lastMove[1],
                }
            moves_data.append(move_info)

            if res.parent is None:
                break

            res = res.parent
            
        moves_data.pop()
        moves_data.reverse() 

        context = {'moves': moves_data}
        return render(request, 'movesLandU.html', context)

class TutorialPageView(TemplateView):
    template_name = "tutorialpage.html"


