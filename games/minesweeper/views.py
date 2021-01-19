from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from . import util
from .models import Board, Cell
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import UserSerializer, GroupSerializer, BoardSerializer, CellSerializer

from rest_framework import generics


class CellList(generics.ListAPIView):
    serializer_class = CellSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        print('mark 1')
        queryset = Cell.objects.all()
        board_id = self.request.query_params.get('board_id', None)
        cmd = self.request.query_params.get('cmd', None)
        cell_name = self.request.query_params.get('cell_name', None)
        #if (board_id & cmd) is not None:
        if board_id is not None:
            board = Board.objects.get(id=board_id)
            print(board)
            board.calc(cmd, cell_name)
            queryset = queryset.filter(board=board_id)
        return queryset



class CellViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cells to be viewed or edited.
    """
    queryset = Cell.objects.all().order_by('-name')
    serializer_class = CellSerializer
    #permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    #permission_classes = [permissions.IsAuthenticated]

class BoardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Boards to be viewed or edited.
    """
    #queryset = Board.objects.all().order_by('-start')
    queryset = Board.objects.all().order_by('name')
    serializer_class = BoardSerializer
    #permission_classes = [permissions.IsAuthenticated]



# Create your views here.
def index(request):
    """
    Index
    """
    print('*** index')
    return render(request, "minesweeper/index.html",
        {
            "boards": util.list_boards()
        })

def show(request, board_id):
    """
    Show
    """
    print('*** show')
    return render(request, "minesweeper/show.html",
        {
            "board": util.get_board(board_id),
            "cells": util.get_cells(board_id),
        })

def edit(request, board):
    """
    Edit
    """
    print('*** edit')
    return render(request, "minesweeper/edit.html",
        {
            #"cells": util.list_cells()
        })

def delete(request, board_id):
    """
    Delete
    """
    print('*** delete')
    util.delete_board(board_id)
    return render(request, "minesweeper/index.html",
        {
            "boards": util.list_boards()
        })

def add_cells(request, board_id):
    """
    Add cells
    """
    print('*** add_cells')
    return render(request, "minesweeper/show.html",
        {
            "board": util.add_cells(board_id)
        })

def add_board(request):
    """
    Add board
    """
    print('*** add_board')
    board = util.add_board('Test')
    return HttpResponseRedirect(reverse("index"))

def play(request, board_id):
    """
    Play
    """
    print('*** play')
    board = util.get_board(board_id)
    board.calc('init')
    return render(request, "minesweeper/grid.html",
        {
            "board": util.get_board(board_id),
            "cells": util.get_cells(board_id),
        })

