from datetime import timedelta
from django.db import models
from django.utils import timezone

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
    start = models.DateTimeField(auto_now_add=True, blank=True)
    end = models.DateTimeField(blank=True, null=True)
    duration = models.DurationField(default=timedelta(minutes=0), blank=True)
    nr_hidden_cells = models.IntegerField(blank=True, null=True)
    state = models.CharField(max_length=16, choices=BOARD_CHOICES, default='BEGIN')

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


    # Calc board
    def calc(self, cmd, cell_name=None):
        import random
        print('*** calc')
        print(cmd)
        print(cell_name)
        cells = Cell.objects.filter(board=self.id)

        # Init - called by views.play
        if cmd == 'init':
            print('** init')
            names = []
            for cell in cells:
                names.append(cell.name)
            mined_cells = random.sample(names, self.rows-1)
            print(mined_cells)
            for cell in cells:
                cell.name = f'{cell.x}_{cell.y}'
                cell.visible = False
                cell.mined = False
                cell.value = 0
                if cell.name in mined_cells:
                    cell.mined = True
                cell.save()


        # Update - called by grid.js
        if cmd == 'update':
            print('** update')
            count = None

            for cell in cells:
                # Clicked cell - must have side effects
                if cell.name == cell_name:
                    cell.visible = True
                    count = self.count_adjacent_mines(cell.x, cell.y)
                    cell.value = count
                    cell.save()

            #  This must be recursive
            if count == 0:
                print('*** RE - EXPLORE !!!')
                #self.clear_around(cell.x, cell.y)


    # Count adjacent mines
    def count_adjacent_mines(self, x0, y0):
        print('count_adjacent_mines')
        count = 0

        for x in range(x0-1, x0+2):
            for y in range(y0-1, y0+2):
                if (x > -1 and x < self.cols) and (y > -1 and y < self.rows):
                    if not (x == x0 and y == y0):
                        name = f'{x}_{y}'
                        print(name)
                        cell = Cell.objects.get(board=self.id, name=name)
                        print(cell)

                        if cell.mined:
                            count += 1
        return count


    # Clear around - Must be recursive
    def clear_around(self, x0, y0):
        print('clear_around')
        for x in range(x0-1, x0+2):
            for y in range(y0-1, y0+2):
                if (x > -1 and x < self.cols) and (y > -1 and y < self.rows):
                    if not (x == x0 and y == y0):
                        name = f'{x}_{y}'
                        print(name)
                        cell = Cell.objects.get(board=self.id, name=name)
                        print(cell)
                        cell.visible = True
                        cell.save()




class Cell(models.Model):
    name = models.CharField(max_length=16)
    x = models.IntegerField()
    y = models.IntegerField()
    value = models.IntegerField(default=0)
    visible = models.BooleanField(default=False)
    mined = models.BooleanField(default=False)
    flagged = models.BooleanField(default=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):
        #return f"Cell: {self.name}, {self.x}, {self.y}, {self.value}, {self.hidden}, {self.mined}, {self.flagged}"
        return f"Cell: {self.name}, {self.x}, {self.y}, {self.value}, {self.visible}, {self.mined}, {self.flagged}"

