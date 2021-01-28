#!/usr/bin/env python3
from datetime import tzinfo, timedelta, datetime, timezone
from django.db import models
from django.contrib.postgres.fields import ArrayField
from . import ms_engine as ms

BOARD_CHOICES = (
    ("created", "Created"),
    ("start", "Start"),
    ("pause", "Pause"),
    ("end", "End"),
)
# created, start, pause, end 


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
    state = models.CharField(max_length=16, choices=BOARD_CHOICES, blank=True, null=True)

    numbers = ArrayField(ArrayField(models.IntegerField()))
    apparent = ArrayField(ArrayField(models.IntegerField()))
    flags = ArrayField(ArrayField(models.IntegerField()))
    mines = ArrayField(ArrayField(models.IntegerField()))

    game_over = models.BooleanField(default=False)
    success = models.BooleanField(default=False)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return f"{self.name}"

    def get_nr_cells(self):
        count = Cell.objects.filter(board=self.id).count()
        return count

    def get_rows(self):
        arr = list(range(self.rows))
        return enumerate(arr)

    def get_cols(self):
        arr = list(range(self.cols))
        return enumerate(arr)

    def get_cells(self):
        """
        Get cells
        """
        if Cell.objects.filter(board=self.id).count() == 0:
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
        # Win condition - 1
        print('*** win condition 1')
        self.flags.sort()
        print(self.flags)
        print(self.mines)
        return self.flags == self.mines

    def long_win(self):
        # Win condition - 2
        print('*** win condition 2')
        print(self.nr_cells_hidden())            
        return self.nr_cells_hidden() == self.nr_mines

    def mined_defeat(self, cell):
        # Mined - Game over
        print('*** defeat condition 1')
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
        print('\n\ninit_game')

        # Reset
        self.reset_cells()

        # Init 
        self.game_over = False
        self.success = False
        self.nr_hidden = self.rows * self.cols
        self.start = datetime.now()
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
        print(self.mines)

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
        print('** update_game')
        print(f'cell_name: {cell_name}')
        print(f'flag: {flag}')
        print()

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
            print('*** manage cells')

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

        if (self.short_win() or self.long_win()) and not self.mined_defeat(cell):
            self.game_over = True
            self.success = True
            cell.success = True
        else:
            print('Not yet !!')
            cell.success = False
        
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
