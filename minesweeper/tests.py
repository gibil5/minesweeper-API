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
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

# Const ------------------------------------------------------------------------
PREFIX = '\n\n------------------------------------------------ '

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


# ------------------------------------------------------------------------------
#                              Test Requests
# ------------------------------------------------------------------------------
#@unittest.skip
class ViewsTestCase(unittest.TestCase):
    """
    Test Requests
    All urls
    """
    def setUp(self):
        """
        Setup
        """
        print('setUp')
        self.prefix = PREFIX
        self.client = Client()
        self.board = get_test_board()
        self.user = get_test_user()

        self.verbose = True 
        #self.verbose = False
        
        # Create temp user
        #User = get_user_model()
        #name = 'temporary'
        #if User.objects.filter(username=name).count() == 0:
        #    user = User.objects.create_user(name, 'temporary@gmail.com', 'temporary')
        

    #@unittest.skip
    def test_view_get_all(self):
        """
        All GET requests
        """
        print(f"{self.prefix}test_view_get_all")

        requests = [

            # Users
            '/',
            '/users/games/',
            '/users/index/',
            '/users/login/',
            '/users/logout/',
            f'/users/show/{self.user.id}/',

            # Boards
            f'/boards/reset/{self.board.id}/',
            f'/boards/play/{self.board.id}/',
            f'/boards/pause/{self.board.id}/',
            f'/boards/back/{self.board.id}/',
            f'/boards/',
            f'/boards/show/{self.board.id}/',
            f'/boards/edit/{self.board.id}/',
            '/boards/add_board/',
            f'/boards/delete/{self.board.id}/',
        ]

        # Login 
        User = get_user_model()
        self.client.login(username='harry', password='nyctal6+')

        for req in requests:
            request = req
            if self.verbose:
                print(f'{request}\n')
            # Get request
            response = self.client.get(request)
            if self.verbose:
                print(response)
            # Check that the response is either 200 or 302
            self.assertIn(response.status_code, [200, 302])
            print()


    @unittest.skip
    def test_view_post_all(self):
        """
        All POST requests
        """
        print(f"{self.prefix}test_view_post_all")

        requests = [
            # Board
            '/boards/update/',
        ]

        id = self.board.id
        name = 'Test'
        rows = '7'
        cols = '7'
        nr_mines = '7'

        for req in requests:
            request = req
            if self.verbose:
                print(request)     
            # Post request
            response = self.client.post(req, { 'id': {id}, 'name': {name}, 'rows': {rows}, 'cols': {cols}, 'nr_mines': {nr_mines} })
            if self.verbose:            
                print(response)
            # Check that the response is either 200 or 302
            self.assertIn(response.status_code, [200, 302])
            print()



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
        self.verbose = True 
        #self.verbose = False


    #@unittest.skip
    def test_url_init(self):
        """
        Board init
        GET request
        """
        print(f"{self.prefix}test_url_init")

        requests = [
            # Board - Game
            f'http://127.0.0.1:8000/rest/boards/',
            f'http://127.0.0.1:8000/rest/boards/{self.board.id}/',
            f'http://127.0.0.1:8000/rest/board_init/?board_id={self.board.id}',
            f'http://127.0.0.1:8000/rest/board_update/?board_id={self.board.id}&cell_name={self.cell_name}&flag={self.flag}',
        ]

        for url in requests:
            if self.verbose:            
                print(url)            

            # Get request
            response = self.client.get(url)
            if self.verbose:            
                print(response)
                print()

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
            

