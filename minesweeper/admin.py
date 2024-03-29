from django.contrib import admin
from .models import Cell, Board

# Register your models here.
class CellAdmin(admin.ModelAdmin):
    list_display = ("name", "x", "y", "value", "board")

class BoardAdmin(admin.ModelAdmin):
    #list_display = ("name", "user", "rows", "cols", "nr_mines", "start", "end", "duration", "state_sm", "get_nr_cells")
    list_display = ("name", "user", "rows", "cols", "nr_mines", "start", "end", "duration", "state_sm")

admin.site.register(Board, BoardAdmin)
admin.site.register(Cell, CellAdmin)
