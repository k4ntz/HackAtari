# from random import random
import numpy as np

def modify_ram_invert_flag(self):
    '''
    Invert Flag
    '''
    ram = self.get_ram()
    types = ram[70:78]
    cols = ram[78:86]
    for i in range(8):
        if types[i] == 2: 
            self.set_ram(78+i, 4)

def wall_inpaintings():
    background_color = np.array((80, 0, 132))
    w, h = 8, 36
    patch = (np.ones((h, w, 3)) * background_color).astype(np.uint8)
    ladder_poses = [(132, 36), (132, 132), (20, 84)]
    return [(y, x, h, w, patch) for x, y in ladder_poses] # needs swapped positions


def _modif_funcs(modifs):
    step_modifs, reset_modifs, inpaintings = [], [], False
    for mod in modifs:
        if mod == "invert_flags":
            step_modifs.append(modify_ram_invert_flag)
        else:
            print('Invalid or unknown modification')
    return step_modifs, reset_modifs, inpaintings

