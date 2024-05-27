LAST_ENEMY_Y_POS = 127
BALL_PREVIOUS_X_POS = 130


def no_fuel(self):
    """
    Removes the fuel deposits from the game.
    """
    ram = self.get_ram()
    self.set_ram(55, 255)
    for i in range(6):
        type = ram[32 + i]
        if type == 10: # fuel deposit
            self.set_ram(32+i, 0)


def _modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        if mod == "no_fuel":
            step_modifs.append(no_fuel)
        else:
            print('Invalid modification')
    return step_modifs, reset_modifs
