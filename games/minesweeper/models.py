#!/usr/bin/env python3
from datetime import tzinfo, timedelta, datetime, timezone
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django_fsm import transition, FSMIntegerField
from . import ms_engine as ms

# FSM
STATE_CREATED = 0
STATE_STARTED = 1
STATE_PAUSED = 2
STATE_ENDED = 3

STATE_CHOICES = (
        (STATE_CREATED, 'created'),
        (STATE_STARTED, 'started'),
        (STATE_ENDED, 'ended'),
        (STATE_PAUSED, 'paused'),
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

    state_sm = FSMIntegerField(choices=STATE_CHOICES, default=STATE_CREATED, protected=True)

    numbers = ArrayField(ArrayField(models.IntegerField()))
    apparent = ArrayField(ArrayField(models.IntegerField()))
    flags = ArrayField(ArrayField(models.IntegerField()))
    mines = ArrayField(ArrayField(models.IntegerField()))
    game_over = models.BooleanField(default=False)
    game_win = models.BooleanField(default=False)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return f"{self.name}"

    
#-------------------------------------------------------------------------------
    # Play
    @transition(field=state_sm, source=[STATE_CREATED, STATE_PAUSED], target=STATE_STARTED)
    def play_sm(self):
        print('** fsm - play_sm')
        print(self.state_sm)
        self.save()

    # End
    @transition(field=state_sm, source=STATE_STARTED, target=STATE_ENDED)
    def end_sm(self):
        print('** fsm - end_sm')
        print(self.state_sm)
        self.save()

    # Pause
    @transition(field=state_sm, source=STATE_STARTED, target=STATE_PAUSED)
    def pause_sm(self):
        print('** fsm - pause_sm')
        print(self.state_sm)
        self.save()


    # Reset
    @transition(field=state_sm, source=[STATE_STARTED, STATE_PAUSED, STATE_CREATED, STATE_ENDED], target=STATE_CREATED)
    def reset_sm(self):
        print('** fsm - reset_sm')
        print(self.state_sm)
        self.save()


#-------------------------------------------------------------------------------
    def reset_game(self):
        print('reset_game')
        self.start = None
        self.end = None
        self.duration = timedelta(0)
        self.game_over = False
        self.game_win = False
        self.save()

#-------------------------------------------------------------------------------
    def get_state(self):
        print(self.state_sm)
        return self.state_sm.capitalize()

    def update_duration(self, duration):
        print('*** update_duration')
        print(duration)
        self.duration = timedelta(milliseconds=int(duration))
        self.save()

    def get_duration(self):
        print(self.duration)
        duration = str(self.duration).split('.')[0]
        return duration


#-------------------------------------------------------------------------------
    def get_nr_cells(self):
        #count = Cell.objects.filter(board=self.id).count()
        count = self.rows * self.cols
        return count

    def get_cells(self):
        """
        Get cells
        """
        print('get_cells')
        count = Cell.objects.filter(board=self.id).count()
        print(count)
        print(self.get_nr_cells())

        #if Cell.objects.filter(board=self.id).count() == 0:
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

    def reset_cells(self):
        """
        Reset
        """
        cells = self.get_cells()
        for cell in cells:
            cell.value = 0
            cell.label = ''
            cell.mined = False
            cell.visible = False
            cell.flagged = False       
            cell.success = False
            cell.save()

#-------------------------------------------------------------------------------
    def not_cell_flagged(self, x, y):
        return [x, y] not in self.flags
        
    def not_cell_displayed(self, x, y):
        return self.apparent[x][y] == None

    def nr_flags_ok(self, x, y):
        return len(self.flags) < self.nr_mines

    def flagging_ok(self, x, y):
        return self.not_cell_flagged(x, y) and self.not_cell_displayed(x, y) and self.nr_flags_ok(x, y)

    def nr_cells_hidden(self):
        cells = self.get_cells()
        count = 0
        for cell in cells:
            if not cell.visible:
                count += 1
        return count
        
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
    def init_game(self):
        """
        Called by views.py
        Data
            numbers - The actual values of the grid
            apparent - The apparent values of the grid (shown to the player)
            flags - The positions that have been flagged
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

        # Initialize the board
        cells = self.get_cells()
        for cell in cells:
            x = cell.x
            y = cell.y
            value = self.numbers[x][y]
            cell.value = value
            cell.label = str(value)
            if self.numbers[x][y] == -1:
                cell.mined = True
            cell.flagged = False
            cell.success = False
            cell.save()


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
        #print()

        # Init
        cell = self.get_cell_name(cell_name)
        x = cell.x
        y = cell.y

        # Flag cell
        if flag == '1':
            print('*** Flag cell')
            print(self.flags)
            # Check if flagging ok
            if self.flagging_ok(x, y):
                print("Set Flag")
                cell = self.get_cell(x, y)
                self.flags.append([x, y])
                cell.flagged = True     # Set cell for flag display
                cell.label = '?'
                cell.save()
                self.save()

        # Cell not flagged
        else:
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
                for x in range(self.rows):
                    for y in range(self.cols):
                        value = self.apparent[x][y]
                        if value != None:
                            cell = self.get_cell(x, y)
                            cell.visible = True
                            if value == 0:
                                cell.label = '.'
                            else:
                                cell.label = str(value)
                            cell.value = self.apparent[x][y]
                            cell.save()


        # Check win conditions
        cell = self.get_cell_name(cell_name)

        if (self.short_win() or self.fast_win()) and not self.mined_defeat(cell):
            self.game_over = True
            self.game_win = True
            cell.success = True
        else:
            cell.success = False

        if self.mined_defeat(cell):
            self.game_over = True
            self.game_win = False


        # Game ends
        if self.game_over:
            self.end = datetime.now(timezone.utc)
            self.end_sm()


        # Stats
        self.nr_hidden = self.nr_cells_hidden()
        if self.start == None:
             self.start = datetime.now(timezone.utc)
        self.duration = datetime.now(timezone.utc).replace(microsecond=0) - self.start.replace(microsecond=0)

        self.save()
        cell.save()


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
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    success = models.BooleanField(default=False)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return f"Cell: {self.name}, {self.x}, {self.y}, {self.value}, {self.visible}, {self.mined}, {self.flagged}"
