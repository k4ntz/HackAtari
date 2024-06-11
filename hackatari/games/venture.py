import random

ENEMY_COLOR = 0
ENEMY_RANDOM_COLORS = [0, 0, 0, 0, 0, 0]

ROOM = 8

colors = [0, 12, 48, 113, 200]

def enemy_colors(self):
    '''
    Changes the color of all enemies to the one specified in the argument.
    '''
    ram = self.get_ram()
    if ram[90] != 8 and ram[90] != 9:
        for i in range(5):
            self.set_ram(37+i, colors[ENEMY_COLOR])
    else:
        for i in range(6):
            self.set_ram(36+i, colors[ENEMY_COLOR])

def random_colors(self):
    '''
    Changes the color of each enemy to one of the five colors at radom. 
    '''
    ram = self.get_ram()
    if ram[90] != 8 and ram[90] != 9:
        for i in range(5):
            self.set_ram(37+i, ENEMY_RANDOM_COLORS[i])
    else:
        for i in range(6):
            self.set_ram(36+i, ENEMY_RANDOM_COLORS[i])
    
    global ROOM
    ram = self.get_ram()
    if ROOM != ram[90]:
        ROOM = ram[90]
        for i in range(6):
            ENEMY_RANDOM_COLORS[i] = random.choice(colors)

def reset_random_colors(self):
    for i in range(6):
        ENEMY_RANDOM_COLORS[i] = random.choice(colors)

# ram 62 == map layout

def _modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        if mod == "enemy_color_random":
            step_modifs.append(random_colors)
            reset_modifs.append(reset_random_colors)
        elif mod.startswith("enemy_color"):
            if mod[-1].isdigit():
                mod_n = int(mod[-1])
                if mod_n < 0 or mod_n > 4:
                    raise ValueError("Invalid color for enemies, choose value 0-4 [black, white, red, blue, green]")
            else:
                raise ValueError("Append value 0-4 [black, white, red, blue, green] to your color mod-argument")
            global ENEMY_COLOR
            ENEMY_COLOR = mod_n
            step_modifs.append(enemy_colors)
        else:
            print('Invalid or unknown modification')
    return step_modifs, reset_modifs

