import random
TYPES = [32, 64, 80]
TYPE_STATE = [0, 0, 0, 0]

SPEED = 2

def no_last_line(self):
    '''
    Removes enemies from the last (lowest) line.
    '''
    self.set_ram(36, 0)

def jets_only(self):
    """
    Replaces all enemies with Bandit-Bombers
    """
    ram = self.get_ram()
    for i in range(4):
        if ram[82-i] and ram[82-i] < 80:
            self.set_ram(82-i, 80)
            if ram[78-i] == 1:
                self.set_ram(78-i, 2)
            elif ram[78-i] == 255:
                self.set_ram(78-i, 254)

def random_enemies(self):
    """
    Randomly assigns enemy types, instead of following the standardized pattern.
    """
    ram = self.get_ram()
    global TYPES, TYPE_STATE
    for i in range(4):
        if ram[79+i] and ram[79+i] < 81 and ram[79+i] != TYPE_STATE[i]:
            enemy = random.choice(TYPES)
            self.set_ram(79+i, enemy)
            if enemy < 80:
                if ram[75+i] == 2:
                    self.set_ram(75+i, 1)
                elif ram[75+i] == 254:
                    self.set_ram(75+i, 255)
            else:
                if ram[75+i] == 1:
                    self.set_ram(75+i, 2)
                elif ram[75+i] == 255:
                    self.set_ram(75+i, 254)
    TYPE_STATE = ram[79:83]

def speed_mode(self):
    """
    Increases the speed of all enemy ships according to the mod argument.
    """
    ram = self.get_ram()
    global SPEED
    for i in range(4):
        if ram[79+i] == 80:
            if ram[75+i]&128:
                self.set_ram(75+i, 255-SPEED)
            elif ram[75+i] > 0:
                self.set_ram(75+i, 1+SPEED)
        else:
            if ram[75+i]&128:
                self.set_ram(75+i, 256-SPEED)
            elif ram[75+i] > 0:
                self.set_ram(75+i, SPEED)


def _modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        if mod == "no_last_line":
            step_modifs.append(no_last_line)
        elif mod == "jets_only":
            step_modifs.append(jets_only)
        elif mod == "randomize_enemies":
            step_modifs.append(random_enemies)
        elif mod.startswith("speed_mode"):
            print(mod[-1])
            if mod[-1].isdigit():
                mod_n = int(mod[-1])
                if mod_n < 2 or mod_n > 10:
                    raise ValueError("Invalid value, choose speed value 2-10")
                global SPEED
                SPEED = mod_n
            elif mod[-1] == 'e':
                pass
            else:
                raise ValueError("Append value 2-10 to your mod-argument to increase speed accordingly")
            
            step_modifs.append(speed_mode)
        else:
            print('Invalid or unknown modification')
    return step_modifs, reset_modifs

