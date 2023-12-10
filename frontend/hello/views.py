from django.views.generic import TemplateView
from .forms import UploadFileForm
from django.views import View
from django.shortcuts import render


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

class LogPageView(TemplateView):
    template_name = "logdownloadpage.html"

class ManagePageView(TemplateView):
    template_name = "managepage.html"

class TutorialPageView(TemplateView):
    template_name = "tutorialpage.html"

class GridPageView(TemplateView):
    template_name = "gridpage.html"

    def get(self,request):
        # placeholder
        manifest = [[0]*12 for i in range(8)]
        manifest[0][0],manifest[0][1],manifest[0][10],manifest[0][11] = -1,-1,-1,-1
        manifest[1][1],manifest[2][1],manifest[0][2],manifest[1][11] = 1,1,1,1

        context={
            'manifest':manifest
        }

        return render(request,'gridpage.html',context)

