"""
Module Url
"""
from django.urls import path
from . import views

# Routing
urlpatterns = [
    path("", views.index, name="index"),
    path("users/", views.users, name="users"),
    path('users_show/<int:user_id>/', views.show, name="show"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("games/", views.games, name="games"),    
    path("add_user/", views.add_user, name="add_user"),
]
