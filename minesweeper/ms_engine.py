"""
    Minesweeper engine

    From the article:
    Ask Python
    "Create Minesweeper using Python From the Basic to Advanced"
    https://www.askpython.com/python/examples/create-minesweeper-using-python
"""
import random

#-------------------------------------------------------------------------------
def set_mines(n, numbers, nr_mines):
    """
    The actual values of the grid
    The actual value for a mine is stored as -1,
    whereas the values stored for display, denote the mine as 'M'.
    """
    # Track of number of mines already set up
    count = 0
    while count < nr_mines:

        # Random number from all possible grid positions
        val = random.randint(0, n*n-1)

        # Generating row and column from the number
        row = val // n
        col = val % n

        # Place the mine, if it doesn't already have one
        if numbers[row][col] != -1:
            count = count + 1
            numbers[row][col] = -1

    return numbers
# set_mines


#-------------------------------------------------------------------------------
def set_values(n, numbers):
    """
    Function for setting up the other grid values
    These values are to be hidden from the player, therefore they are stored in numbers variable.
    """
    # Loop for counting each cell value
    for r in range(n):
        for col in range(n):

            # Skip, if it contains a mine
            if numbers[r][col] == -1:
                continue

            # Check up
            if r > 0 and numbers[r-1][col] == -1:
                numbers[r][col] = numbers[r][col] + 1

            # Check down
            if r < n-1  and numbers[r+1][col] == -1:
                numbers[r][col] = numbers[r][col] + 1

            # Check left
            if col > 0 and numbers[r][col-1] == -1:
                numbers[r][col] = numbers[r][col] + 1

            # Check right
            if col < n-1 and numbers[r][col+1] == -1:
                numbers[r][col] = numbers[r][col] + 1

            # Check top-left
            if r > 0 and col > 0 and numbers[r-1][col-1] == -1:
                numbers[r][col] = numbers[r][col] + 1

            # Check top-right
            if r > 0 and col < n-1 and numbers[r-1][col+1]== -1:
                numbers[r][col] = numbers[r][col] + 1

            # Check below-left
            if r < n-1 and col > 0 and numbers[r+1][col-1]== -1:
                numbers[r][col] = numbers[r][col] + 1

            # Check below-right
            if r < n-1 and col< n-1 and numbers[r+1][col+1]==-1:
                numbers[r][col] = numbers[r][col] + 1

    return numbers
# set_values


#-------------------------------------------------------------------------------
def neighbours(n, row, col, vis, apparent, numbers):
    """
    Recursive
    """
    # If the cell already not visited
    if [row,col] not in vis:

        # Mark the cell visited
        vis.append([row,col])

        # If the cell is zero-valued
        if numbers[row][col] == 0:

            # Display it to the user
            apparent[row][col] = numbers[row][col]

            # Recursive calls for the neighbouring cells
            if row > 0:
                neighbours(n, row-1, col, vis, apparent, numbers)

            if row < n-1:
                neighbours(n, row+1, col, vis, apparent, numbers)

            if col > 0:
                neighbours(n, row, col-1, vis, apparent, numbers)

            if col < n-1:
                neighbours(n, row, col+1, vis, apparent, numbers)

            if row > 0 and col > 0:
                neighbours(n, row-1, col-1, vis, apparent, numbers)

            if row > 0 and col < n-1:
                neighbours(n, row-1, col+1, vis, apparent, numbers)

            if row < n-1 and col > 0:
                neighbours(n, row+1, col-1, vis, apparent, numbers)

            if row < n-1 and col < n-1:
                neighbours(n, row+1, col+1, vis, apparent, numbers)

        # If the cell is not zero-valued
        if numbers[row][col] != 0:
            apparent[row][col] = numbers[row][col]
# neighbours
