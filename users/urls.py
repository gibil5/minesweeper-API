"""
Module Url
"""
from django.urls import path
from . import views

# Routing
urlpatterns = [
    path("", views.index, name="index"),
    path("users/index/", views.users, name="users"),
    path('users/show/<int:user_id>/', views.show, name="users_show"),
    path("users/login/", views.login_view, name="login"),
    path("users/logout/", views.logout_view, name="logout"),
    path("users/games/", views.games, name="games"),
    #path("users/add_users/", views.add_users, name="add_users"),
]
