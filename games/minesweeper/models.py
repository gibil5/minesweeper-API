from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField
#from django.contrib.postgres.fields import JSONField
from . import ms_engine as ms

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
    nr_hidden_cells = models.IntegerField(blank=True, null=True)

    start = models.DateTimeField(auto_now_add=True, blank=True)
    end = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(default=timedelta(minutes=0), blank=True)
    state = models.CharField(max_length=16, choices=BOARD_CHOICES, default='BEGIN')

    #numbers = JSONField()
    #numbers = models.JSONField(null=True, blank=True)

    #numbers = ArrayField(ArrayField(models.IntegerField(blank=True)))
    #numbers = ArrayField(ArrayField(models.IntegerField(blank=True)))
    #numbers = ArrayField(ArrayField(models.IntegerField(default=0, blank=True, null=True)))
    #numbers = ArrayField(
    #                    ArrayField(
    #                        models.IntegerField(default=list(list()), blank=True, null=True),
    #                        size=100,
    #                    ),
    #                    size=100,
    #                )

    #data = ArrayField(
    #    ArrayField(
    #        models.CharField(max_length=10, blank=True, default=''),
    #        size=100,
    #    ),
    #    size=100,
    #)

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


    def reset_cells(self):
        cells = self.get_cells()
        for cell in cells:
            cell.value = '0'
            cell.mined = False 
            cell.visible = False
            cell.save()
            

    def get_cells(self):
        if Cell.objects.filter(board=self.id).count() == 0:
            print('\n\n***Creating cells !!!\n\n')
            for x in range(self.rows):
                for y in range(self.cols):
                    c = Cell(id=None, name=f'{x}_{y}', x=x, y=y, value='0', visible=False, mined=False, flagged=False, board=self)
                    c.save()
            
        return Cell.objects.filter(board=self.id)


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
    #jx
    def init_game(self):
        """
        Inits game
        Called by views.py
        """
        self.reset_cells()

        # Init
        n = self.rows

        #The actual values of the grid    
        numbers = [[0 for y in range(n)] for x in range(n)] 

        # Set the mines
        nr_mines = self.mines
        numbers = ms.set_mines(n, numbers, nr_mines)


        # Set the values - Here !
        # an object member
        numbers = ms.set_values(n, numbers)


        print()
        print(numbers)

        # Init the board 
        cells = self.get_cells()
        for cell in cells:
            x = cell.x 
            y = cell.y
            cell.value = numbers[x][y]
            if numbers[x][y] == -1:
                cell.mined = True
            cell.save()


    def update_game(self, cell_name):
        """
        Called by grid.js
        Looks for the cell that has been clicked. 
        Actions:
            It is rendered visible. 
        """
        print('** update_game')
        
        cells = self.get_cells()
        
        # Init
        arr = []
        r = self.rows
        n = self.cols

        #The apparent values of the grid
        mine_values = [[' ' for y in range(n)] for x in range(n)]
        for cell in cells:
            if cell.name == cell_name:
                cell.visible = True
                cell.save()

                # If landing on a cell with 0 mines in neighboring cells
                if numbers[r][n] == 0:
                    pass
                    
                if cell.value == 0:
                    r = self.rows
                    vis = []
                    mine_values[r][n] = '0'

                    #ms.neighbours(r, col, vis, mine_values, numbers)

                    # The positions that have been flagged
                    #flags = []
                    #vis = []
        
        
        

#-------------------------------------------------------------------------------
    def update_nex(self, cell_name):
        """
        Dep !
        """
        print('** update_nex')
        cells = Cell.objects.filter(board=self.id)
        arr = []
        for cell in cells:
            if cell.name == cell_name:
                cell.visible = True
                cell.save()

                if cell.value == '0':
                    ms.get_empty_neighbors(cell.x, cell.y, arr, self.id, Cell)

        print(arr)
        if False:
            for tup in arr:
                x = tup[0]
                y = tup[1]
                try:
                    cell = Cell.objects.get(board=self.id, x=x, y=y)
                except:
                    print('error')
                else:            
                    #print('ok')
                    if cell.value == '0': 
                        cell.visible = True
                        cell.save()




    # Calc board
    def update(self, cell_name):
        """
        Dep !
        """
        print('** update')

        cells = Cell.objects.filter(board=self.id)
        #count = 1

        # Update - called by grid.js
        for cell in cells:
            if cell.name == cell_name:
                cell.visible = True
                cell.save()

                # Get adjacent empty cells
                if cell.value == '0':

                    # Horizontal
                    count_h = 1
                    solution_hor = []
                    if True:
                        #ms.explore_horizontal(cell, count_h, self.rows, self.cols, Cell, self.id, solution_hor, 0, 1)
                        ms.explore_all(cell, count_h, self.rows, self.cols, Cell, self.id, solution_hor, 0, 1)
                        print('****************')
                        print(solution_hor)
                        print('****************')

                    # Vertical
                    count_v = 1
                    solution_ver = []
                    if True:
                        #ms.explore_vertical(cell, count_v, self.rows, self.cols, Cell, self.id, solution_ver, 1, 0)
                        ms.explore_all(cell, count_v, self.rows, self.cols, Cell, self.id, solution_ver, 1, 0)
                        print('****************')
                        print(solution_ver)
                        print('****************')

        # Adjacent cells must be visible also
        for tup in solution_hor:
            x = tup[0]
            y = tup[1]
            cell = Cell.objects.get(board=self.id, x=x, y=y)
            cell.visible = True
            cell.save()

        for tup in solution_ver:
            x = tup[0]
            y = tup[1]
            cell = Cell.objects.get(board=self.id, x=x, y=y)
            cell.visible = True
            cell.save()



    # Calc engine
    def calc_engine(self):
        print('calc_engine')
        
        p = 0.1
        bombs, solution = ms.create_board(self.rows, self.cols, p)
        board = ms.clean(bombs, solution, self.rows, self.cols)
        print(board)

        
        cells = Cell.objects.filter(board=self.id)

        # init
        for cell in cells:
            cell.name = f'{cell.x}_{cell.y}'
            cell.visible = False
            cell.value = board[cell.x][cell.y]
            if cell.value == '*':
                cell.mined = True 
            else: 
                cell.mined = False 
            cell.save()
            #print(cell.name, cell.value, cell.x, cell.y)
            #print()


        # Check adherence
        #print('check adherence')
        #for cell in cells:
        #    if cell.value == '0':
        #        print('zero')
        #        print(cell.name)
        #        print()











class Cell(models.Model):
    name = models.CharField(max_length=16)
    x = models.IntegerField()
    y = models.IntegerField()

    #value = models.IntegerField(default=0)
    value = models.CharField(max_length=10, default=None)

    visible = models.BooleanField(default=False)
    mined = models.BooleanField(default=False)
    flagged = models.BooleanField(default=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):
        #return f"Cell: {self.name}, {self.x}, {self.y}, {self.value}, {self.hidden}, {self.mined}, {self.flagged}"
        return f"Cell: {self.name}, {self.x}, {self.y}, {self.value}, {self.visible}, {self.mined}, {self.flagged}"

