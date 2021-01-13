from django.db import models

# Create your models here.
class Cell(models.Model):
    name = models.CharField(max_length=16)

    x = models.IntegerField()
    y = models.IntegerField()
    value = models.IntegerField()   # 1 to 8

    hidden = models.BooleanField()
    mined = models.BooleanField()
    flagged = models.BooleanField()


    def __init__(self):
        print('Cell - init')

    def __str__(self):
        return f"Cell: {self.x}, {self.y}, {self.value}"


class Board(models.Model):
    name = models.CharField(max_length=16)
    rows = models.IntegerField()
    cols = models.IntegerField()
    mines = models.IntegerField()

    start = models.DateTimeField()
    end = models.DateTimeField()
    duration = models.DurationField()

    nr_hidden_cells = models.IntegerField()
    state = models.CharField(max_length=16)
    
    cells = models.ManyToManyField(Cell, blank=True)


    def __init__(self):
        print('Board - init')

    def __str__(self):
        return f"Board: {self.name}, {self.y}, {self.value}"

