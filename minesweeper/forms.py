from django import forms
from minesweeper.models import Board

#------------------------------------ Forms ------------------------------------
class BoardForm(forms.ModelForm):
    """
    Used by: edit 
    """
    class Meta:
        """
        Meta
        """
        model = Board
        fields = ['id', 'name', 'rows', 'nr_mines']
    id = forms.IntegerField()
    name = forms.CharField(max_length=16)
    rows = forms.IntegerField(min_value=0)
    nr_mines = forms.IntegerField(min_value=0)

class NewBoardForm(forms.Form):
    """
    Used by: update 
    """
    id = forms.IntegerField()
    name = forms.CharField(max_length=16)
    rows = forms.IntegerField()
    nr_mines = forms.IntegerField()
