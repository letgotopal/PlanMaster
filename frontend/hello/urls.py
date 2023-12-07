from django.urls import path
from .views import HomePageView, LogPageView, SettingsPageView, GridPageView

urlpatterns = [
    path("settings/", SettingsPageView.as_view(), name="settingspage"),
    path("settings/log/", LogPageView.as_view(), name="logpage"),
    path("",  HomePageView.as_view(), name="homepage"),
    path("gridpage/", GridPageView.as_view(), name="gridpage")
]