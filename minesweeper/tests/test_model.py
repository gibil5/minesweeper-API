#!/usr/bin/env python3
"""
    Test Model
"""
import random
import unittest
from django.test import TestCase
from . import funcs 

# Const ------------------------------------------------------------------------
SKIP_MODEL_TESTS = 1
PREFIX = '\n\n---------------------------------------------------------------- '

# ------------------------------------------------------------------------------
#                              Test Models
# ------------------------------------------------------------------------------
@unittest.skipIf(SKIP_MODEL_TESTS, 'x')
class GameEngineTestCase(unittest.TestCase):
    """
    Test Model
        Board 
        Cell 
    """
    def setUp(self):
        """
        Setup
        """
        self.prefix = PREFIX
        self.board = funcs.get_test_board()
        self.verbose = False 

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
            funcs.reset_game(self.board)
            flag = str(random.randint(0, 1))
            x = str(random.randint(0, self.board.rows-1))
            y = str(random.randint(0, self.board.cols-1))
            cell_name = f'{x}_{y}'

            # Update
            self.board.update_game(cell_name, flag)
            print()

            # Cell
            cell = self.board.get_cell_by_name(cell_name)
            if self.verbose:            
                print(cell)
                print(f'State SM:{self.board.state_sm}')
                print(f'Flag: {flag}')

            # Assert cell
            if flag == '0':
                #self.assertIn(cell.label, ['-1', '0', '1', '2', '3', '4', '5', '6', '7', '8'])
                self.assertIn(cell.label, ['-1', '.', '1', '2', '3', '4', '5', '6', '7', '8'])
                self.assertEqual(cell.visible, True)
                self.assertEqual(cell.flagged, False)

            # Flag
            elif flag == '1':
                count_flagged += 1
                self.assertIn(cell.label, ['-1', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8'])
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

        if self.verbose:            
            print(f'\n\nRandom test was run: {nr_scenarios} times.')
            print(f'Was mined: {count_mined} times.')
            print(f'Was flagged: {count_flagged} times.')
