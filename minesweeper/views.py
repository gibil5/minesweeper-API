#!/usr/bin/env python3
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django_fsm import TransitionNotAllowed
from minesweeper.models import Board
from minesweeper.forms import BoardForm
from . import util

#------------------------------------- Const -----------------------------------
SUCCESS = '\nSUCCESS'
ERROR = '\nERROR'
PAGE_NOT_FOUND = 'The requested page was not found.'

#------------------------------------- CRUD ------------------------------------
# Create your views here.

def index(request):
    """
    Index
    """
    print('*** index')
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

# Edit 
def edit(request, board_id):
    """
    Edit - GET
    """
    print('*** edit')
    if request.method == 'GET':
        print('get')
        form = BoardForm(instance=util.get_board(board_id))
        return render(request, "minesweeper/edit.html", {
            "form": form,
        })


# Update
def update(request):
    """
    Update - POST
    """
    print('*** update')
    #print(request)
    #print(request.POST)
    if request.method == 'POST':
        #print('post')
        form = BoardForm(request.POST)
        if form.is_valid():
            #print('form is valid')
            board_id = form.cleaned_data["id"]
            name = form.cleaned_data["name"]
            rows = form.cleaned_data["rows"]
            cols = rows
            nr_mines = form.cleaned_data["nr_mines"]
            util.update_board(id=board_id, name=name, rows=rows, cols=cols, nr_mines=nr_mines)
            return HttpResponseRedirect(reverse('show', args=(board_id,)))
        else:
            #print('form not valid')
            return render(request, "minesweeper/error.html", {
                "message": 'Form is not valid !'
            })

def delete(request, board_id):
    """
    Delete
    """
    print('*** delete')
    util.delete_board(board_id)
    return HttpResponseRedirect(reverse("games"))

#------------------------------------- Add ------------------------------------
@login_required(login_url='/login')
def add_board(request):
    """
    Add board
    """
    print('*** add_board')
    user = request.user
    util.add_board(user)
    return HttpResponseRedirect(reverse("games"))

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
