"""
Module Url
"""
from django.urls import path
from . import views

# Routing
urlpatterns = [
    path("", views.index, name="index"),    
    path('show/<str:board>/', views.show, name="show"),
    path("edit/<str:board>/", views.edit, name="edit"),
]
