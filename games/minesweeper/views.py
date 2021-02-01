#!/usr/bin/env python3
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, generics
from .serializers import UserSerializer, GroupSerializer, BoardSerializer, CellSerializer
from .models import Board, Cell
from . import util


#-------------------------------------------------------------------------------
class BoardInit(generics.ListAPIView):
    serializer_class = BoardSerializer
    def get_queryset(self):
        queryset = Board.objects.all()
        board_id = self.request.query_params.get('board_id', None)
        if board_id is not None:
            board = Board.objects.get(id=board_id)
            board.init_game()
            queryset = queryset.filter(id=board_id)
        return queryset


class BoardUpdate(generics.ListAPIView):
    """
    Called by REST query:
    http://127.0.0.1:8000/cells_from/?board_id=<board_id>&cmd=update&cell_name=<cell_name>
    Ex:
    curl -H 'Accept: application/json; indent=4' -u admin:adminadmin url http://127.0.0.1:8000/cells_from/?board_id=19&cmd=update&cell_name=4_5
    """
    serializer_class = CellSerializer

    def get_queryset(self):
        """
        Sends the update message to the model
        Returns to caller a filtered list of Cells.
        """
        queryset = Cell.objects.all()
        board_id = self.request.query_params.get('board_id', None)

        cell_name = self.request.query_params.get('cell_name', None)
        flag = self.request.query_params.get('flag', None)

        duration = self.request.query_params.get('duration', None)

        state = self.request.query_params.get('state', None)

        if board_id is not None:
            board = Board.objects.get(id=board_id)
            print(board)
            queryset = queryset.filter(board=board_id)

        # Update game 
        if (cell_name is not None) and (flag is not None):
            board.update_game(cell_name, flag)

        # Update duration
        if duration is not None:
            board.update_duration(duration)

        # Update state 
        if state is not None:
            board.update_state(state)

        return queryset


#-------------------------------------------------------------------------------
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
    queryset = Board.objects.all().order_by('name')
    serializer_class = BoardSerializer
    #permission_classes = [permissions.IsAuthenticated]

#-------------------------------------------------------------------------------
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

#def edit(request, board):
#    """
#    Edit
#    """
#    print('*** edit')
#    return render(request, "minesweeper/edit.html",
#        {
            #"cells": util.list_cells()
#        })

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

def add_board(request):
    """
    Add board
    """
    print('*** add_board')
    util.add_board('Test')
    return HttpResponseRedirect(reverse("index"))


def play(request, board_id):
    """
    Play
    Calls board.init_game
    """
    print('*** play')
    board = util.get_board(board_id)


    if board.state in ['end']:
        return HttpResponseRedirect(reverse('show', args=(board_id,)))

    elif board.state in ['init']:
        board.init_game()

    elif board.state in ['pause']:
        board.state = 'start'
        board.save()

    return render(request, "minesweeper/grid.html",
        {
            "board": util.get_board(board_id),
            "cells": util.get_cells(board_id),
        })


def reset(request, board_id):
    """
    Reset
    """
    print('*** reset')
    board = util.get_board(board_id)
    board.reset_game()
    return HttpResponseRedirect(reverse('show', args=(board_id,)))


def pause(request, board_id):
    """
    pause
    """
    print('*** pause')
    board = util.get_board(board_id)
    board.pause_game()
    return HttpResponseRedirect(reverse('show', args=(board_id,)))
    #return render(request, "minesweeper/grid.html",
    #    {
    #        "board": util.get_board(board_id),
    #        "cells": util.get_cells(board_id),
    #    })

