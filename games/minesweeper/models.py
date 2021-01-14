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


class Cell(models.Model):
    name = models.CharField(max_length=16)
    x = models.IntegerField()
    y = models.IntegerField()
    value = models.IntegerField()   # 1 to 8
    hidden = models.BooleanField()
    mined = models.BooleanField()
    flagged = models.BooleanField()
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cell: {self.name}, {self.x}, {self.y}, {self.value}, {self.hidden}, {self.mined}, {self.flagged}"

