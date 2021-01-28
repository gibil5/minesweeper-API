#!/usr/bin/env python3
"""
    Tests
"""

import unittest
from django.test import TestCase
from .models import Board, Cell

# ------------------------------------------------------------------------------
#                              Test Util library
# ------------------------------------------------------------------------------
#@unittest.skip
class GameEngineTestCase(unittest.TestCase):
    """
    Unit tests
    For the game engine
    """
    def setUp(self):
        """
        Setup
        """
        self.prefix = '\n\n'
        self.board_id = 4
        self.flag = 0
        self.cell_name = '0_0'

    #@unittest.skip
    def test_init_game(self):
        """
        Init game
        """
        print(f"{self.prefix}test_init_game")
        board = Board.objects.get(id=self.board_id)
        board.init_game()
        cells = Cell.objects.filter(board=self.board_id).order_by('name')
        #print()
        #print(board.numbers)
        #print()
        #print(board.apparent)
        #print()
        #print(cells)
        
    #@unittest.skip
    def test_update_game(self):
        """
        Update game
        """
        print(f"{self.prefix}test_update_game")
        board = Board.objects.get(id=self.board_id)
        flag = self.flag
        board.update_game(self.cell_name, flag)
