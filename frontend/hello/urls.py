from django.urls import path
from .views import HomePageView, LogPageView, SettingsPageView

urlpatterns = [
    path("settings/", SettingsPageView.as_view(), name="settingspage"),
    path("settings/log/", LogPageView.as_view(), name="logpage"),
    path("",  HomePageView.as_view(), name="homepage"),
]