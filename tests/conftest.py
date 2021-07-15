"""
Pytest 
Fixture
Creates new users and boards
"""
import pytest  
from django.contrib.auth.models import User
from datetime import timedelta, datetime, timezone
from django_fsm import FSMIntegerField
from minesweeper.models import Board

# User -------------------------------------------------------------------------
@pytest.fixture()
def user_1(db):
    """
    Method 1 - Simple
    """
    user =  User.objects.create_user('test-user')
    return user 

@pytest.fixture
def new_user_factory(db):
    """
    Method 2 - Using factories
    """
    def create_app_user(    # inner function 
        username: str, 
        password: str = None, 
        first_name: str = 'first name', 
        last_name: str = 'last name', 
        email: str = 'test@test.com', 
        is_staff: str = False, 
        is_superuser: str = False, 
        is_active:str = True, 
    ):
        user = User.objects.create_user(
            username = username, 
            password = password, 
            first_name = first_name, 
            last_name = last_name, 
            email = email, 
            is_staff = is_staff, 
            is_superuser = is_superuser, 
            is_active = is_active, 
        )
        return user 
    return create_app_user 

@pytest.fixture
def new_user(db, new_user_factory):
    return new_user_factory('Test User', 'password', 'MyName')


# Board ------------------------------------------------------------------------
@pytest.fixture
def new_board_factory(db):
    """
    Method 2 - Using factories
    """
    def create_app_board(    # inner function 
        name: str, 
        rows: int = 7, 
        cols: int = 7, 
        nr_mines: int = 3, 
        nr_hidden: int = 0, 
        start: datetime = False, 
        end: datetime = False, 
        duration:timedelta = True, 
        state_sm: FSMIntegerField = 0, 
        numbers = [0], 
        apparent = [0], 
        flags = [0], 
        mines = [0], 
        game_over: int = 0, 
        game_win: int = 0, 
        #user: User, 
        #created_at: str, 
        #updated_at: str, 
    ):
        board = Board.objects.create(
            name = name, 
            rows = rows, 
            cols = cols, 
            nr_mines = nr_mines, 
            nr_hidden = nr_hidden, 
            numbers = numbers, 
            apparent = apparent, 
            flags = flags, 
            mines = mines, 
            game_over = game_over, 
            game_win = game_win, 
        )
        return board 
    return create_app_board 


@pytest.fixture
def board(db, new_board_factory):
    return new_board_factory('Test board')
