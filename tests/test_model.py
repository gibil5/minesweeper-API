"""
Testing with Pytest 
Integration tests

Tests:
    test_init_board 
    test_update_board 
    test_flag_cell 

Test 
    pytest tests
"""
import pytest  
import random

PREFIX = '\n\n---------------------------------------------------------------- '
VERBOSE = 0

# Tools ------------------------------------------------------------------------
def draw(vec):
    for x in range(len(vec)):
        for y in range(len(vec)):
            print(vec[x][y], '\t', end='')
        print()

# Tests ------------------------------------------------------------------------
def test_init_board(board):
    print(f"{PREFIX}test_init_board")
    # Init 
    board.init_game()   
    # Assert 
    assert len(board.numbers) == 7
    assert len(board.apparent) == 7
    assert len(board.mines) == 3
    assert len(board.flags) == 0

def test_update_board(board):
    print(f"{PREFIX}test_update_board")
    # Init
    board.init_game()
    flag = str(0)
    x = random.randint(0, board.rows-1)
    y = random.randint(0, board.cols-1)
    cell_name = f'{x}_{y}'    

    # Print 
    if VERBOSE:
        print(cell_name)
        print()
        draw(board.numbers)
        print()
        draw(board.apparent)
        print()

    # Update
    board.update_game(cell_name, flag)  

    # Print 
    if VERBOSE:
        print()
        draw(board.apparent)

def test_flag_cell(board):
    print(f"{PREFIX}test_flag_cell")
    # Init
    board.init_game()       
    flag = str(1)
    x = random.randint(0, board.rows-1)
    y = random.randint(0, board.cols-1)
    cell_name = f'{x}_{y}'
    # Update
    board.update_game(cell_name, flag)      
    # Assert 
    assert [[x, y]] == board.flags
