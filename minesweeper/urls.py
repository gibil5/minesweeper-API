"""
Module Url
"""
from django.urls import path
from . import views

# Routing
urlpatterns = [
    path("index/", views.index, name="index"),    
    path("add_board/", views.add_board, name="add_board"),
    path('show/<int:board_id>/', views.show, name="show"),
    path("delete/<int:board_id>/", views.delete, name="delete"),
    path('play/<int:board_id>/', views.play, name="play"),
    path('reset/<int:board_id>/', views.reset, name="reset"),
    path('pause/<int:board_id>/', views.pause, name="pause"),
    path('back/<int:board_id>/', views.back, name="back"),
    path('edit/<int:board_id>/', views.edit, name="edit"),
    path("update/", views.update, name="update"),
]
