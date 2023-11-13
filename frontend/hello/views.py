from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "homepage.html"

class LogPageView(TemplateView):
    template_name = "logdownloadpage.html"