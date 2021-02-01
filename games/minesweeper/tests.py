#!/usr/bin/env python3
"""
    Test suite
"""
import unittest
from django.test import TestCase
from django.test import Client
from .models import Board, Cell

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
        self.prefix = '\n\n'
        self.client = Client()
        name = 'Game 2'
        self.board = Board.objects.get(name=name)
        self.board_id = self.board.id 
        self.cell_name = '0_0'
        self.flag = '0'
        self.duration = '5555'
        self.state = 'pause'


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

        # board update
        url = f'http://127.0.0.1:8000/board_update/?board_id={self.board.id}&cell_name={self.cell_name}&flag={self.flag}'
        response = self.client.get(url)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


    #@unittest.skip
    def test_url_board_update_duration(self):
        """
        Board update duration
        GET request
        """
        print(f"{self.prefix}test_url_board_update_duration")

        # board update duration
        url = f'http://127.0.0.1:8000/board_update/?board_id={self.board.id}&duration={self.duration}'
        response = self.client.get(url)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


    #@unittest.skip
    def test_url_board_update_state(self):
        """
        Board update state
        GET request

        http://127.0.0.1:8000/update_state/?board_id=${board_id}&state=${state}
        """
        print(f"{self.prefix}test_url_board_update_state")

        # board update state
        url = f'http://127.0.0.1:8000/board_update/?board_id={self.board.id}&state={self.state}'
        response = self.client.get(url)

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


# ------------------------------------------------------------------------------
#                              Test Transactions
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
        self.prefix = '\n\n'
        self.client = Client()
        name = 'Game 2'
        self.board = Board.objects.get(name=name)

    #@unittest.skip
    def test_view_index(self):
        """
        Index view
        GET request
        """
        print(f"{self.prefix}test_view_index")
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
        self.prefix = '\n\n'
        self.flag = 0
        self.cell_name = '0_0'
        name = 'Game 3'
        self.board = Board.objects.get(name=name)

    #@unittest.skip
    def test_init_game(self):
        """
        Init game
        """
        print(f"{self.prefix}test_init_game")
        self.board.init_game()
        cells = Cell.objects.filter(board=self.board.id).order_by('name')
        
    #@unittest.skip
    def test_update_game(self):
        """
        Update game
        """
        print(f"{self.prefix}test_update_game")
        self.board.update_game(self.cell_name, self.flag)
