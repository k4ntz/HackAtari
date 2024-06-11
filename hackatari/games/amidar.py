# from random import random

PAUSE = 0
TIMER = 0

def set_enemies(self):
    '''
    Changes the enemies to the second version.
    '''
    ram = self.get_ram()
    for i in range(7):
        if ram[73+i]&32:
            self.set_ram(73+i, ram[73+i]|16)

def set_player(self):
    '''
    Changes the player to the second version.
    '''
    ram = self.get_ram()
    for i in range(7):
        if not ram[73+i]&32:
            self.set_ram(73+i, ram[73+i]|16)

# def no_enemies(self):
#     ram = self.get_ram()
#     for i in range(7):
#         if ram[73+i]&32:
#             self.set_ram(73+i, ram[73+i]&(~32))
    


def _modif_funcs(modifs): 
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        if mod == "change_enemy":
            step_modifs.append(set_enemies)
        elif mod == "change_player":
            step_modifs.append(set_player)
        elif mod == "no_enemies":
            step_modifs.append(no_enemies)
        else:
            print('Invalid or unknown modification')
    return step_modifs, reset_modifs

