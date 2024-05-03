import random

NB_LIFES = 5
poses = ((77, 235), (88, 192), (128, 192), (133, 148), (33, 148), (22, 192))
BASE_DELAY = 108
DELAY = BASE_DELAY
DEAD = False

def random_position_start_res(self):
    """
    Enemy does not move after returning the shot.
    """
    if ram[3] == 1:
        global NB_LIFES
        ram = self.get_ram()
        NB_LIFES = ram[58]
        pos = random.choice(poses)
        pos = poses[5]
        for i, ram_n in enumerate([42, 43]):
            self.set_ram(ram_n, pos[i])


def random_position_start(self):
    if ram[3] == 1:
        global NB_LIFES, DEAD
        ram = self.get_ram()
        if ram[58] == NB_LIFES - 1 or DEAD: # life lost
            DEAD = True
        if DEAD:
            if ram[2] == 4:
                pos = poses[1]
                NB_LIFES = ram[58]
                for i, ram_n in enumerate([42, 43]):
                    self.set_ram(ram_n, pos[i])
                DEAD = False


def modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        if mod == "random_position_start":
            step_modifs.append(random_position_start)
            reset_modifs.append(random_position_start_res)
        else:
            print('Invalid modification')
    return step_modifs, reset_modifs
