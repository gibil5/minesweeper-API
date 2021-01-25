from django.contrib.auth.models import User, Group
from .models import Board, Cell
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class BoardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Board
        #fields = ['id', 'name', 'rows', 'cols', 'mines', 'start', 'end', 'duration', 'nr_hidden_cells', 'state']
        #fields = ['id', 'name', 'rows', 'cols', 'nr_mines', 'start', 'end', 'duration', 'state']
        fields = ['id', 'name', 'rows', 'cols', 'nr_mines', 'mines', 'flags', 'game_over', 'success']

class CellSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cell
        #fields = ['name', 'value', 'visible', 'mined', 'flagged']
        #fields = ['name', 'value', 'label', 'visible', 'mined', 'flagged']
        fields = ['name', 'value', 'label', 'visible', 'mined', 'flagged', 'success']