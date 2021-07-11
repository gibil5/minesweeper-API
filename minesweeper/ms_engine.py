"""
    This is the Minesweeper game Engine
    It can be used by any framework. 
    
    From the article: 
    "Create Minesweeper using Python From the Basic to Advanced"
    Ask Python web site 
    https://www.askpython.com/python/examples/create-minesweeper-using-python
"""
import random

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
    Which is calculated using the nr of mines around each cell. 
    """
    # Init 
    n = len(numbers[0])

    # Loop for counting each cell value
    for row in range(n):
        for col in range(n):

            # Skip, if it contains a mine
            if numbers[row][col] == -1:
                continue

            #if row > 0 and numbers[row - 1][col] == -1:
            #if row < n-1  and numbers[row + 1][col] == -1:
            #if col > 0 and numbers[row][col - 1] == -1:
            #if col < n-1 and numbers[row][col + 1] == -1:

            #if row > 0 and col > 0:
            #if row > 0 and col < n-1:
            #if row < n-1 and col > 0:
            #if row < n-1 and col< n-1:


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
