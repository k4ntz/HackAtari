import random

global CURRENT_COLORS
global TIMER
CURRENT_COLORS = [random.randint(0, 200), random.randint(0, 200), random.randint(0, 200), random.randint(0, 200)]
TIMER = 0

def gravity(self):
    """
    Enables gravity for the player.
    """
    # makes game kinda unplayable
    ram = self.get_ram()
    global TIMER
    if ram[97] < 105 and not TIMER%5:
        self.set_ram(97, ram[97] + 1)
    TIMER +=1

def disable_enemies(self):
    # Has stray missiles/Divers seem to transform into enemy missiles sometimes
    """
    Disables all the enemies.
    """
    for x in range(4): # disables underwater enemies
        self.set_ram(36 + x, 0)
    self.set_ram(60, 0) # disables surface enemies


def is_gamestart(self):
    """
    Determines if it is the start of the game
    via the position of the player and the points
    """
    ram = self.get_ram()
    if ram[97] == 13 and ram[70] == 76 and ram[26] == 80:
        return True
    return False

def unlimited_oxygen(self):
    """
    Changes the behavior of the oxygen bar to remain filled
    by changing the corresponding ram positions
    """
    ram = self.get_ram()
    if ram[97] > 13: # when not surfacing
        self.set_ram(102, 63)
    if is_gamestart(self):
        self.set_ram(59, 3) # replace life if lost because of bug

def random_color_enemies(self):
    """
    The enemies have new random colors each time they go across the screen.
    """
    ram = self.get_ram()
    for i in range (4):
        if ram[30 + i] == 200: # if the enemy is not in frame
            CURRENT_COLORS[i] = random.randint(0, 255)
        self.set_ram(44 + i, CURRENT_COLORS[i])


def _modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        if mod == "unlimited_oxygen":
            step_modifs.append(unlimited_oxygen)
        elif mod == "gravity":
            step_modifs.append(gravity)
        elif mod == "disable_enemies":
            step_modifs.append(disable_enemies)
        if mod == "random_color_enemies":
            step_modifs.append(random_color_enemies)
    return step_modifs, reset_modifs