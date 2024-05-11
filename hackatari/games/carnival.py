def no_flying_duck(self):
    """
    Ducks in the last row disappear instead of turning into flying ducks.
    """
    ram = self.get_ram()
    self.set_ram(1, 79)

def unlimited_ammo(self):
    """
    Ammunition doesn't decrease.
    """
    ram = self.get_ram()
    self.set_ram(3, 40)


def modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        if mod == "no_flying_duck":
            step_modifs.append(no_flying_duck)
        elif mod == "unlimited_ammo":
            step_modifs.append(unlimited_ammo)
        else:
            print('Invalid modification')
    return step_modifs, reset_modifs
