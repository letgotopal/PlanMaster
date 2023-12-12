from django.views.generic import TemplateView
from .forms import UploadFileForm
from django.views import View
from django.shortcuts import render
import json
from . import models
import sys
sys.path.append("..")
from backend import manifest,ship,luAlg

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

            if not request.session.session_key:
                request.session.create()

            # parse and process file
            m = manifest.Manifest()
            ship = m.read_manifest('ManifestUploads/' + uploaded_file.name)
            ship_grid = models.ShipGrid.objects.create()
            ship_grid.read_bay(ship)
            ship_grid.save()
            request.session['lu_before_id'] = ship_grid.pk

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

        ship_grid = models.ShipGrid.objects.create()
        ship_grid.read_bay(out_ship)
        ship_grid.save()
        request.session['lu_after_id'] = ship_grid.pk

        print(ship_grid.pk)

        # NOTE: Access the stored goal ship by calling
        # models.ShipGrid.objects.get(pk=request.session['lu_after_id'])

        context={
            'lu_after_id':ship_grid.pk
        }

        return render(request,self.template_name,context)

