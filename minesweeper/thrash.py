#21 feb 2021

"""
    Explore - Deprecated !
    Alternative library - not used
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







# 19 feb 
    #def check_game(self, cell_name):
    #    """
    #    If mined re-initialize.
    #    """
    #    print('*** check_game')
    #    print(cell_name)
    #    cell = self.get_cell_name(cell_name)
    #    if cell.mined:
    #        print('*** gotcha !!!')                
            # Init the game
    #        self.init_game()
    #        self.save()




# 15 feb 


def add_user(request, user_name):
    print('*** add_user')

    if user_name == 'harry':
        first_name = 'Harry'
        last_name = 'Potter'
        email = 'hpotter@gmail.com'
        password = 'nyctal6+'

    elif user_name == 'ron':
        first_name = 'Ron'
        last_name = 'Weasly'
        email = 'rweasly@gmail.com'
        password = "@2wHGS#B"

    elif user_name == 'hermione':
        first_name = 'Hermione'
        last_name = 'Granger'
        email = 'hgranger@gmail.com'
        password = "Tz9+8ndB"

    else:
        # This should not happen
        1/0

    user = util.add_user(user_name, first_name, last_name, email, password)
    return HttpResponseRedirect(reverse("index"))








# 14 feb 

    @unittest.skip
    def test_url_update(self):
        """
        Board update
        GET request
        """
        print(f"{self.prefix}test_url_update")

        # Init
        reset_game(self.board)

        # Cell
        url = f'http://127.0.0.1:8000/board_update/?board_id={self.board.id}&cell_name={self.cell_name}&flag={self.flag}'
        response = self.client.get(url)

        count = len(response.json())
        
        # Assert dimension
        self.assertEqual(count, self.board.rows * self.board.cols)
        
        for i in range(count):
            cell = response.json()[i]
            if cell['name'] == self.cell_name:
                print(cell)

                # Assert visible
                self.assertEqual(cell['visible'], True)
                self.assertIn(cell['value'], [-1, 0, 1, 2, 3, 4, 5, 6, 7, 8])
                self.assertIn(cell['label'], ['-1', '.', '1', '2', '3', '4', '5', '6', '7', '8'])

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)







def index(request):
    """
    Index
    """
    print('*** index')
    return render(request, "minesweeper/index.html",
        {
            "boards": util.list_boards()
        })


#-------------------------------------------------------------------------------
#class UserViewSet(viewsets.ModelViewSet):
#    """
#    API endpoint that allows users to be viewed or edited.
#    """
#    queryset = User.objects.all().order_by('-date_joined')
#    serializer_class = UserSerializer
    #permission_classes = [permissions.IsAuthenticated]

#class GroupViewSet(viewsets.ModelViewSet):
#    """
#    API endpoint that allows groups to be viewed or edited.
#    """
#    queryset = Group.objects.all()
#    serializer_class = GroupSerializer
    #permission_classes = [permissions.IsAuthenticated]




    @unittest.skip
    def test_view_index(self):
        """
        Index view
        GET request
        """
        print(f"{self.prefix}test_view_index")
        # Login because login required
        User = get_user_model()
        self.client.login(username='temporary', password='temporary')
        # Index
        response = self.client.get('/games/')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


    @unittest.skip
    def test_view_show(self):
        """
        Show view
        GET request
        """
        print(f"{self.prefix}test_view_show")
        # Show
        response = self.client.get(f'/show/{self.board.id}/')
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)


    @unittest.skip
    def test_view_play(self):
        """
        Play view
        GET request
        """
        print(f"{self.prefix}test_view_play")

        # Init
        self.board.reset_sm()
        self.board.init_game()

        # Play
        response = self.client.get(f'/play/{self.board.id}/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)








# Feb 5 2021

# Models

    def update_duration(self, duration):
        print('*** update_duration')
        print(duration)
        self.duration = timedelta(milliseconds=int(duration))
        self.save()

    def get_duration(self):
        print(self.duration)
        duration = str(self.duration).split('.')[0]
        return duration






# Tests 
# State 
#url = f'http://127.0.0.1:8000/board_update/?board_id={self.board.id}&state={self.state}'
# Duration
#url = f'http://127.0.0.1:8000/board_update/?board_id={self.board.id}&duration={self.duration}'





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
