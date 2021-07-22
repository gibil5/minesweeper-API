#!/usr/bin/env python3
"""
Test API

Tests
    test_rest_api_get

GET Endpoints
    /rest/users/

    /rest/boards/
    /rest/boards/{self.board.id}/
    /rest/board_init/?board_id={self.board.id}
    /rest/board_update/?board_id={self.board.id}&cell_name={self.cell_name}&flag={self.flag}
"""
import os
import unittest
from django.test import Client
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from . import funcs 

# Const ------------------------------------------------------------------------
SKIP_API_TESTS = 0
PREFIX = '\n\n---------------------------------------------------------------- '

# ------------------------------------------------------------------------------
#                              Test REST API
# ------------------------------------------------------------------------------
@unittest.skipIf(SKIP_API_TESTS, 'x')
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
        self.board = funcs.get_test_board()
        self.verbose = False 
        self.username = os.environ.get('TEST_USERNAME')
        self.password = os.environ.get('TEST_PASSWORD')

    #@unittest.skip
    def test_rest_api_get(self):
        """
        Test REST-API
        GET request
        """
        print(f"{self.prefix}test_rest_api_get")
        print(SKIP_API_TESTS)

        requests = [
            # Board - Game
            f'/rest/boards/',
            f'/rest/boards/{self.board.id}/',
            f'/rest/board_init/?board_id={self.board.id}',
            f'/rest/board_update/?board_id={self.board.id}&cell_name={self.cell_name}&flag={self.flag}',
            f'/rest/users/',
            #f'/rest/groups/',
        ]

        # Login 
        User = get_user_model()
        self.client.login(username=self.username, password=self.password)
        for url in requests:       
            print(url)            

            # Get request
            response = self.client.get(url)
            if self.verbose:            
                print(response)
                print()

            # Check that the response is 200 OK.
            self.assertEqual(response.status_code, 200)
