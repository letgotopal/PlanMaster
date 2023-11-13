from django.urls import path
from .views import HomePageView, LogPageView

urlpatterns = [
    path("settings/log/", LogPageView.as_view(), name="logpage"),
    path("",  HomePageView.as_view(), name="homepage"),
]