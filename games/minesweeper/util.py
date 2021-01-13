#!/usr/bin/env python3
"""
Module Util
    Created:    28 dec 2020
    Last up:    11 jan 2021

Library for interaction with cells
"""
import re
from functools import wraps
from bs4 import BeautifulSoup
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from .models import Board 

# ------------------------------------------------------------------------------
#                              Entries
# ------------------------------------------------------------------------------
def list_boards():
    """
    Returns a list of boards.
    """
    #arr = ['1', '2', '3', '4', '5', '6']
    
    boards = Board.objects.all()

    #return list(sorted(arr))
    return boards


def get_board(name):
    board = Board.objects.filter(name=name)
    return board




