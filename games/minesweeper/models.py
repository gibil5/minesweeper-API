from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
from . import ms_engine as ms
#from django.contrib.postgres.fields import JSONField

BOARD_CHOICES = (
    ("BEGIN", "Begin"),
    ("IN_PROGRESS", "In progress"),
    ("PAUSE", "Pause"),
    ("END", "End"),
)

# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=16)
    rows = models.IntegerField(default=1)
    cols = models.IntegerField(default=1)
    mines = models.IntegerField(default=1)
    #nr_hidden_cells = models.IntegerField(blank=True, null=True)
    start = models.DateTimeField(auto_now_add=True, blank=True)
    end = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(default=timedelta(minutes=0), blank=True)
    state = models.CharField(max_length=16, choices=BOARD_CHOICES, default='BEGIN')
    #numbers = JSONField()
    #numbers = models.JSONField(null=True, blank=True)
    numbers = ArrayField(ArrayField(models.IntegerField()))
    apparent = ArrayField(ArrayField(models.IntegerField()))

    class Meta:
        #ordering = ('-start', )
        ordering = ('name', )

    def __str__(self):
        #return f"Board: {self.name}, {self.rows} rows, {self.cols} cols, {self.mines} mines, {self.nr_hidden_cells} hidden, {self.state}, {timezone.localtime(self.start)}, {timezone.localtime(self.end)}, {self.duration}"
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
                    #c = Cell(id=None, name=f'{x}_{y}', x=x, y=y, value='0', visible=False, mined=False, flagged=False, board=self)
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
            #cell.value = '0'
            cell.value = 0
            cell.label = ''
            cell.mined = False 
            cell.visible = False
            cell.save()

#-------------------------------------------------------------------------------
    def init_game(self):
        """
        Called by views.py

        The actual values of the grid
            numbers
            
        The apparent values of the grid (shown to the player)
            apparent

        The positions that have been flagged
            flags
        """
        print('\n\ninit_game')

        # Reset
        self.reset_cells()

        # Init - only square boards, for the moment
        n = self.rows

        #The actual values of the grid    
        self.numbers = [[0 for y in range(n)] for x in range(n)] 

        #The apparent values of the grid
        #self.apparent = [[0 for y in range(n)] for x in range(n)]
        #self.apparent = [[9 for y in range(n)] for x in range(n)]
        self.apparent = [[None for y in range(n)] for x in range(n)]

        # Set the mines
        nr_mines = self.mines
        self.numbers = ms.set_mines(n, self.numbers, nr_mines)

        # Set the actual values
        self.numbers = ms.set_values(n, self.numbers)

        #print()
        #print(self.numbers)
        #print(self.apparent)
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
            cell.save()



    def update_game(self, cell_name, flag):
        """
        Called by grid.js

        Actions:
            clicked cell is rendered visible,
            if value is equal to zero, adjacent cells also.
        """
        print('** update_game')
        print(cell_name)
        print(flag)
        print()

        # Init
        cell = self.get_cell_name(cell_name)

        # Render the cell visible
        cell.visible = True
        x = cell.x
        y = cell.y
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
            #print()
            #print(self.apparent)
            #print()
            #print(vis)
            #print()

            # Update cells
            for x in range(self.rows):
                for y in range(self.cols):
                    value = self.apparent[x][y]
                    #if self.apparent[x][y] != None:
                    #if self.apparent[x][y] != 9:
                    #if value != 9:
                    if value != None:
                        cell = self.get_cell(x, y)
                        cell.visible = True
                        if value == 0:
                            cell.label = ''
                        else:
                            cell.label = str(value)
                        cell.value = self.apparent[x][y]
                        cell.save()

            # The positions that have been flagged
            #flags = []

        
#-------------------------------------------------------------------------------    
class Cell(models.Model):
    name = models.CharField(max_length=16)

    x = models.IntegerField()
    y = models.IntegerField()

    #value = models.CharField(max_length=10, default=None)
    #value = models.IntegerField(default=0)
    value = models.IntegerField()
    label = models.CharField(max_length=10, default='', blank=True, null=True)

    visible = models.BooleanField(default=False)
    mined = models.BooleanField(default=False)
    flagged = models.BooleanField(default=False)

    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    class Meta:
        #ordering = ('-start', )
        ordering = ('name', )

    def __str__(self):
        #return f"Cell: {self.name}, {self.x}, {self.y}, {self.value}, {self.hidden}, {self.mined}, {self.flagged}"
        return f"Cell: {self.name}, {self.x}, {self.y}, {self.value}, {self.visible}, {self.mined}, {self.flagged}"

