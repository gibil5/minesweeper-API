import pytest  
from django.contrib.auth.models import User
from minesweeper.models import Board, Cell

prefix = '\n\n------------------------------------------------ '
verbose = True

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



# Fixtures ---------------------------------------------------------------------
@pytest.fixture(scope="session")
def fixture_1():
    print('fixture_1')
    print('Start')
    yield 1 
    print('End')



# Tests ------------------------------------------------------------------------
@pytest.mark.django_db()
def x_test_user_create():
    print('test_user_create')
    User.objects.create_user('test', 'test@test.com', 'test')
    assert User.objects.count() == 1


def x_test_example(fixture_1):
    print('test_example')
    num = fixture_1
    print(num)
    assert num == 1 


def x_test_board_update():
    """
    Init and update game
    """
    print(f"{prefix}test_board_update")

    count_mined = 0
    count_flagged = 0
    nr_scenarios = 1

    for i in range(nr_scenarios):

        print(f'\n\nIteration: {i}')

        # Init
        board = get_test_board()
        reset_game(board)

        flag = str(random.randint(0, 1))
        x = str(random.randint(0, self.board.rows-1))
        y = str(random.randint(0, self.board.cols-1))
        cell_name = f'{x}_{y}'


        # Update
        #self.board.update_game(cell_name, flag)
        #print()

        # Cell
        #cell = self.board.get_cell_name(cell_name)
        #if self.verbose:            
        #    print(cell)
        #    print(f'State SM:{self.board.state_sm}')
        #    print(f'Flag: {flag}')

        # Assert cell
        #if flag == '0':
            #self.assertIn(cell.label, ['-1', '0', '1', '2', '3', '4', '5', '6', '7', '8'])
        #    self.assertIn(cell.label, ['-1', '.', '1', '2', '3', '4', '5', '6', '7', '8'])
        #    self.assertEqual(cell.visible, True)
        #    self.assertEqual(cell.flagged, False)

        # Flag
        #elif flag == '1':
        #    count_flagged += 1
        #    self.assertIn(cell.label, ['-1', '.', '0', '1', '2', '3', '4', '5', '6', '7', '8'])
        #    self.assertEqual(cell.visible, False)
        #    self.assertEqual(cell.flagged, True)

        # value
        #self.assertIn(cell.value, [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8])

        # Assert mined
        #if cell.mined:
        #    count_mined += 1
        #    if not cell.flagged:
        #        self.assertEqual(self.board.state_sm, 4)
        #    else:
        #        self.assertEqual(self.board.state_sm, 1)

    if verbose:            
        print(f'\n\nRandom test was run: {nr_scenarios} times.')
        print(f'Was mined: {count_mined} times.')
        print(f'Was flagged: {count_flagged} times.')
