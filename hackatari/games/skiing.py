# from random import random


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


def _modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        if mod == "invert_flags":
            step_modifs.append(modify_ram_invert_flag)
        else:
            print('Invalid or unknown modification')
    return step_modifs, reset_modifs

