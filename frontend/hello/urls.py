from django.urls import path
from .views import HomePageView, LogPageView, GridPageView, ManagePageView, TutorialPageView

urlpatterns = [
    path("manage/", ManagePageView.as_view(), name="managepage"),
    path("manage/log/", LogPageView.as_view(), name="logpage"),
    path("",  HomePageView.as_view(), name="homepage"),
    path("gridpage/", GridPageView.as_view(), name="gridpage"),
    path("gridpage/process_grid", GridPageView.as_view(), name="process_grid"),
    path("tutorial/", TutorialPageView.as_view(), name="tutorialpage"),
]