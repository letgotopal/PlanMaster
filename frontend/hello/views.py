from django.views.generic import TemplateView
from django.shortcuts import render


class HomePageView(TemplateView):
    template_name = "homepage.html"

class LogPageView(TemplateView):
    template_name = "logdownloadpage.html"

class SettingsPageView(TemplateView):
    template_name = "settingspage.html"

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

