#!/usr/bin/env python3
import itertools
from datetime import tzinfo, timedelta, datetime, timezone
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from django_fsm import transition, FSMIntegerField, TransitionNotAllowed
from . import ms_engine as ms

# FSM
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
) 

# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=16)
    rows = models.IntegerField(default=1)
    cols = models.IntegerField(default=1)
    nr_mines = models.IntegerField(default=1)
    nr_hidden = models.IntegerField(default=0)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(default=timedelta(minutes=0), blank=True)
    state_sm = FSMIntegerField(choices=STATE_CHOICES, default=STATE_CREATED)
    numbers = ArrayField(ArrayField(models.IntegerField()))
    apparent = ArrayField(ArrayField(models.IntegerField()))
    flags = ArrayField(ArrayField(models.IntegerField()))
    mines = ArrayField(ArrayField(models.IntegerField()))
    game_over = models.BooleanField(default=False)
    game_win = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    # new
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('created_at', )

    def __str__(self):
        return f"{self.name}"

    
#-------------------------------------------------------------------------------
    # Play
    @transition(field=state_sm, source=[STATE_CREATED, STATE_PAUSED], target=STATE_STARTED)
    def play_sm(self):
        print('*** fsm - play_sm')

    # End win
    @transition(field=state_sm, source=STATE_STARTED, target=STATE_END_WIN)
    def end_win_sm(self):
        print('*** fsm - end_win_sm')

    # End loose
    @transition(field=state_sm, source=STATE_STARTED, target=STATE_END_LOOSE)
    def end_loose_sm(self):
        print('*** fsm - end_loose_sm')

    # Pause
    @transition(field=state_sm, source=STATE_STARTED, target=STATE_PAUSED)
    def pause_sm(self):
        print('*** fsm - pause_sm')

    # Reset
    @transition(field=state_sm, source='*', target=STATE_CREATED)
    def reset_sm(self):
        print('*** fsm - reset_sm')

    # Helpers
    def can_end_win(self):
        return not(self.state_sm == 3)

    def can_end_loose(self):
        return not(self.state_sm == 4)


#---------------------------------- Getters ------------------------------------
    def get_duration(self):
        return str(self.duration).split('.')[0]

    def get_user(self):
        return self.user.username.capitalize() if self.user else None

    def get_state(self):
        return STATE_CHOICES[self.state_sm][1].capitalize()


#-------------------------------------------------------------------------------
    def get_cells(self):
        """
        Get cells
        """
        count = Cell.objects.filter(board=self.id).count()
        if count != self.get_nr_cells():    
            print('Cleaning cells')
            cells = Cell.objects.filter(board=self.id).order_by('name')
            for cell in cells:
                cell.delete()
            print('\n\n***Creating cells !!!\n\n')
            for x in range(self.rows):
                for y in range(self.cols):
                    c = Cell(id=None, name=f'{x}_{y}', x=x, y=y, value='0', label='', visible=False, mined=False, flagged=False, board=self)
                    c.save()
        cells = Cell.objects.filter(board=self.id).order_by('name')
        return cells

    def get_cell(self, x, y):
        """
        Get cell
        """
        cell = Cell.objects.get(board=self.id, x=x, y=y)
        return cell

    def get_cell_name(self, name):
        """
        Get cell by name
        """
        cell = Cell.objects.get(board=self.id, name=name)
        return cell

    def get_nr_cells(self):
        count = self.rows * self.cols
        return count

    def not_cell_flagged(self, x, y):
        return [x, y] not in self.flags
        
    def not_cell_displayed(self, x, y):
        return self.apparent[x][y] == None

    def nr_cells_visible(self):
        cells = self.get_cells()
        count = 0
        for cell in cells:
            if cell.visible:
                count += 1
        return count

    def nr_cells_hidden(self):
        cells = self.get_cells()
        count = 0
        for cell in cells:
            if not cell.visible:
                count += 1
        return count

    def cells_update(self, game_over, game_win):
        cells = Cell.objects.filter(board=self.id).order_by('name')
        for cell in cells:
            cell.game_over = game_over
            cell.success = game_win
            cell.save()

#-------------------------------------------------------------------------------
    def nr_flags_ok(self, x, y):
        #return len(self.flags) < self.nr_mines
        return True

    def flagging_ok(self, x, y):
        return self.not_cell_flagged(x, y) and self.not_cell_displayed(x, y) and self.nr_flags_ok(x, y)
        
    def short_win(self):
        """
        Win condition - 1
        """
        self.flags.sort()
        return self.flags == self.mines

    def fast_win(self):
        """
        Win condition - 2
        """
        return self.nr_cells_hidden() == self.nr_mines

    def mined_defeat(self, cell):
        """
        Mined - Game over
        """
        return cell.mined and cell.visible


#-------------------------------------------------------------------------------
    def reset_cells(self):
        """
        Reset cells
        """
        print('reset_cells')
        cells = self.get_cells()
        for cell in cells:
            cell.value = 0
            cell.label = ''
            cell.mined = False
            cell.visible = False
            cell.flagged = False       
            cell.game_over = False
            cell.success = False

            cell.empty = False
            #cell.empty = True

            cell.save()


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
    def init_game(self):
        """
        Called by views.py
        Data
            numbers - The actual values of the grid
            apparent - The apparent values of the grid (shown to the player)
            flags - The positions that have been flagged
            mines - The positions that have been mined
        """
        print('*** init_game')

        # Reset
        self.reset_cells()

        # Init 
        self.game_over = False
        self.game_win = False
        self.nr_hidden = self.rows * self.cols
        self.start = datetime.now(timezone.utc)
        self.duration = timedelta(minutes=0)

        # Only square boards, for the moment
        n = self.rows

        # The positions that have been flagged
        self.flags = []

        #The actual values of the grid
        self.numbers = [[0 for y in range(n)] for x in range(n)]

        #The apparent values of the grid
        self.apparent = [[None for y in range(n)] for x in range(n)]

        # Set the mines
        nr_mines = self.nr_mines
        self.numbers = ms.set_mines(n, self.numbers, nr_mines)

        # Set the actual values
        self.numbers = ms.set_values(n, self.numbers)

        # The positions that have been mined
        self.mines = []
        for x in range(self.rows):
            for y in range(self.cols):
                value = self.numbers[x][y]
                if value == -1:
                    self.mines.append([x, y])

        self.save()


        # Reset
        #self.reset_cells()

        # Initialize the board
        cells = self.get_cells()
        for cell in cells:
            x = cell.x
            y = cell.y
            value = self.numbers[x][y]
            cell.value = value
            cell.label = str(value)
            cell.visible = False 
            if self.numbers[x][y] == -1:
                cell.mined = True
            cell.flagged = False

            if value == 0:
                cell.empty = True 

            cell.game_over = False
            cell.success = False
            cell.save()

        #print('Mines')
        #print(self.mines)


#-------------------------------------------------------------------------------
    def check_game(self, cell_name):
        print('*** check_game')
        # Check 
        cell = self.get_cell_name(cell_name)
        if cell.mined and self.nr_cells_visible() == 0 :
            print('Re-init the game !!!')
            self.init_game()
            self.save()


#-------------------------------------------------------------------------------
    def update_game(self, cell_name, flag):
        """
        Called by grid.js

        Actions:
            clicked cell is rendered visible,
            if value is equal to zero, adjacent cells also.
        """
        print('*** update_game')
        #print(f'cell_name: {cell_name}')
        #print(f'flag: {flag}')

        # Init
        cell = self.get_cell_name(cell_name)
        x = cell.x
        y = cell.y


        # Flag cell
        if flag == '1':
            print('** Flag cell')

            # Check if flagging ok
            if self.flagging_ok(x, y):
                print('** Flagging ok')
                cell = self.get_cell(x, y)
                self.flags.append([x, y])
                cell.flagged = True     # Set cell for flag display
                #cell.label = '?'
                cell.save()
                self.save()

            elif not cell.visible:
                print('** Unflag')
                cell = self.get_cell(x, y)
                self.flags.remove([x, y])
                cell.flagged = False
                cell.visible = False
                #cell.label = 'u'
                cell.save()
                self.save()


        # Analyse cell
        elif not cell.flagged:

            # Render the cell visible
            cell.visible = True
            self.apparent[x][y] = self.numbers[x][y]
            self.save()
            cell.save()

                
            # If landing on a cell with 0 mines in neighboring cells
            if cell.value == 0:
                # Init
                vis = []
                self.apparent[x][y] = 0
                n = self.rows
                # Looks for adjacent cells that can be cleared - Recursive
                ms.neighbours(n, x, y, vis, self.apparent, self.numbers)

                # Update cells
                # Avoid nested loops 
                for x, y in itertools.product( list(range(self.rows)), list(range(self.cols)) ):
                    value = self.apparent[x][y]
                    if value != None:
                        cell = self.get_cell(x, y)
                        cell.visible = True
                        if value == 0:
                            cell.label = '.'
                            cell.empty = True
                        else:
                            cell.label = str(value)
                        cell.value = self.apparent[x][y]
                        cell.save()


        # Check win conditions
        cell = self.get_cell_name(cell_name)

        # Game over - loose
        if self.mined_defeat(cell):
            self.game_over = True
            self.game_win = False

            # FSM - loose
            if self.can_end_loose():
                print(self.state_sm)
                self.end_loose_sm()
                print(self.state_sm)
                self.save()

        # Game over - win
        elif (self.short_win() or self.fast_win()):
            self.game_over = True
            self.game_win = True

            # FSM - win 
            if self.can_end_win():
                print(self.state_sm)
                self.end_win_sm()
                print(self.state_sm)
                self.save()

        # Not game over - continue
        else:
            self.game_over = False
            self.game_win = False
            cell.success = False


        # Stats
        self.nr_hidden = self.nr_cells_hidden()
        if self.start == None:
             self.start = datetime.now(timezone.utc)
        self.duration = datetime.now(timezone.utc).replace(microsecond=0) - self.start.replace(microsecond=0)
        self.end = datetime.now(timezone.utc)

        cell.save()
        self.save()

        # Update all cells
        self.cells_update(self.game_over, self.game_win)


#-------------------------------------------------------------------------------
class Cell(models.Model):
    name = models.CharField(max_length=16)
    x = models.IntegerField()
    y = models.IntegerField()

    value = models.IntegerField()
    label = models.CharField(max_length=10, default='', blank=True, null=True)

    visible = models.BooleanField(default=False)
    mined = models.BooleanField(default=False)
    flagged = models.BooleanField(default=False)
    empty = models.BooleanField(default=False)

    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    game_over = models.BooleanField(default=False)
    success = models.BooleanField(default=False)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return f"Cell -> name: {self.name}, x: {self.x}, y: {self.y}, value: {self.value}, label: {self.label}, visible: {self.visible}, mined: {self.mined}, flagged: {self.flagged}"
