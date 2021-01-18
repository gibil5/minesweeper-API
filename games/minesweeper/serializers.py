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
        fields = ['id', 'name', 'rows', 'cols', 'mines', 'start', 'end', 'duration', 'nr_hidden_cells', 'state']

class CellSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Cell
        fields = ['name', 'value', 'visible', 'mined', 'flagged']
