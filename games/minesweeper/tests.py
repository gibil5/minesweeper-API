#!/usr/bin/env python3
"""
    Test suite
"""
import unittest
from django.test import TestCase
from django.test import Client
from .models import Board, Cell

# Const ------------------------------------------------------------------------
#PREFIX = '\n\n***** '
PREFIX = '\n\n------------------------ '

# Tools ------------------------------------------------------------------------
def get_test_board():
    if Board.objects.filter(name='Test').count() == 0:
        board = Board.objects.create(name='Test', rows=4, cols=4, nr_mines=1, numbers=[], apparent=[], flags=[], mines=[])
    else:
        board = Board.objects.get(name='Test')
    return board

def reset_game(board):
    board.reset_sm()
    board.play_sm()
    board.init_game()


# ------------------------------------------------------------------------------
#                              Test REST API
# ------------------------------------------------------------------------------
#@unittest.skip
class RestApiTestCase(unittest.TestCase):
    """
    Test REST API
    """
    def setUp(self):
        """
        Setup
        """
        self.prefix = PREFIX
        self.client = Client()
        self.cell_name = '0_0'
        self.flag = '0'
        self.duration = '5555'
        self.state = 'pause'
        self.board = get_test_board()

    def tearDown(self):
        pass


    #@unittest.skip
    def test_url_board_init(self):
        """
        Board init
        GET request
        """
        print(f"{self.prefix}test_url_board_init")

        # board init
        url = f'http://127.0.0.1:8000/board_init/?board_id={self.board.id}'
        response = self.client.get(url)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


    #@unittest.skip
    def test_url_board_update(self):
        """
        Board update
        GET request
        """
        print(f"{self.prefix}test_url_board_update")

        # Init
        reset_game(self.board)

        # State 
        #url = f'http://127.0.0.1:8000/board_update/?board_id={self.board.id}&state={self.state}'
        # Duration
        #url = f'http://127.0.0.1:8000/board_update/?board_id={self.board.id}&duration={self.duration}'
        # Cell
        url = f'http://127.0.0.1:8000/board_update/?board_id={self.board.id}&cell_name={self.cell_name}&flag={self.flag}'
        response = self.client.get(url)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


# ------------------------------------------------------------------------------
#                              Test Views
# ------------------------------------------------------------------------------
#@unittest.skip
class TransactionsTestCase(unittest.TestCase):
    """
    Test Transactions
    """
    def setUp(self):
        """
        Setup
        """
        print('setUp')
        self.prefix = PREFIX
        self.client = Client()
        self.board = get_test_board()

    def tearDown(self):
        pass


    #@unittest.skip
    def test_view_index(self):
        """
        Index view
        GET request
        """
        print(f"{self.prefix}test_view_index")

        # Index
        response = self.client.get('/index/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


    #@unittest.skip
    def test_view_show(self):
        """
        Show view
        GET request
        """
        print(f"{self.prefix}test_view_show")

        # Show
        response = self.client.get(f'/show/{self.board.id}/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    #@unittest.skip
    def test_view_play(self):
        """
        Play view
        GET request
        """
        print(f"{self.prefix}test_view_play")

        # Init
        self.board.reset_sm()
        self.board.init_game()

        # Play
        response = self.client.get(f'/play/{self.board.id}/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


# ------------------------------------------------------------------------------
#                              Test Models
# ------------------------------------------------------------------------------
#@unittest.skip
class GameEngineTestCase(unittest.TestCase):
    """
    Test Models
    """
    def setUp(self):
        """
        Setup
        """
        self.prefix = PREFIX
        self.flag = 0
        self.cell_name = '0_0'
        self.board = get_test_board()

    def tearDown(self):
        pass

    #@unittest.skip
    def test_init_and_update_game(self):
        """
        Init and update game
        """
        print(f"{self.prefix}test_init_and_update_game")
        self.board.init_game()
        cells = Cell.objects.filter(board=self.board.id).order_by('name')        
        self.board.update_game(self.cell_name, self.flag)
