from rest_framework import serializers
from django.contrib.auth.models import User, Group
from django.contrib.postgres.fields import ArrayField
from .models import Board, Cell
from django.db import models

#class BoardSerializer(serializers.HyperlinkedModelSerializer):
#    class Meta:
#        model = Board
#       fields = ['id', 'name', 'rows', 'cols', 'nr_hidden', 'nr_mines', 'numbers', 'apparent', 'mines', 'flags', 'start', 'end', 'duration', 'game_over', 'game_win', 'state_sm']

class BoardSerializer(serializers.Serializer):
    """
    A more explicit serializer
    """
    id = serializers.IntegerField(read_only=True)

    name = serializers.CharField(required=True, max_length=16)

    rows = serializers.IntegerField(default=5)
    cols = serializers.IntegerField(default=5)
    nr_hidden = serializers.IntegerField(default=25)
    nr_mines = serializers.IntegerField(default=3)
    state_sm = serializers.IntegerField(default=0)

    game_over = serializers.BooleanField(required=False)
    game_win = serializers.BooleanField(required=False)

    start = serializers.DateTimeField(required=False)
    end = serializers.DateTimeField(required=False)
    created_at = serializers.DateTimeField(required=False)
    updated_at = serializers.DateTimeField(required=False)
    duration = serializers.DurationField(default="0")

    #numbers = ArrayField(ArrayField(serializers.IntegerField()))
    #apparent = ArrayField(ArrayField(serializers.IntegerField()))
    #flags = ArrayField(ArrayField(serializers.IntegerField()))
    #mines = ArrayField(ArrayField(serializers.IntegerField()))
    #user = serializers.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def create(self, validated_data):
        """
        Create and return a new `Board` instance, given the validated data.
        """
        return Board.objects.create(**validated_data)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    'User Simple serializer'
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class CellSerializer(serializers.HyperlinkedModelSerializer):
    'Cell Simple serializer'
    class Meta:
        model = Cell
        fields = ['name', 'value', 'label', 'visible', 'mined', 'flagged', 'game_over', 'success']

#class GroupSerializer(serializers.HyperlinkedModelSerializer):
#    'Group Simple serializer'
#    class Meta:
#        model = Group
#        fields = ['url', 'name']
