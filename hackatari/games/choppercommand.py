global count
count = 100

def delay_shots(self):
    """
    Puts time delay between shots
    """
    global count
    if count == 100 and (self._get_action() == 1 or self._get_action() >= 10):
        count = 0
    elif 25 < count < 100:
        for ram_n in [49,52,55,58,61,64]:
            self.set_ram(ram_n, 0)
        self.set_ram(45, 0)
    if count < 100:
        count += 1
    
def no_enemies(self):
    """
    Removes all Enemies from the game
    """
    for ram_n in range(6,13):
        self.set_ram(ram_n, 0)

def no_radar(self):
    """
    Removes the radar content
    """
    # self.set_ram(117, 8)
    self.set_ram(118, 37)

def invisible_player(self):
    """
    Makes the player invisible
    """
    self.set_ram(118, 38)


def modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        if mod == "delay_shots":
            step_modifs.append(delay_shots)
        elif mod == "no_enemies":
            step_modifs.append(no_enemies)
        elif mod == "no_radar":
            step_modifs.append(no_radar)
        elif mod == "invis_player":
            step_modifs.append(invisible_player)
    return step_modifs, reset_modifs