#!/usr/bin/env python3
"""
The classic game of Minesweeper
A RESTful API

Specs
-------
- Design and develop a documented RESTful API.
- Implement an API client, using a frontend language, ie Javascript.
- The UI must be optimized for a mobile device user, it must be responsive. 
- When a cell with no adjacent mines is revealed, all adjacent cells will be revealed, and repeat.
  This requires a recursive solution.
- Ability to "flag" a cell with a question mark or a red flag.
- Detect when the game is over.
- Persistence.
- Time tracking.
- Ability to start a new game and preserve/resume the old ones.
- Ability to select the game parameters: number of rows, columns, and mines.
- Ability to support multiple users/accounts.

Algorithm
-----------
We have used the following article: 
"Create Minesweeper using Python From the Basic to Advanced". From the AskPython website

API Documentation
-------------------
https://minesweeper-api-jr.herokuapp.com/redoc 

"""
import itertools
from datetime import timedelta, datetime, timezone
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django_fsm import transition, FSMIntegerField
from minesweeper import ms_engine as ms
from minesweeper import funcs

# FSM (Finite state machine) - Init
STATE_CREATED = 0
STATE_STARTED = 1
STATE_PAUSED = 2
STATE_END_WIN = 3
STATE_END_LOOSE = 4
STATE_CHOICES = (
    (STATE_CREATED, 'init'),
    (STATE_STARTED, 'start'),
    (STATE_PAUSED, 'pause'),
    (STATE_END_WIN, 'end win'),
    (STATE_END_LOOSE, 'end lose'),
)   #pylint: disable=invalid-sequence-index


# Defaults ---------------------------------------------------------------------
def default_rows():
    return 7

def default_cols():
    return 7

def default_nr_hidden():
    return 49

def default_nr_mines():
    return 7

def default_matrix():
    return {}

def default_numbers():
    return 0

# Model ------------------------------------------------------------------------
class Board(models.Model):  #pylint: disable=too-many-instance-attributes
    """
    Game board
    Is a 2d matrix of Cells
    #Is owned by a User
    Is owned by a []
    """
    name = models.CharField(max_length=16)

    # Int
    rows = models.IntegerField(default=default_rows)
    cols = models.IntegerField(default=default_cols)
    nr_mines = models.IntegerField(default=default_nr_mines)
    nr_hidden = models.IntegerField(default=default_nr_hidden)
    state_sm = FSMIntegerField(choices=STATE_CHOICES, default=STATE_CREATED)

    # Boolean
    game_over = models.BooleanField(default=False)
    game_win = models.BooleanField(default=False)

    # Dates
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    duration = models.DurationField(default=timedelta(minutes=0), blank=True)

    # User
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    # Matrixes - Array of Array
    #numbers = ArrayField(ArrayField(models.IntegerField()))
    numbers = ArrayField(ArrayField(models.IntegerField(default=default_numbers)))
    apparent = ArrayField(ArrayField(models.IntegerField()))
    flags = ArrayField(ArrayField(models.IntegerField()))
    mines = ArrayField(ArrayField(models.IntegerField()))

    # Matrixes - Json
    matrix_numbers = models.JSONField(default=default_matrix)
    matrix_apparent = models.JSONField(default=default_matrix)
    matrix_mines = models.JSONField(default=default_matrix)
    matrix_flags = models.JSONField(default=default_matrix)


    class Meta: #pylint: disable=missing-class-docstring,too-few-public-methods
        ordering = ('created_at', )

    def __str__(self):
        return f"{self.name}"



# Used by template  ------------------------------------------------------------
    def get_nr_cells(self):
        """
        Used by template
        """
        return self.rows * self.cols

# FSM transitions --------------------------------------------------------------
    # Play
    @transition(field=state_sm, source=[STATE_CREATED, STATE_PAUSED], target=STATE_STARTED)
    def play_sm(self):  #pylint: disable=no-self-use
        print('\n*** fsm - play_sm')

    # End win
    @transition(field=state_sm, source=STATE_STARTED, target=STATE_END_WIN)
    def end_win_sm(self):   #pylint: disable=no-self-use
        print('*** fsm - end_win_sm')

    # End loose
    @transition(field=state_sm, source=STATE_STARTED, target=STATE_END_LOOSE)
    def end_loose_sm(self): #pylint: disable=no-self-use
        print('*** fsm - end_loose_sm')

    # Pause
    @transition(field=state_sm, source=STATE_STARTED, target=STATE_PAUSED)
    def pause_sm(self): #pylint: disable=no-self-use
        print('*** fsm - pause_sm')

    # Reset
    @transition(field=state_sm, source='*', target=STATE_CREATED)
    def reset_sm(self): #pylint: disable=no-self-use
        print('\n*** fsm - reset_sm')

    # Helpers
    def can_end_win(self):
        #return not self.state_sm == 3
        return self.state_sm != 3

    def can_end_loose(self):
        #return not self.state_sm == 4
        return self.state_sm != 4

    def get_state(self):
        return STATE_CHOICES[self.state_sm][1].capitalize()


# Cell funcs -------------------------------------------------------------------
    def get_cell(self, x, y):
        """
        Get cell by position
        """
        cell = Cell.objects.get(board=self.id, x=x, y=y)
        return cell

    def get_cell_by_name(self, name):
        """
        Get cell by name
        """
        cell = Cell.objects.get(board=self.id, name=name)
        return cell

    # Get cells
    def get_cells(self):
        """
        Get or create cells
        """
        print('* get_cells')
        count = Cell.objects.filter(board=self.id).count()
        nr_cells = self.rows * self.cols
        # Create if necessary
        if count != nr_cells:
            # Clean cells
            cells = Cell.objects.filter(board=self.id).order_by('name')
            for cell in cells:
                cell.delete()
            # Create cells
            for x, y in itertools.product(list(range(self.rows)), list(range(self.cols))):
                c = Cell(id=None, name=f'{x}_{y}', x=x, y=y, value='0', label='', visible=False, mined=False, flagged=False, board=self)
                c.save()
        # Get cells
        cells = Cell.objects.filter(board=self.id).order_by('name')
        return cells


# First level ------------------------------------------------------------------
    def init_game(self):
        """
        Called by views.py
        Data - Bidimensional arrays
            numbers - The actual values of the grid
            apparent - The apparent values of the grid (seen by the player)
            flags - The positions that have been flagged
            mines - The positions that have been mined
        Called by
            the fronted (grid.js),
            via the BoardUpdate.get_queryset() method in api_view.py
        """
        print('\n*** init_game')

        # Reset
        cells = self.get_cells()
        funcs.reset_cells(cells)

        # Init
        self.game_over = False
        self.game_win = False
        self.nr_hidden = self.rows * self.cols
        self.start = datetime.now(timezone.utc)
        self.duration = timedelta(minutes=0)
        n = self.rows   # Only square boards, for the moment

        # Bidimensional Arrays
        # ------------------------
        # The visible number on the board
        self.apparent = [[None for y in range(n)] for x in range(n)]        # Init

        # The actual numbers on the board
        self.numbers = [[0 for y in range(n)] for x in range(n)]            # Init
        self.numbers = ms.set_mines(self.numbers, self.nr_mines)            # Set the mines
        self.numbers = ms.set_values(self.numbers)     # Set the board values, which are calculated using the mines positions

        # Positions flagged
        self.flags = []

        # Positions mined
        self.mines = []

        for x, y in itertools.product(list(range(self.rows)), list(range(self.cols))):
            if self.numbers[x][y] == -1:
                self.mines.append([x, y])

        self.save()

        # Initialize the board
        cells = self.get_cells()
        funcs.init_cells(cells, self.numbers)
    # init_game


# Second level -----------------------------------------------------------------

    # Toggle flag
    def toggle_flag(self, cell):
        print('** Toggle cell')
        x = cell.x
        y = cell.y

        # Check if flagging ok
        if funcs.flagging_ok(self, x, y):
            print('** Flag cell')
            cell = self.get_cell(x, y)
            self.flags.append([x, y])
            cell.flagged = True     # Set cell for flag display
            cell.save()
            self.save()

        elif not cell.visible:
            print('** Unflag cell')
            cell = self.get_cell(x, y)
            self.flags.remove([x, y])
            cell.flagged = False
            cell.visible = False
            cell.save()
            self.save()
    # toggle_flag

    # Analyse and discover
    def analyse_and_discover(self, cell):
        print('** Analyse and discover cells')
        x = cell.x
        y = cell.y

        # Render the cell visible
        cell.visible = True
        self.apparent[x][y] = self.numbers[x][y]
        self.save()
        cell.save()

        # If landing on a cell with value equal to 0 (no mines in neighboring cells)
        if cell.value == 0:
            # Init
            vis = []
            self.apparent[x][y] = 0
            n = self.rows
            # Looks for adjacent cells that can be cleared - Recursive
            ms.neighbours(n, x, y, vis, self.apparent, self.numbers)

            # Update cells
            # Avoid nested loops
            for x, y in itertools.product(list(range(self.rows)), list(range(self.cols))):
                value = self.apparent[x][y]
                if value is not None:
                    cell = self.get_cell(x, y)
                    cell.visible = True
                    if value == 0:
                        cell.label = '.'
                        cell.empty = True
                    else:
                        cell.label = str(value)
                    cell.value = self.apparent[x][y]
                    cell.save()
    # analyse_and_discover

    # Check win conditions
    def check_win_conditions(self, cell):
        print('** Check win conditions')
        # Game over - Loose
        if funcs.mined_defeat(cell):
            self.game_over = True
            self.game_win = False
            # FSM - loose
            if self.can_end_loose():
                print(self.state_sm)
                self.end_loose_sm()
                print(self.state_sm)
                self.save()
        # Game over - Win
        elif (funcs.short_win(self) or funcs.long_win(self)):
            self.game_over = True
            self.game_win = True
            # FSM - win
            if self.can_end_win():
                print(self.state_sm)
                self.end_win_sm()
                print(self.state_sm)
                self.save()
        # Not game over - Continue
        else:
            self.game_over = False
            self.game_win = False
            cell.success = False
    # check_win_conditions

    # Build macro stats
    def buid_macro_stats(self):
        print('** Build macro stats')
        # self.nr_hidden = self.nr_cells_hidden()
        cells = self.get_cells()
        self.nr_hidden = funcs.nr_cells_hidden(cells)
        if self.start is None:
            self.start = datetime.now(timezone.utc)
        self.duration = datetime.now(timezone.utc).replace(microsecond=0) - self.start.replace(microsecond=0)
        self.end = datetime.now(timezone.utc)
    # buid_macro_stats


# First level ------------------------------------------------------------------
    def update_game(self, cell_name, flag):
        """
        Algorithm
            if flag Toggle
            else
                Analyse and discover
            Check win conditions
            Build Macro Stats
            Update all cells

        Bidimensional arrays (matrixes)
            numbers - The actual values of the grid
            apparent - The apparent values of the grid (seen by the player)
            flags - The positions that have been flagged
            mines - The positions that have been mined

        Actions:
            clicked cell is rendered visible,
            if value is equal to zero, adjacent cells also.

        Called by
            the fronted (grid.js),
            via the BoardUpdate.get_queryset() method in api_view.py
        """
        print('\n*** update_game')
        print(f'cell_name: {cell_name}')
        print(f'flag: {flag}')

        # Init
        cell = self.get_cell_by_name(cell_name)

        # Toggle Flag
        if flag == '1':
            self.toggle_flag(cell)

        # Analyse and discover cells
        else:
            self.analyse_and_discover(cell)

        # Check win conditions
        print('** Check win conditions')
        cell = self.get_cell_by_name(cell_name)
        self.check_win_conditions(cell)
        cell.save()

        # Build Macro Stats
        print('** Build Macro Stats')
        self.buid_macro_stats()
        self.save()

        # Update all cells
        cells = Cell.objects.filter(board=self.id).order_by('name')
        funcs.update_cells(cells, self.game_over, self.game_win)
    # update_game


# First level ------------------------------------------------------------------
    def check_game(self, cell_name):
        """
        Executed only once, at the beginning of the game.
        Checks the first cell chosen. If mined, restarts the game.
        """
        print('*** check_game')
        cell = self.get_cell_by_name(cell_name)
        cells = self.get_cells()
        # Check
        if cell.mined and funcs.nr_cells_visible(cells) == 0:
            print('Re-init the game !!!')
            self.init_game()
            self.save()
    # check_game


# Model ------------------------------------------------------------------------
class Cell(models.Model):
    """
    Cell
    Used by Board
    Board is a ForeignKey
    """
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    name = models.CharField(max_length=16)
    x = models.IntegerField()
    y = models.IntegerField()
    value = models.IntegerField()
    label = models.CharField(max_length=10, default='', blank=True, null=True)
    visible = models.BooleanField(default=False)
    mined = models.BooleanField(default=False)
    flagged = models.BooleanField(default=False)
    empty = models.BooleanField(default=False)
    game_over = models.BooleanField(default=False)
    success = models.BooleanField(default=False)

    class Meta: #pylint: disable=missing-class-docstring,too-few-public-methods
        ordering = ('name', )

    def __str__(self):
        return f"Cell -> name: {self.name}, x: {self.x}, y: {self.y}, value: {self.value}, label: {self.label}, visible: {self.visible}, mined: {self.mined}, flagged: {self.flagged}"
