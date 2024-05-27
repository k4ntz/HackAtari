global count
count = 100
COLOR = 0

colors = [38, 40, 23, 86, 48]
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

def color(self):
    """
    Changes the color of background to [Black, White, Red, Blue, Green] by choosing a value 0-4. This also affects the enemies colors
    """
    global COLOR
    self.set_ram(117, colors[COLOR])


def _modif_funcs(modifs):
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
        elif mod.startswith("color"):
            if mod[-1].isdigit():
                mod_n = int(mod[-1])
                if mod_n < 0 or mod_n > 4:
                    raise ValueError("Invalid color value, choose value 0-4 [black, white, red, blue, green]")
            else:
                raise ValueError("Append value 0-4 [black, white, red, blue, green] to your color mod-argument")
            global COLOR
            COLOR = mod_n
            step_modifs.append(color)
    return step_modifs, reset_modifs