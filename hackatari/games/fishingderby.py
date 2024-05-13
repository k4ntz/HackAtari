FISH_MODE = 0 # Give the fishes an area to swim in (Int: 0-3)
SHARK_MODE = 0 # Give the shark an area to swim in (Int: 0-4)

def alter_shark(self):
    '''
    alter_shark: Allows for alterations in the behavior of the shark as specified
    by the corresponding command line option
    '''
    # shark modes
    if SHARK_MODE > 0:
        # shark mode: no movement easy
        if SHARK_MODE == 1:
            self.set_ram(75, 105)
        # shark mode: no movement hard
        if SHARK_MODE == 2:
            self.set_ram(75, 25)
        # shark mode: teleport
        if SHARK_MODE == 3:
            current_x_position = self.get_ram()[75]
            if current_x_position == 100:
                self.set_ram(75, 25)
            if current_x_position == 30:
                self.set_ram(75, 105)
        # shark mode: speed mode
        if SHARK_MODE == 4:
            current_x_position = self.get_ram()[75]
            if current_x_position < 120:
                self.set_ram(75, current_x_position+5)
            if current_x_position > 120:
                self.set_ram(75, 1)

def alter_fish(self):
    '''
    alter_fishes: Allows for alterations in the behavior of the fish as specified
    by the corresponding command line option
    '''
    # fish modes
    if FISH_MODE > 0:
        # fish mode 1: fish are all on player's side
        if FISH_MODE == 1:
            for i in range(6):
                if self.get_ram()[69+i] > 86:
                    self.set_ram(69+i, 44)
        # # fish mode 2: fish are all on enemy's side
        # if FISH_MODE == 2:
        #     for i in range(6):
        #         if self.get_ram()[69+i] < 70:
        #             self.set_ram(69+i, 116)
        # fish mode 3: fish are always in the middle between player and enemy
        if FISH_MODE == 3:
            for i in range(6):
                if self.get_ram()[112] != i+1 or self.get_ram()[113] != i+1:
                    if self.get_ram()[69+i] < 70:
                        self.set_ram(69+i, 86)
                    if self.get_ram()[69+i] > 86:
                        self.set_ram(69+i, 70)

def _modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        mod_n = int(mod[-1])
        if mod.startswith('f'):
            global FISH_MODE
            FISH_MODE = mod_n
            step_modifs.append(alter_fish)
        elif mod.startswith('s'):
            global SHARK_MODE
            SHARK_MODE = mod_n
            step_modifs.append(alter_shark)
    return step_modifs, reset_modifs