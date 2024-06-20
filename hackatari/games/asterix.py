SPEED = 0

def obelix(self):
    ram = self.set_ram(54, 5)

def set_speed(self):
    global SPEED
    ram = self.set_ram(54, SPEED)

def unlimited_lives(self):
    self.set_ram(83, 3)


def even_lines_free(self):
    for i in range(1, 9, 2):
        self.set_ram(73+i, i+1)
        self.set_ram(18-i, 11)

def odd_lines_free(self):
    for i in range(0, 8, 2):
        self.set_ram(73+i, i+1)
        self.set_ram(18-i, 11)

def _modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    global SPEED
    for mod in modifs:
        if mod == "obelix":
            step_modifs.append(obelix)
            SPEED += 4
        elif mod.startswith("speed"):
            mod_n = int(mod[-1])
            SPEED += 8 * mod_n
            step_modifs.append(set_speed)
        elif mod == "unlimited_lives":
            step_modifs.append(unlimited_lives)
        elif mod == "even_lines_free":
            step_modifs.append(even_lines_free)
        elif mod == "odd_lines_free":
            step_modifs.append(odd_lines_free)
        else:
            print('Invalid modification')
    return step_modifs, reset_modifs