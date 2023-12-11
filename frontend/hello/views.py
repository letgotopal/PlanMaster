from django.views.generic import TemplateView
from .forms import UploadFileForm
from django.views import View
from django.shortcuts import render
from . import models
import sys
sys.path.append("..")
from backend import manifest

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

            # parse and process file
            m = manifest.Manifest()
            ship = m.read_manifest('ManifestUploads/' + uploaded_file.name)
            ship_grid = models.ShipGrid.objects.create()
            ship_grid.read_bay(ship)
            ship_grid.save()

            # Render the template with a success message and uploaded file name
            return render(request, self.template_name, {'form': form, 'upload_success': True, 'uploaded_file_name': uploaded_file.name})
        return render(request, self.template_name, {'form': form})

class LogPageView(TemplateView):
    template_name = "logdownloadpage.html"

class ManagePageView(TemplateView):
    template_name = "managepage.html"

class TutorialPageView(TemplateView):
    template_name = "tutorialpage.html"

class GridPageView(TemplateView):
    template_name = "gridpage.html"

    def get(self,request):

        grid_data = models.ShipGrid.objects.latest('id')
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

        return render(request,'gridpage.html',context)

