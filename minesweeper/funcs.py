"""
Funcs 
Library for the Minesweeper game

API
    get_cells(board, model)
    init_cells(cells, vec)
    update_cells(cells, game_over, game_win)
    reset_cells(cells)
"""
import itertools

# -------------------------------- Cell model funcs ----------------------------
#-------------------------------------------------------------------------------
def d_get_cells(board, model):
    """
    Get cells
    """
    print('* get_cells')
    # Count
    count = model.objects.filter(board=board.id).count()
    if count != board.get_nr_cells():    
        # Delete cells 
        cells = model.objects.filter(board=board.id).order_by('name')
        for cell in cells:
            cell.delete()
        # Create cells
        for x, y in itertools.product(list(range(board.rows)), list(range(board.cols))):
            c = model(id=None, name=f'{x}_{y}', x=x, y=y, value='0', label='', visible=False, mined=False, flagged=False, board=board)
            c.save()
    # Get and order 
    cells = model.objects.filter(board=board.id).order_by('name')
    return cells




# -------------------------------- Board funcs ---------------------------------
def short_win(board):
    """
    Win condition 1
    All mines have been flagged
    """
    print('funcs - short_win')
    print('All mines have been flagged')
    board.flags.sort()
    return board.flags == board.mines

def long_win(board):
    """
    Win condition 2
    Nr mines is equal to nr of hidden cells 
    """
    print('funcs - long_win')
    print('Nr mines is equal to nr of hidden cells')
    cells = board.get_cells()
    return nr_cells_hidden(cells) == board.nr_mines


def not_cell_flagged(board, x, y):
    """
    used by flagging_ok
    """
    return [x, y] not in board.flags
    
def not_cell_displayed(board, x, y):
    """
    used by flagging_ok
    """
    return board.apparent[x][y] == None

def flagging_ok(board, x, y):
    return not_cell_flagged(board, x, y) and not_cell_displayed(board, x, y)


# -------------------------------- Cell funcs ----------------------------------
#-------------------------------------------------------------------------------
def mined_defeat(cell):
    'Mined - Game over'
    return cell.mined and cell.visible

#-------------------------------------------------------------------------------
def nr_cells_hidden(cells):
    count = 0
    for cell in cells:
        if not cell.visible:
            count += 1
    return count

#-------------------------------------------------------------------------------
def nr_cells_visible(cells):
    count = 0
    for cell in cells:
        if cell.visible:
            count += 1
    return count
    
#-------------------------------------------------------------------------------
def reset_cells(cells):
    """
    Reset cells
    """
    print('funcs - reset_cells')
    #cells = self.get_cells()
    for cell in cells:
        cell.value = 0
        cell.label = ''
        cell.mined = False
        cell.visible = False
        cell.flagged = False       
        cell.game_over = False
        cell.success = False
        cell.empty = False
        cell.save()


#-------------------------------------------------------------------------------
def init_cells(cells, vec):
    """
    Init cells
    """
    print('funcs - init_cells')
    for cell in cells:
        x = cell.x
        y = cell.y

        #value = self.numbers[x][y]
        value = vec[x][y]

        cell.value = value
        cell.label = str(value)
        cell.visible = False 

        #if self.numbers[x][y] == -1:
        if vec[x][y] == -1:
            cell.mined = True

        cell.flagged = False
        if value == 0:
            cell.empty = True 
        cell.game_over = False
        cell.success = False
        cell.save()


#-------------------------------------------------------------------------------
def update_cells(cells, game_over, game_win):
    print('funcs - update_cells')
    #cells = Cell.objects.filter(board=self.id).order_by('name')
    for cell in cells:
        cell.game_over = game_over
        cell.success = game_win
        cell.save()



