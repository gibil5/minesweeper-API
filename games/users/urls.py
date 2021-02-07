"""
Module Url
"""
from django.urls import path
from . import views

# Routing
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("games/", views.games, name="games"),    
]
