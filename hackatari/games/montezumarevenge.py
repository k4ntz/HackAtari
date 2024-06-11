import random
import numpy as np

NB_LIFES = 5
poses = ((77, 235), (88, 192), (128, 192), (133, 148), (33, 148), (22, 192))
BASE_DELAY = 108
DELAY = BASE_DELAY
DEAD = False

COLORS = [0, 1, 2, 4, 6]
COLOR_INDEX = 4

LEVEL = 0

# First list entey are is the item type (ram[49] for type, ram[50] for color), second list entry is the amount and space between items of the same type (ram[84])

ITEMS = [           [1, 0], None, None,
                None, None, [6, 0], [2, 0], [4, 0],
            [4, 0], None, [1, 0], None, None, None, [4, 0],
         None, None, None, None, [4, 0], [1, 4], None, None, [1, 3]]


# MAP = [             [0, 1, 2],
#                 [3, 4, 5, 6, 7],
#             [8, 9, 10, 11, 12, 13, 14],
#        [15, 16, 17, 18, 19, 20, 21, 22, 23]]


def random_position_start_res(self):
    """
    Enemy does not move after returning the shot.
    """
    ram = self.get_ram()
    if ram[3] == 1:
        global NB_LIFES
        ram = self.get_ram()
        NB_LIFES = ram[58]
        pos = random.choice(poses)
        pos = poses[5]
        for i, ram_n in enumerate([42, 43]):
            self.set_ram(ram_n, pos[i])


def random_position_start(self):
    ram = self.get_ram()
    if ram[3] == 1:
        global NB_LIFES, DEAD
        ram = self.get_ram()
        if ram[58] == NB_LIFES - 1 or DEAD: # life lost
            DEAD = True
        if DEAD:
            if ram[2] == 4:
                pos = poses[1]
                NB_LIFES = ram[58]
                for i, ram_n in enumerate([42, 43]):
                    self.set_ram(ram_n, pos[i])
                DEAD = False

def set_level(self):
    """
    Changes the level to a more difficult version. Level 0, 1, 2 are different versions, afterwards level%3 determines map layout.
    """
    global LEVEL
    self.set_ram(57, LEVEL)

def randomize_items(self):
    """
    Randomize which item is found in which room.
    """
    item_rooms = [0, 5, 6, 7, 8, 10, 14, 19, 20, 23]
    randomized = item_rooms.copy()
    random.shuffle(randomized)

    global ITEMS
    new_items = ITEMS.copy()

    j = 0
    for i in item_rooms:
        new_items[i] = ITEMS[randomized[j]]
        j+=1
    ITEMS = new_items

def change_items(self):
    # ram[49] for type, ram[50] for color, space between items of the same type ram[84]
    ram = self.get_ram()

    global ITEMS
    if ram[3] != 1 and ram[49] != 0:
        item_type = ITEMS[ram[3]][0]
        if item_type < 3:
            color = item_type
        else:
            color = 4
        self.set_ram(49, ITEMS[ram[3]][0])
        self.set_ram(50, color)
        self.set_ram(84, ITEMS[ram[3]][1])

def full_inventory(self):
    """
    Adds all items to inventory.
    """
    self.set_ram(65, 249)

def unify_item_color(self):
    """
    All items are turned into the same color. [Black (Invisible), Orang (Ruby), White (Sword), Yellow (Key), Green (Snake)]
    """
    global COLORS, COLOR_INDEX
    self.set_ram(50, COLORS[COLOR_INDEX])


def _modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        if mod == "random_position_start":
            step_modifs.append(random_position_start)
            reset_modifs.append(random_position_start_res)
        elif mod.startswith("level"):
            global LEVEL
            try:
                LEVEL = int(mod[-1])
            except:
                raise("Append a number 0-9 to the end of the mod-argument to choose the level")
            reset_modifs.append(set_level)
        elif mod == "randomize_items":
            step_modifs.append(change_items)
            reset_modifs.append(randomize_items)
        elif mod == "full_inventory":
            step_modifs.append(full_inventory)
        elif mod.startswith("item_color"):
            if mod[-1].isdigit():
                mod_n = int(mod[-1])
                if mod_n < 0 or mod_n > 4:
                    raise ValueError("Invalid color value, choose value 0-4 [Black (Invisible), Orang (Ruby), White (Sword), Yellow (Key), Green (Snake)]")
            else:
                raise ValueError("Append value 0-4 [Black (Invisible), Orang (Ruby), White (Sword), Yellow (Key), Green (Snake)] to your color mod-argument")
            global COLOR_INDEX
            COLOR_INDEX = mod_n
            step_modifs.append(unify_item_color)
        else:
            print('Invalid modification')
    return step_modifs, reset_modifs
