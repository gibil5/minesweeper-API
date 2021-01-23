
# ------------------------------------------------------------------------------
# Models
# ------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
    def neighbours(self, n, row, col, vis, apparent, numbers):
        """
        Recursive
        """
        print('** neighbours')
        #print(vis)
        #global apparent
        #global numbers
        #global vis
     
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
                    #neighbours(row-1, col)
                    self.neighbours(n, row-1, col, vis, apparent, numbers)

                if row < n-1:
                    #neighbours(row+1, col)
                    self.neighbours(n, row+1, col, vis, apparent, numbers)

                if col > 0:
                    #neighbours(row, col-1)
                    self.neighbours(n, row, col-1, vis, apparent, numbers)

                if col < n-1:
                    #neighbours(row, col+1)    
                    self.neighbours(n, row, col+1, vis, apparent, numbers)

                if row > 0 and col > 0:
                    #neighbours(row-1, col-1)
                    self.neighbours(n, row-1, col-1, vis, apparent, numbers)

                if row > 0 and col < n-1:
                    #neighbours(row-1, col+1)
                    self.neighbours(n, row-1, col+1, vis, apparent, numbers)

                if row < n-1 and col > 0:
                    #neighbours(row+1, col-1)
                    self.neighbours(n, row+1, col-1, vis, apparent, numbers)

                if row < n-1 and col < n-1:
                    #neighbours(row+1, col+1)  
                    self.neighbours(n, row+1, col+1, vis, apparent, numbers)  

            # If the cell is not zero-valued         
            if numbers[row][col] != 0:
                apparent[row][col] = numbers[row][col]
    # neighbours
        



#-------------------------------------------------------------------------------
    def update_nex(self, cell_name):
        """
        Dep !
        """
        print('** update_nex')
        cells = Cell.objects.filter(board=self.id)
        arr = []
        for cell in cells:
            if cell.name == cell_name:
                cell.visible = True
                cell.save()
                if cell.value == '0':
                    ms.get_empty_neighbors(cell.x, cell.y, arr, self.id, Cell)
        print(arr)
        if False:
            for tup in arr:
                x = tup[0]
                y = tup[1]
                try:
                    cell = Cell.objects.get(board=self.id, x=x, y=y)
                except:
                    print('error')
                else:            
                    #print('ok')
                    if cell.value == '0': 
                        cell.visible = True
                        cell.save()

    # Calc board
    def update(self, cell_name):
        """
        Dep !
        """
        print('** update')
        cells = Cell.objects.filter(board=self.id)
        #count = 1
        # Update - called by grid.js
        for cell in cells:
            if cell.name == cell_name:
                cell.visible = True
                cell.save()
                # Get adjacent empty cells
                if cell.value == '0':
                    # Horizontal
                    count_h = 1
                    solution_hor = []
                    if True:
                        #ms.explore_horizontal(cell, count_h, self.rows, self.cols, Cell, self.id, solution_hor, 0, 1)
                        ms.explore_all(cell, count_h, self.rows, self.cols, Cell, self.id, solution_hor, 0, 1)
                        print('****************')
                        print(solution_hor)
                        print('****************')

                    # Vertical
                    count_v = 1
                    solution_ver = []
                    if True:
                        #ms.explore_vertical(cell, count_v, self.rows, self.cols, Cell, self.id, solution_ver, 1, 0)
                        ms.explore_all(cell, count_v, self.rows, self.cols, Cell, self.id, solution_ver, 1, 0)
                        print('****************')
                        print(solution_ver)
                        print('****************')

        # Adjacent cells must be visible also
        for tup in solution_hor:
            x = tup[0]
            y = tup[1]
            cell = Cell.objects.get(board=self.id, x=x, y=y)
            cell.visible = True
            cell.save()

        for tup in solution_ver:
            x = tup[0]
            y = tup[1]
            cell = Cell.objects.get(board=self.id, x=x, y=y)
            cell.visible = True
            cell.save()

    # Calc engine
    def calc_engine(self):
        print('calc_engine')        
        p = 0.1
        bombs, solution = ms.create_board(self.rows, self.cols, p)
        board = ms.clean(bombs, solution, self.rows, self.cols)
        print(board)
        cells = Cell.objects.filter(board=self.id)
        # init
        for cell in cells:
            cell.name = f'{cell.x}_{cell.y}'
            cell.visible = False
            cell.value = board[cell.x][cell.y]
            if cell.value == '*':
                cell.mined = True 
            else: 
                cell.mined = False 
            cell.save()
            #print(cell.name, cell.value, cell.x, cell.y)
            #print()

        # Check adherence
        #print('check adherence')
        #for cell in cells:
        #    if cell.value == '0':
        #        print('zero')
        #        print(cell.name)
        #        print()



# ------------------------------------------------------------------------------
# Engine
# ------------------------------------------------------------------------------

def explore_horizontal(cell, count, rows, cols, Cell, board_id, solution, x0, y0):
    """
    Recursive
    """
    print('\n*** explore')
    print(count)
    count += 1
    if len(solution) < 10 and count < 10:
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
                        explore_horizontal(new_cell, count, rows, cols, Cell, board_id, solution, 0, 1)
                    # New cell is not empty
                    else:
                        print('Cell is NOT empty')
                        #return
    else:
        print('jx')
    return



def explore_vertical(cell, count, rows, cols, Cell, board_id, solution, x0, y0):
    """
    Recursive
    """
    print('\n*** explore')
    print(count)
    count += 1
    if len(solution) < 10 and count < 10:
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
                        explore_vertical(new_cell, count, rows, cols, Cell, board_id, solution, 1, 0)
                    # New cell is not empty
                    else:
                        print('Cell is NOT empty')
                        #return
    else:
        print('jx')
    return










# ------------------------------------------------------------------------------
# Models 
# ------------------------------------------------------------------------------
    # Calc board
    def calc(self, cmd, cell_name=None):
        import random
        print('*** calc')
        print(cmd)
        print(cell_name)
        cells = Cell.objects.filter(board=self.id)


        # Init - called by views.play
        if cmd == 'init':
            print('** init')
            names = []
            for cell in cells:
                names.append(cell.name)
            mined_cells = random.sample(names, self.rows-1)
            print(mined_cells)
            for cell in cells:
                cell.name = f'{cell.x}_{cell.y}'
                cell.visible = False
                cell.mined = False
                cell.value = 0
                if cell.name in mined_cells:
                    cell.mined = True
                    cell.value = 9
                cell.save()


        # Update - called by grid.js
        if cmd == 'update':
            print('** update')
            count = None

            for cell in cells:
                # Clicked cell - must have side effects
                if cell.name == cell_name:
                    cell.visible = True
                    #count = self.count_adjacent_mines(cell.x, cell.y)
                    #cell.value = count
                    cell.save()

            #  This must be recursive
            if count == 0:
                print('*** RE - EXPLORE !!!')
                #self.clear_around(cell.x, cell.y)


    # Count adjacent mines
    def count_adjacent_mines(self, x0, y0):
        print('count_adjacent_mines')
        count = 0

        for x in range(x0-1, x0+2):
            for y in range(y0-1, y0+2):
                if (x > -1 and x < self.cols) and (y > -1 and y < self.rows):
                    if not (x == x0 and y == y0):
                        name = f'{x}_{y}'
                        print(name)
                        cell = Cell.objects.get(board=self.id, name=name)
                        print(cell)

                        if cell.mined:
                            count += 1
        return count


    # Clear around - Must be recursive
    def clear_around(self, x0, y0):
        print('clear_around')
        for x in range(x0-1, x0+2):
            for y in range(y0-1, y0+2):
                if (x > -1 and x < self.cols) and (y > -1 and y < self.rows):
                    if not (x == x0 and y == y0):
                        name = f'{x}_{y}'
                        print(name)
                        cell = Cell.objects.get(board=self.id, name=name)
                        print(cell)
                        cell.visible = True
                        cell.save()
