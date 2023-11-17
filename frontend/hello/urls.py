from django.urls import path
from .views import HomePageView, LogPageView, ManagePageView, TutorialPageView

urlpatterns = [
    path("manage/", ManagePageView.as_view(), name="managepage"),
    path("manage/log/", LogPageView.as_view(), name="logpage"),
    path("",  HomePageView.as_view(), name="homepage"),
    path("tutorial/", TutorialPageView.as_view(), name="tutorialpage"),
]