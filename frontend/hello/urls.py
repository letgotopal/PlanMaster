from django.urls import path
from .views import HomePageView, LogPageView, ManagePageView, TutorialPageView, MovesView, MovesLandUView, download_txt, clear_txt, home

urlpatterns = [
    path("manage/", ManagePageView.as_view(), name="managepage"),
    path("manage/log/", LogPageView.as_view(), name="logpage"),
    path("",  HomePageView.as_view(), name="homepage"),
    path("tutorial/", TutorialPageView.as_view(), name="tutorialpage"),
    path('download-txt/', download_txt, name='download_txt'),
    path('clear-txt/', clear_txt, name='clear_txt'),
    path('home/', home, name='home'),
    path('moves/', MovesView.as_view(), name='movespage'),
    path('movesLandU/', MovesLandUView.as_view(), name='movespageU'),
    
]