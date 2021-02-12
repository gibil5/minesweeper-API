"""
    Explore

    Alternative - not used
"""

#-------------------------------------------------------------------------------
def get_empty_neighbors(xo, yo, arr, board_id, Cell):
    print('\n\nget_empty_neighbors')
    print(xo, yo)
    print()
    if len(arr) < 10:
        for x in range(xo - 1, xo + 2):
            for y in range(yo - 1, yo + 2):
                if x > -1 and y > -1:
                    if (x, y) != (xo, yo):
                        if not (x, y) in arr:
                            print(x, y)
                            arr.append((x, y))
        for tup in arr:
            x = tup[0]
            y = tup[1]
            try:
                print('try')
                cell = Cell.objects.get(board=board_id, x=x, y=y)
            except:
                print('error')
            else:            
                print('success')
                if cell.value == '0': 
                    print('ok')
                    cell.visible = True
                    cell.save()
                    get_empty_neighbors(x, y, arr, board_id, Cell)
    else:
        print('jx')
    return

def explore_all(cell, count, rows, cols, Cell, board_id, solution, x0, y0):
    """
    Recursive
    """
    print('\n*** explore')
    print(count)
    count += 1
    #if len(solution) < 10 and count < 10:
    if len(solution) < 20 and count < 10:
        # Deltas
        deltas_x = [-1, 1]
        for delta in deltas_x: 
            x = cell.x + delta * x0
            y = cell.y + delta * y0
            if -1 < x < cols + 1 and -1 < y < rows + 1:
                try:
                    new_cell = Cell.objects.get(board=board_id, x=x, y=y)
                except:
                    print("Something went wrong")
                else:
                    print("Nothing went wrong")
                    # New cell is empty
                    if new_cell.value == '0':
                        print('Cell is empty')
                        if not (x, y) in solution:
                            solution.append((x, y))
                        explore_all(new_cell, count, rows, cols, Cell, board_id, solution, x0, y0)
                    # New cell is not empty
                    else:
                        print('Cell is NOT empty')
                        #return
    else:
        print('jx')
    return


#-------------------------------------------------------------------------------
def clean(bombs, solution, m, n, verbose=False):
    #print()
    board = []
    for i in range(1, m+1):
        b = []
        board.append(b)
        for k in range(1, n+1):
            if bombs[i][k]:
                value = '*'
            else:
                value = f'{solution[i][k]}'
            #print(value, end='')
            b.append(value)
        #print()
    #print()
    return board

def create2D(rowCount, colCount, value=None):
    """
    Create and return a 2D array having rowCount rows and colCount
    columns, with each element initialized to value.
    """
    a = [None] * rowCount
    for row in range(rowCount):
        a[row] = [value] * colCount
    return a

def create_board(m, n, p):
    # Accept integers m and n, and float p as command-line arguments.
    # Create a m x n minesweeper game where each cell is a bomb with
    # probability p. Write the m x n game and the neighboring bomb counts
    # to standard output.
    print('*** create_board')
    print(m)
    print(n)
    print(p)
    print()
    
    # Bombs
    # ------
    # Create bombs as a m+2 * n+2 array.
    bombs = create2D(m+2, n+2, False)

    # bombs is [1..m][1..n]; the border is used to handle boundary cases.
    for r in range(1, m+1):
        for c in range(1, n+1):
            bombs[r][c] = (random.random() < p)

    # Write the bombs.
    for r in range(1, m+1):
        for c in range(1, n+1):
            if bombs[r][c]:
                print('* ', end='')
            else:
                print('. ', end='')
        print()

    # Solution
    # ---------
    # Create solution as a m+2 x n+2 array.
    solution = create2D(m+2, n+2, 0)

    # solution[i][j] is the number of bombs adjacent to cell (i, j).
    for r in range(1, m+1):
        for c in range(1, n+1):
            # (rr, cc) indexes neighboring cells.
            for rr in range(r-1, r+2):
                for cc in range(c-1, c+2):
                    if bombs[rr][cc]:
                        solution[r][c] += 1

    # Write solution.
    print()
    for r in range(1, m+1):
        for c in range(1, n+1):
            if bombs[r][c]:
                print('* ', end='')
            else:
                print(str(solution[r][c]) + ' ', end='')
        #stdio.writeln()
        print()

    return bombs, solution
# End create_board


# Main
m = 3
n = 3
p = 0.2
bombs, solution = create_board(m, n, p)
#print(bombs)
#print(solution)
print('------------')
print()
#for i in range(1, m+1):
#    for k in range(1, n+1):
#        if bombs[i][k]:
#            print('* ', end='')
#        else:
#            print('. ', end='')            
#    #print()

print()
board = []
for i in range(1, m+1):
    b = []
    board.append(b)
    for k in range(1, n+1):
        if bombs[i][k]:
            value = '* '
        else:
            value = f'{solution[i][k]} '
        print(value, end='')
        b.append(value)
    #print()
#print()

print(board)
