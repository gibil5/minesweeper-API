#!/usr/bin/env python3
from datetime import timedelta
from .models import Board, Cell
from django.contrib.auth.models import User


# ---------------------------------- Users -------------------------------------
def add_user(data):
    username = data[0]
    first_name = data[1]
    last_name = data[2]
    email = data[3]
    password = data[4]
    is_superuser = data[5]
    user, created = User.objects.get_or_create(username=username, first_name=first_name, last_name=last_name, email=email, is_active=True, is_staff=True, is_superuser=is_superuser)
    user.set_password(password)
    user.save()
    return user

def get_users():
    return User.objects.order_by('username')

def list_boards_user(user):
    print('list_boards_user')
    boards = Board.objects.filter(user=user)    
    return boards


# ---------------------------------- Boards ------------------------------------
def list_boards():
    """
    Returns a list of boards.
    """
    boards = Board.objects.all()    
    return boards

def get_board(board_id):
    board = Board.objects.get(id=board_id)
    return board

def get_cells(board_id):
    board = Board.objects.get(id=board_id)
    cells = Cell.objects.filter(board=board)
    return cells

def delete_board(board_id):
    board = Board.objects.get(id=board_id)
    board.delete()

def add_board(username):
    user = User.objects.get(username=username)
    b = Board.objects.create(name='Test', rows=3, cols=3, nr_mines=3, nr_hidden=9, state_sm=0, numbers=[[0]], apparent=[[0]], flags=[[0]], mines=[[0]], user=user)
    b.save()
    return b

def add_cells(board_id):
    board = Board.objects.get(id=board_id)
    Cell.objects.filter(board=board).delete()
    for x in range(board.rows):
        for y in range(board.cols):
            c = Cell(id=None, name='cell_name', x=x, y=y, value=0, hidden=True, mined=False, flagged=False, board=board)
            c.save()
    return board

def update_board(id, name, rows, cols, nr_mines):
    #print('update_board')
    boards = Board.objects.filter(id=id)
    ret = boards.update(
        #id = id, 
        name = name, 
        rows = rows,
        cols = cols,
        nr_mines = nr_mines,        
        numbers = [],
        apparent = [],
        flags = [],
        mines = [],
        state_sm = 0, 
        start=None,
        end=None,
        duration=timedelta(0),
        game_over=False,
        game_win=False,
        #defaults={'first_name': 'Bob'},
    )
    print(ret)
