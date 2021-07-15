#!/usr/bin/env python3
"""
    Test View
"""
import os
import unittest
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from . import funcs 

# Const ------------------------------------------------------------------------
SKIP_VIEW_TESTS = 0
PREFIX = '\n\n------------------------------------------------ '

# ------------------------------------------------------------------------------
#                              Test Views
# ------------------------------------------------------------------------------
@unittest.skipIf(SKIP_VIEW_TESTS, 'x')
class ViewsTestCase(unittest.TestCase):
    """
    Test Views
    """
    def setUp(self):
        """
        Setup
        """
        print('setUp')
        self.prefix = PREFIX
        self.client = Client()
        self.board = funcs.get_test_board()
        self.user = funcs.get_test_user()
        self.verbose = False 
        self.username = os.environ.get('TEST_USERNAME')
        self.password = os.environ.get('TEST_PASSWORD')

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
            '/users/',
            '/users/login/',
            '/users/logout/',
            f'/users/show/{self.user.id}/',

            # Boards
            f'/boards/reset/{self.board.id}/',
            f'/boards/play/{self.board.id}/',
            f'/boards/pause/{self.board.id}/',
            f'/boards/back/{self.board.id}/',
            # Crud 
            f'/boards/',
            f'/boards/show/{self.board.id}/',
            f'/boards/edit/{self.board.id}/',
            '/boards/add_board/',
            f'/boards/delete/{self.board.id}/',
        ]

        # Login 
        User = get_user_model()
        self.client.login(username=self.username, password=self.password)

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

    #@unittest.skip
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
