"""
Module Url
"""
from django.urls import path
from . import views

# Routing
urlpatterns = [
    path("", views.index, name="index"),    
    path("add_board/", views.add_board, name="add_board"),
    path('show/<int:board_id>/', views.show, name="show"),
    path("delete/<int:board_id>/", views.delete, name="delete"),
    path("add_cells/<int:board_id>/", views.add_cells, name="add_cells"),
    path('play/<int:board_id>/', views.play, name="play"),
    path("cells/", views.cells, name="cells"),
]
