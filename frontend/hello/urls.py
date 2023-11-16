from django.urls import path
from .views import HomePageView, LogPageView, SettingsPageView, TutorialPageView

urlpatterns = [
    path("settings/", SettingsPageView.as_view(), name="settingspage"),
    path("settings/log/", LogPageView.as_view(), name="logpage"),
    path("",  HomePageView.as_view(), name="homepage"),
    path("tutorial/", TutorialPageView.as_view(), name="tutorialpage"),
]