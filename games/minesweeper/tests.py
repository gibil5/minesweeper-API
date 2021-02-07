#!/usr/bin/env python3
"""
    Test Minesweeper
"""
import time
import random
import unittest
from django.test import TestCase
from django.test import Client
from .models import Board, Cell

# Const ------------------------------------------------------------------------
#PREFIX = '\n\n------------------------ '
PREFIX = '\n\n------------------------------------------------ '

# Tools ------------------------------------------------------------------------
def get_test_board():
    if Board.objects.filter(name='Test').count() == 0:
        board = Board.objects.create(name='Test', rows=4, cols=4, nr_mines=5, numbers=[], apparent=[], flags=[], mines=[])
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
    def test_url_update(self):
        """
        Board update
        GET request
        """
        print(f"{self.prefix}test_url_update")

        # Init
        reset_game(self.board)

        # Cell
        url = f'http://127.0.0.1:8000/board_update/?board_id={self.board.id}&cell_name={self.cell_name}&flag={self.flag}'
        response = self.client.get(url)

        count = len(response.json())
        
        # Assert dimension
        self.assertEqual(count, self.board.rows * self.board.cols)
        
        for i in range(count):
            cell = response.json()[i]
            if cell['name'] == self.cell_name:
                print(cell)

                # Assert visible
                self.assertEqual(cell['visible'], True)
                self.assertIn(cell['value'], [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8])
                self.assertIn(cell['label'], ['-1', '.', '1', '2', '3', '4', '5', '6', '7', '8'])

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


    #@unittest.skip
    def test_url_init(self):
        """
        Board init
        GET request
        """
        print(f"{self.prefix}test_url_init")

        # board init
        url = f'http://127.0.0.1:8000/board_init/?board_id={self.board.id}'
        response = self.client.get(url)

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
        #self.flag = 0
        #self.cell_name = '0_0'
        self.board = get_test_board()

    def tearDown(self):
        pass


    #@unittest.skip
    def test_board_update(self):
        """
        Init and update game
        """
        print(f"{self.prefix}test_board_update")

        count_mined = 0
        count_flagged = 0
        nr_scenarios = 5

        for i in range(nr_scenarios):

            print(f'\n\nIteration: {i}')

            # Init
            reset_game(self.board)
            flag = str(random.randint(0, 1))
            x = str(random.randint(0, self.board.rows-1))
            y = str(random.randint(0, self.board.cols-1))
            cell_name = f'{x}_{y}'

            # Update
            self.board.update_game(cell_name, flag)
            print()

            # Cell
            cell = self.board.get_cell_name(cell_name)
            print(cell)
            print(f'State SM:{self.board.state_sm}')
            print(f'Flag: {flag}')

            # Assert cell
            if flag == '0':
                self.assertIn(cell.label, ['-1', '.', '1', '2', '3', '4', '5', '6', '7', '8'])
                self.assertEqual(cell.visible, True)
                self.assertEqual(cell.flagged, False)

            # Flag
            elif flag == '1':
                count_flagged += 1
                self.assertEqual(cell.label, '?')
                self.assertEqual(cell.visible, False)
                self.assertEqual(cell.flagged, True)

            # value
            self.assertIn(cell.value, [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8])

            # Assert mined
            if cell.mined:
                count_mined += 1
                if not cell.flagged:
                    self.assertEqual(self.board.state_sm, 4)
                else:
                    self.assertEqual(self.board.state_sm, 1)

        print(f'\n\nRandom test was run: {nr_scenarios} times.')
        print(f'Was mined: {count_mined} times.')
        print(f'Was flagged: {count_flagged} times.')
            

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


