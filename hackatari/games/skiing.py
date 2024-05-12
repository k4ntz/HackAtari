from random import random


def modify_ram_invert_flag(self):
    '''
    wind: Sets the ball in the up and right direction by 3 pixles every single ram step
    to simulate the effect of wind
    '''
    ram = self.get_ram()
    types = ram[70:78]
    cols = ram[78:86]
    for i in range(8):
        if types[i] == 2: 
            self.set_ram(78+i, 4)


def modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        if mod == "invert_flags":
            step_modifs.append(modify_ram_invert_flag)
    return step_modifs, reset_modifs

