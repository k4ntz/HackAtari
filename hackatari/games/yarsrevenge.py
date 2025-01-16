# from random import random


def static_enemy_position(self):
    """
    Makes the enemy and the blocks unable to move up and down
    """
    self.set_ram(42, 90)
    self.set_ram(26, 37)


def _modif_funcs(env, modifs):
    for mod in modifs:
        if mod == "static":
            env.step_modifs.append(static_enemy_position)
        else:
            print("Invalid or unknown modification")
