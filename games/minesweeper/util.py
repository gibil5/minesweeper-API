#!/usr/bin/env python3
from datetime import timedelta
from .models import Board, Cell

def list_boards():
    """
    Returns a list of boards.
    """
    boards = Board.objects.all()    
    return boards

def get_board(board_id):
    #print('get_board')
    #print(board_id)
    board = Board.objects.get(id=board_id)
    #print(board)
    return board

def get_cells(board_id):
    #print('get_cells')
    #print(board_id)
    board = Board.objects.get(id=board_id)
    cells = Cell.objects.filter(board=board)
    #print(cells)
    return cells

def delete_board(board_id):
    #print('delete_board')
    #print(board_id)
    board = Board.objects.get(id=board_id)
    board.delete()

def add_board(name):
    #print('add_board')
    b = Board(name='Test', rows=3, cols=3, mines=3, nr_hidden_cells=9, state='BEGIN', duration=timedelta(minutes=0))
    b.save()
    return b

def add_cells(board_id):
    #print('add_cells')
    #print(board_id)    
    board = Board.objects.get(id=board_id)
    Cell.objects.filter(board=board).delete()
    for x in range(board.rows):
        for y in range(board.cols):
            c = Cell(id=None, name='cell_name', x=x, y=y, value=0, hidden=True, mined=False, flagged=False, board=board)
            c.save()
    #print(board)
    return board



