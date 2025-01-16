# from random import random
REPEAT = True
BIT = 7

TIMER = 50


def endeless_oxygen(self):
    '''
    Player can no longer run out of oxygen. Will not be set at max, so oxygen can always be picked up
    '''
    self.set_ram(113, 255)


def infinte_lives(self):
    '''
    Always maximizes the treasure value (represents the remaining lives)
    '''
    self.set_ram(73, 3)


def double_wave_length(self):
    '''
    Doubles the time of each wave
    '''
    global REPEAT
    ram = self.get_ram()
    if REPEAT:
        global BIT
        try:
            if ram[114] and not ram[114] & (2**BIT):
                self.set_ram(114, ram[114] | (2**BIT))
                REPEAT = False
            elif not ram[114] and not ram[115] & (2**BIT):
                self.set_ram(115, ram[115] | (2**BIT))
                REPEAT = False
        except:
            pass
    else:
        if ram[114] and not ram[114] & (2**BIT):
            BIT -= 1
            REPEAT = True
        elif not ram[114] and ram[115] & (2**BIT):
            BIT += 1
            REPEAT = True


def quick_start(self):
    """
    Skips the intro and starts the game at once
    """
    self.set_ram(65, 10)

# def octo_start(self):
#     """
#     Adds the first lane of tentacles for the octopus
#     """
#     global TIMER
#     if TIMER:
#         for i in range(5):
#             self.set_ram(9+(10*i), 64)
#         TIMER-=1

# def octo_rest(self):
#     global TIMER
#     TIMER = 20


def _modif_funcs(env, modifs):
    for mod in modifs:
        if mod == "endeless_oxygen":
            env.step_modifs.append(endeless_oxygen)
        elif mod == "infinte_lives":
            env.step_modifs.append(infinte_lives)
        elif mod == "double_wave_length":
            env.step_modifs.append(double_wave_length)
        elif mod == "quick_start":
            env.reset_modifs.append(quick_start)
        # elif mod == "octo_start":
        #     env.reset_modifs.append(quick_start)
        #     env.reset_modifs.append(octo_rest)
        else:
            print('Invalid or unknown modification')
