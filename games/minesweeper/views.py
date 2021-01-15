from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util

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
    #return render(request, "minesweeper/flex.html",
    return render(request, "minesweeper/grid.html",
        {
            "board": util.get_board(board_id),
            "cells": util.get_cells(board_id),
        })
