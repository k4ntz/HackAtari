ICE_COLOR = 0 # Black, Red, Blue, Green
UI_COLOR = 0 # New color for the UI (Int: 000-255)
LINE = [False,False,False,False] # Which lines are recolored, multiple line commands are possible (Int: 0-3)
ENEMIES_NUMBER = 0 # Define the numbers of enemies to occur per line (Int: 0-3)
NEW_X_POS = 0 # New startposition of ice shelves (Int: 0-255)

colors = [0, 48, 113, 200]
"""
A constant used to change the mode for the number of enemies.
"""
def modify_ram_for_color(self):
    '''
    Adjusts the colors of the ice floes bases on the specified values.
    '''
    if LINE[3]:
        self.set_ram(43, colors[ICE_COLOR])
    if LINE[2]:
        self.set_ram(44, colors[ICE_COLOR])
    if LINE[1]:
        self.set_ram(45, colors[ICE_COLOR])
    if LINE[0]:
        self.set_ram(46, colors[ICE_COLOR])

def modify_ram_for_uicolor(self):
    '''
    Adjusts the colors of the ui bases on the specified values.
    '''
    self.set_ram(71, UI_COLOR)

def modify_ram_for_floes_position(self):
    '''
    Adjusts the memory based on the specified new position of the ice floes.
    '''
    self.set_ram(22, 0)
    self.set_ram(31, NEW_X_POS)
    self.set_ram(32, NEW_X_POS)
    self.set_ram(33, NEW_X_POS)
    self.set_ram(34, NEW_X_POS)

def modify_ram_for_enemy_amount(self):
    '''
    Adjusts the memory based on the specified number of enemies selected by the user.
    '''
    if ENEMIES_NUMBER > 0:
        # enemies number 1: easy mode with 0 enemies
        if ENEMIES_NUMBER == 1:
            value = 0
        # enemies number 2: medium mode with 8 enemies
        elif ENEMIES_NUMBER == 2:
            value = 5
        # enemies number 3: medium mode with 12 enemies
        elif ENEMIES_NUMBER == 3:
            value = 15
        for rows in range(92, 96):
            self.set_ram(rows, value)


def random_color(self):
    global ICE_COLOR
    self.set_ram(43, ICE_COLOR)
    self.set_ram(44, ICE_COLOR)
    self.set_ram(45, ICE_COLOR)
    self.set_ram(46, ICE_COLOR)


def _modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        if mod.startswith('color'):
            if mod[-1].isdigit():
                mod_n = int(mod[-1])
                if mod_n < 0 or mod_n > 3:
                    raise ValueError("Invalid color for ice, choose value 0-3 [black, red, blue, green]")
            else:
                raise ValueError("Append value 0-3 [black, red, blue, green] to your color mod-argument")
            global ICE_COLOR
            ICE_COLOR = mod_n
            step_modifs.append(modify_ram_for_color)
        elif mod.startswith('line'):
            mod_n = int(mod[-1])
            if mod_n < 1 or mod_n > 4:
                raise ValueError("Invalid color for ice, choose number 1-5")
            global LINE
            LINE[mod_n-1] = True
            step_modifs.append(modify_ram_for_color)
        elif mod.startswith('ui_color'):
            if mod[-1].isdigit():
                mod_n = int(mod[-1])
                if mod_n < 0 or mod_n > 3:
                    raise ValueError("Invalid color for ui, choose value 0-3 [black, red, blue, green]")
            else:
                raise ValueError("Append value 0-3 [black, red, blue, green] to your ui_color mod-argument")
            global UI_COLOR
            UI_COLOR = mod_n
            step_modifs.append(modify_ram_for_uicolor)
        elif mod.startswith('e'):
            mod_n = int(mod[-1])
            if mod_n < 0 or mod_n > 3:
                raise ValueError("Invalid number of enenmies, choose number 0-3")
            global ENEMIES_NUMBER
            ENEMIES_NUMBER = mod_n
            step_modifs.append(modify_ram_for_enemy_amount)
        elif mod.startswith('f'):
            for i in range(3):
                if mod[-3+i:].isdigit():
                    mod_n = int(mod[-3+i:])
                    break
            if mod_n < 0 or mod_n > 160:
                raise ValueError("Invalid position for floes, max. value is 160")
            global NEW_X_POS
            NEW_X_POS = mod_n
            step_modifs.append(modify_ram_for_floes_position)
    return step_modifs, reset_modifs


# def _modif_funcs(modifs):
#     step_modifs, reset_modifs = [], []
#     for mod in modifs:
#         if mod.startswith('color'):
#             mod_n = int(mod[-3:])
#             if mod_n < 0 or mod_n > 255:
#                 raise ValueError("Invalid color for ice")
#             global ICE_COLOR
#             ICE_COLOR = mod_n
#             #step_modifs.append(modify_ram_for_color)
#         elif mod.startswith('line'):
#             mod_n = int(mod[-1])
#             if mod_n < 1 or mod_n > 5:
#                 raise ValueError("Invalid color for ice")
#             global LINE
#             LINE[mod_n] = True
#             step_modifs.append(modify_ram_for_color)
#         elif mod.startswith('color_ui'):
#             mod_n = int(mod[-3:])
#             if mod_n < 0 or mod_n > 255:
#                 raise ValueError("Invalid color for UI")
#             global UI_COLOR
#             UI_COLOR = mod_n
#             step_modifs.append(modify_ram_for_uicolor)
#         elif mod.startswith('e'):
#             mod_n = int(mod[-1])
#             if mod_n < 0 or mod_n > 3:
#                 raise ValueError("Invalid number of enenmies")
#             global ENEMIES_NUMBER
#             ENEMIES_NUMBER = mod_n
#             step_modifs.append(modify_ram_for_enemy_amount)
#         elif mod.startswith('f'):
#             mod_n = int(mod[-3:])
#             if mod_n < 0 or mod_n > 255:
#                 raise ValueError("Invalid position for floes")
#             global NEW_X_POS
#             NEW_X_POS = mod_n
#             reset_modifs.append(modify_ram_for_floes_position)
#     return step_modifs, reset_modifs