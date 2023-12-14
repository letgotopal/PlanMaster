from django.urls import path
from .views import HomePageView, LogPageView, ManagePageView, TutorialPageView, MovesView, MovesLandUView, GridPageView, download_txt, clear_txt, home

urlpatterns = [
    path("manage/", ManagePageView.as_view(), name="managepage"),
    path("manage/log/", LogPageView.as_view(), name="logpage"),
    path("",  HomePageView.as_view(), name="homepage"),
    path("gridpage/", GridPageView.as_view(), name="gridpage"),
    path("gridpage/process_grid", GridPageView.as_view(), name="process_grid"),
    path("tutorial/", TutorialPageView.as_view(), name="tutorialpage"),
    path("gridpage/", GridPageView.as_view(), name="gridpage"),
    path("gridpage/process_grid", GridPageView.as_view(), name="process_grid"),
    path('download-txt/', download_txt, name='download_txt'),
    path('clear-txt/', clear_txt, name='clear_txt'),
    path('home/', home, name='home'),
    path('moves/', MovesView.as_view(), name='movespage'),
    path('movesLandU/', MovesLandUView.as_view(), name='movespageU'),

]