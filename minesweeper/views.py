#!/usr/bin/env python3
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User, Group
from django import forms
from django_fsm import TransitionNotAllowed
from rest_framework import viewsets, permissions, generics
from .serializers import UserSerializer, GroupSerializer, BoardSerializer, CellSerializer
from .models import Board, Cell
from . import util

SUCCESS = '\nSUCCESS'
ERROR = '\nERROR'
PAGE_NOT_FOUND = 'The requested page was not found.'

#-------------------------------------------------------------------------------
class BoardForm(forms.ModelForm):
    """
    Board form
    """
    class Meta:
        """
        Meta
        """
        model = Board
        fields = ['id', 'name', 'rows', 'nr_mines']

    id = forms.IntegerField()
    name = forms.CharField(max_length=16)
    rows = forms.IntegerField(min_value=0)
    nr_mines = forms.IntegerField(min_value=0)

class NewBoardForm(forms.Form):
    """
    New Board form
    """
    id = forms.IntegerField()
    name = forms.CharField(max_length=16)
    rows = forms.IntegerField()
    nr_mines = forms.IntegerField()


#-------------------------------------------------------------------------------
class BoardUpdate(generics.ListAPIView):
    """
    Board update

    Called by REST query:
    http://127.0.0.1:8000/cells_from/?board_id=<board_id>&cmd=update&cell_name=<cell_name>
    curl -H 'Accept: application/json; indent=4' -u admin:adminadmin url http://127.0.0.1:8000/cells_from/?board_id=19&cmd=update&cell_name=4_5
    """
    serializer_class = CellSerializer

    def get_queryset(self):
        """
        Sends the update message to the model
        Returns to caller a filtered list of Cells.
        """
        #print('\n\nget_queryset')
        queryset = Cell.objects.all()
        board_id = self.request.query_params.get('board_id', None)
        cell_name = self.request.query_params.get('cell_name', None)
        flag = self.request.query_params.get('flag', None)
        if board_id is not None:
            board = Board.objects.get(id=board_id)
            queryset = queryset.filter(board=board_id)

        # Update game 
        if (cell_name is not None) and (flag is not None):
            try:
                #print('TRY UPDATE GAME')
                board.update_game(cell_name, flag)
            except TransitionNotAllowed:
                print('ERROR')
            else:
                #print('SUCCESS')
                pass

        return queryset

class BoardInit(generics.ListAPIView):
    """
    Board init
    """
    serializer_class = BoardSerializer
    def get_queryset(self):
        queryset = Board.objects.all()
        board_id = self.request.query_params.get('board_id', None)
        if board_id is not None:
            board = Board.objects.get(id=board_id)
            board.init_game()
            queryset = queryset.filter(id=board_id)
        return queryset

class BoardCheck(generics.ListAPIView):
    """
    Board check
    """
    serializer_class = BoardSerializer
    def get_queryset(self):
        queryset = Board.objects.all()

        board_id = self.request.query_params.get('board_id', None)
        cell_name = self.request.query_params.get('cell_name', None)

        if board_id is not None:
            board = Board.objects.get(id=board_id)
            queryset = queryset.filter(id=board_id)
        
        board.check_game(cell_name)

        return queryset

#-------------------------------------------------------------------------------
class CellViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cells to be viewed or edited.
    """
    queryset = Cell.objects.all().order_by('-name')
    serializer_class = CellSerializer
    #permission_classes = [permissions.IsAuthenticated]

class BoardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Boards to be viewed or edited.
    """
    queryset = Board.objects.all().order_by('name')
    serializer_class = BoardSerializer
    #permission_classes = [permissions.IsAuthenticated]


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated]

#class GroupViewSet(viewsets.ModelViewSet):
#    """
#    API endpoint that allows groups to be viewed or edited.
#    """
#    queryset = Group.objects.all()
#    serializer_class = GroupSerializer
    #permission_classes = [permissions.IsAuthenticated]

#------------------------------------- CRUD ------------------------------------
# Create your views here.

def index(request):
    """
    Index
    """
    print('*** index')
    #return render(request, "minesweeper/index_flex.html",
    return render(request, "minesweeper/index.html",
        {
            "userx": request.user,
            "boards": util.list_boards(),
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

def edit(request, board_id):
    """
    Edit
    """
    print('*** edit')
    if request.method == 'GET':
        print('get')
        form = BoardForm(instance=util.get_board(board_id))
        return render(request, "minesweeper/edit.html", {
            "form": form,
        })

def delete(request, board_id):
    """
    Delete
    """
    print('*** delete')
    util.delete_board(board_id)
    return HttpResponseRedirect(reverse("games"))

@login_required(login_url='/login')
def add_board(request):
    """
    Add board
    """
    print('*** add_board')
    user = request.user
    util.add_board(user)
    return HttpResponseRedirect(reverse("games"))

def update(request):
    """
    update
    Post
    """
    print('*** update')
    #print(request)
    #print(request.POST)
    if request.method == 'POST':
        #print('post')
        form = NewBoardForm(request.POST)
        if form.is_valid():
            #print('form is valid')
            board_id = form.cleaned_data["id"]
            name = form.cleaned_data["name"]
            rows = form.cleaned_data["rows"]
            #cols = form.cleaned_data["cols"]
            cols = rows
            nr_mines = form.cleaned_data["nr_mines"]
            util.update_board(id=board_id, name=name, rows=rows, cols=cols, nr_mines=nr_mines)
            return HttpResponseRedirect(reverse('show', args=(board_id,)))
        else:
            #print('form not valid')
            return render(request, "minesweeper/error.html", {
                "message": 'Form is not valid !'
            })

#------------------------------------- Game ------------------------------------
def play(request, board_id):
    """
    Play
    Calls board.init_game
    """
    print('*** play')
    board = util.get_board(board_id)

    if board.state_sm == 0:
        board.init_game()

    if board.state_sm in [0, 2]:
        board.play_sm()

    board.save()

    return render(request, "minesweeper/grid.html",
        {
            "board": util.get_board(board_id),
            "cells": util.get_cells(board_id),
        })

def pause(request, board_id):
    """
    pause
    """
    print('*** pause')
    board = util.get_board(board_id)
    try:
        board.pause_sm()
    except TransitionNotAllowed:
        print('\n\njx internal - ERROR: TransitionNotAllowed\n\n')
        raise TransitionNotAllowed('\n\n\njx - Error caught - Pause - Transition not allowed.\n\n\n')
    else:
        print('SUCCESS')
    board.save()    
    return HttpResponseRedirect(reverse('show', args=(board_id,)))

def reset(request, board_id):
    """
    Reset
    """
    print('*** reset')
    board = util.get_board(board_id)
    board.reset_sm()

    #board.reset_game()
    board.init_game()
    
    board.save()
    return HttpResponseRedirect(reverse('show', args=(board_id,)))

def back(request, board_id):
    """
    back
    """
    print('*** back')
    return HttpResponseRedirect(reverse('show', args=(board_id,)))
