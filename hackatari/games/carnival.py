MISSILE_SPEED_INCREASE = 0

def no_flying_ducks (self):
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

def fast_missiles(self):
    """
    The projectiles fired from the players are faster. 
    Increases the speed of the missiles by changing the corresponding ram positions.
    Uses the values 1-3 to determine how by how much to speed the missile up.
    """
    missile_y = self.get_ram()[55]

    #ensures there is a missile in the game 
    if missile_y >= 5: 
        self.set_ram(55, missile_y - MISSILE_SPEED_INCREASE)


def _modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        if mod == "no_flying_ducks":
            step_modifs.append(no_flying_ducks)
        elif mod == "unlimited_ammo":
            step_modifs.append(unlimited_ammo)
        elif mod.startswith("fast_missiles"):
            if mod[-1].isdigit():
                mod_n = int(mod[-1])
                if mod_n < 1 or mod_n > 3:
                    raise ValueError("Invalid speed increase, choose value 1-3")
            else:
                raise ValueError("Append value 1-3 to your fast_missiles mod-argument")
            global MISSILE_SPEED_INCREASE
            MISSILE_SPEED_INCREASE = mod_n
            step_modifs.append(fast_missiles)
        else:
            print('Invalid modification')
    return step_modifs, reset_modifs
