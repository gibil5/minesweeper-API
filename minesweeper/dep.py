# 19 jul 2020 


    #def get_duration(self):
    #   """
    #   Used by the template
    #   """
    #    return str(self.duration).split('.')[0]

    #def get_user(self):
    #   """
    #   Used by the template
    #   """
    #    return self.user.username.capitalize() if self.user else None






# Cell funcs -------------------------------------------------------------------

    #def nr_cells_hidden(self):
    #    cells = self.get_cells()
    #    count = 0
    #    for cell in cells:
    #        if not cell.visible:
    #            count += 1
    #    return count


    #def nr_cells_visible(self):
    #def nr_cells_visible(cells):
        #cells = self.get_cells()
        #cells = funcs.get_cells(self)
    #    count = 0
    #    for cell in cells:
    #        if cell.visible:
    #            count += 1
    #    return count

    #def reset_cells(self):
    #    """
    #    Reset cells
    #    """
    #    print('reset_cells')
    #    cells = self.get_cells()
    #    for cell in cells:
    #        cell.value = 0
    #        cell.label = ''
    #        cell.mined = False
    #        cell.visible = False
    #        cell.flagged = False       
    #        cell.game_over = False
    #        cell.success = False
    #        cell.empty = False
    #        cell.save()

    #def update_cells(self, game_over, game_win):
    #    cells = Cell.objects.filter(board=self.id).order_by('name')
    #    for cell in cells:
    #        cell.game_over = game_over
    #        cell.success = game_win
    #        cell.save()

    #def mined_defeat(self, cell):
    #    'Mined - Game over'
    #    return cell.mined and cell.visible

