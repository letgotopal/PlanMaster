from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "homepage.html"

class LogPageView(TemplateView):
    template_name = "logdownloadpage.html"

class SettingsPageView(TemplateView):
    template_name = "settingspage.html"

class GridPageView(TemplateView):
    template_name = "gridpage.html"

