from django.contrib import admin
from .models import Cell, Board

# Register your models here.
class CellAdmin(admin.ModelAdmin):
    list_display = ("name", "x", "y", "value")

class BoardAdmin(admin.ModelAdmin):
    list_display = ("name", "rows", "cols", "mines")

admin.site.register(Cell, CellAdmin)
admin.site.register(Board, BoardAdmin)
