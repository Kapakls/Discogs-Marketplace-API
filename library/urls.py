from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login, name="login"),
    path("callback/", views.callback, name="callback"),

    path("music/", views.music, name="music"),
    path("music/fetch/", views.music_fetch, name="music_fetch"),
    path("music/results/", views.music_results, name="music_results"),
]