"""
Ms Engine
Engine for the Minesweeper game

Functions:
    set_mines
    set_values
    neighbours

Origin:
    "Create Minesweeper using Python From the Basic to Advanced"
    Ask Python web site
    https://www.askpython.com/python/examples/create-minesweeper-using-python
"""
import random
import itertools

#-------------------------------------------------------------------------------
def set_mines(numbers, nr_mines):
    """
    Data:
        Numbers is a square 2d Matrix
        n is the number of rows or cols
        nr_mines is the number of mines
    Description:
        Sets mines in the numbers matrix.
        The value for a mine is -1.
    """
    # Init
    n = len(numbers[0])
    count = 0

    # Place the mines
    while count < nr_mines:
        # Random mine position
        val = random.randint(0, n*n-1)
        row = val // n  # integer division
        col = val % n   # remainder

        # Place the mine, if it doesn't already have one
        if numbers[row][col] != -1:
            numbers[row][col] = -1
            count = count + 1

    return numbers

# set_mines


#-------------------------------------------------------------------------------
def set_values(numbers):
    """
    Set each cell's value.
    Which is the nr of mines around each cell.
    """
    # Init
    n = len(numbers[0])

    # Loop for counting each cell value
    for row, col in itertools.product(list(range(n)), list(range(n))):

        # Skip, if it contains a mine
        if numbers[row][col] == -1:
            continue

        # Check vertical
        # ----------------
        # Up
        if row != 0:                            # if not the first row
            if numbers[row-1][col] == -1:       # there is a mine up
                numbers[row][col] += 1          # increase value

        # Down
        if row != n-1:                          # if not the last row
            if numbers[row+1][col] == -1:       # there is a mine down
                numbers[row][col] +=  1         # increase value

        # Check horizontal
        # -----------------
        # Left
        if col != 0:
            if numbers[row][col-1] == -1:
                numbers[row][col] +=  1

        # Right
        if col != n-1:
            if numbers[row][col+1] == -1:
                numbers[row][col] +=  1

        # Check corners
        # ---------------
        # Top left
        if row != 0 and col != 0:
            if numbers[row - 1][col - 1] == -1:
                numbers[row][col] += 1

        # Top right
        if row != 0 and col != n-1:
            if numbers[row - 1][col + 1]== -1:
                numbers[row][col] += 1

        # Below left
        if row != n-1 and col != 0:
            if numbers[row + 1][col - 1]== -1:
                numbers[row][col] += 1

        # Below right
        if row != n-1 and col != n-1:
            if numbers[row + 1][col + 1]==-1:
                numbers[row][col] += 1

    return numbers

# set_values


#-------------------------------------------------------------------------------
def neighbours(n, row, col, visited, apparent, numbers):    #pylint: disable=too-many-arguments
    """
    The most complex algorith in the game *****
    This requires a recursive solution.
    When a cell with no adjacent mines is revealed (value = 0),
    all adjacent cells must be revealed, and repeat.
    Data
        numbers is a square 2d matrix
    """
    # If the cell already not visited
    if [row, col] not in visited:

        # Mark the cell visited
        visited.append([row, col])

        # If the cell is zero-valued
        if numbers[row][col] == 0:

            # Display it to the user
            apparent[row][col] = numbers[row][col]

            # Recursive calls for the neighbouring cells
            if row > 0:
                neighbours(n, row-1, col, visited, apparent, numbers)

            if row < n-1:
                neighbours(n, row+1, col, visited, apparent, numbers)

            if col > 0:
                neighbours(n, row, col-1, visited, apparent, numbers)

            if col < n-1:
                neighbours(n, row, col+1, visited, apparent, numbers)

            if row > 0 and col > 0:
                neighbours(n, row-1, col-1, visited, apparent, numbers)

            if row > 0 and col < n-1:
                neighbours(n, row-1, col+1, visited, apparent, numbers)

            if row < n-1 and col > 0:
                neighbours(n, row+1, col-1, visited, apparent, numbers)

            if row < n-1 and col < n-1:
                neighbours(n, row+1, col+1, visited, apparent, numbers)

        # If the cell is not zero-valued
        if numbers[row][col] != 0:
            apparent[row][col] = numbers[row][col]

# neighbours
