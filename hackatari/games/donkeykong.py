import random
NBLIVES = 2

def _randomize_pos(self):
        pot_start_pos = [(49, 154), (110, 154), (49, 127), (111, 132), (111, 99),
                         (50, 71), (53, 48), (111, 43), (111, 21)]
                        
        rndinit = random.randint(0, len(pot_start_pos))
        self._env.step(1) # activate the game
        [self._env.step(0) for _ in range(8)] 
        startp = pot_start_pos[rndinit]
        for rp, sp in zip([19, 27], startp):
            self.set_ram(rp, sp)
        self.lasty = startp[1]

def no_barrel(self):
    # if self.get_ram()[16] == 0:
    self.set_ram(25, 255)

def unlimited_time(self):
    # if self.get_ram()[16] == 0:
    self.set_ram(36, 70)

def random_start_step(self):
    global NBLIVES
    ram = self.get_ram()
    if NBLIVES != ram[35]:
        _randomize_pos(self)
        NBLIVES = ram[35]

def _modif_funcs(env, modifs):
    
    for mod in modifs:
        if mod == "no_barrel":
            env.step_modifs.append(no_barrel)
        if mod == "unlimited_time":
            env.step_modifs.append(unlimited_time)
        elif mod == "random_start":
            env.reset_modifs.append(_randomize_pos)
            env.step_modifs.append(random_start_step)
        else:
            print('Invalid modification')
    
