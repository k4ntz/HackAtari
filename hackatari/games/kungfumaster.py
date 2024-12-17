# from random import random

def no_damage(self):
    '''
    Always sets the player health to max, making them invincible
    '''
    self.set_ram(75, 39)


def infinite_time(self):
    '''
    Unlimited time to clear the level
    '''
    self.set_ram(27, 32)
    self.set_ram(28, 1)


def infinte_lives(self):
    '''
    Always sets the player health to max, making them invincible
    '''
    self.set_ram(29, 3)


def _modif_funcs(env, modifs):
    for mod in modifs:
        if mod == "no_damage":
            env.step_modifs.append(no_damage)
        elif mod == "infinite_time":
            env.step_modifs.append(infinite_time)
        elif mod == "infinte_lives":
            env.step_modifs.append(infinte_lives)
        else:
            print('Invalid or unknown modification')
