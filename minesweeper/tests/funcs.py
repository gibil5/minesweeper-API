from django.contrib.auth.models import User
from minesweeper.models import Board, Cell


# Tools ------------------------------------------------------------------------
def get_test_user():
    return User.objects.get(username='harry')

def get_test_board():
    user = User.objects.get(username='harry')
    if Board.objects.filter(name='Test').count() == 0:
        board = Board.objects.create(name='Test', rows=4, cols=4, nr_mines=5, numbers=[], apparent=[], flags=[], mines=[], user=user)
    else:
        board = Board.objects.filter(name='Test')[0]
    return board

def reset_game(board):
    board.reset_sm()
    board.play_sm()
    board.init_game()
