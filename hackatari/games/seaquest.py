def gravity(self):
    """
    Enables gravity for the player.
    """
    ram = self.get_ram()
    if ram[97] < 105:
        self.set_ram(97, ram[97] + 1)

def disable_enemies(self):
    """
    Disables all the enemies.
    """
    for x in range(4):
        self.set_ram(36 + x, 0)

def is_gamestart(self):
    """
    Determines if it is the start of the game
    via the position of the player and the points
    """
    ram = self.get_ram()
    if ram[97] == 13 and ram[70] == 76 and ram[26] == 80:
        return True
    return False

def oxygen(self):
    """
    Changes the behavior of the oxygen bar
    by changing the corresponding ram positions
    """
    ram = self.get_ram()
    self.set_ram(102,64)
    if is_gamestart(self):
        self.set_ram(59, 3) # replace life if lost because of bug


def modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        if mod == "oxygen":
            step_modifs.append(oxygen)
        elif mod == "gravity":
            step_modifs.append(gravity)
        elif mod == "disable_enemies":
            step_modifs.append(disable_enemies)
    return step_modifs, reset_modifs