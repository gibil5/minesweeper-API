from django.shortcuts import render

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

def show(request, board):
    """
    Show
    """
    print('*** show')
    return render(request, "minesweeper/show.html",
        {
            "board": util.get_board('Board 1')
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
