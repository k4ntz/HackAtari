# from random import random


def static_enemy_position(self):
    '''
    Makes the enemy and the blocks unable to move up and down
    '''
    self.set_ram(42, 90)
    self.set_ram(26, 37)

def _modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        if mod == "static":
            step_modifs.append(static_enemy_position)
        else:
            print('Invalid or unknown modification')
    return step_modifs, reset_modifs

