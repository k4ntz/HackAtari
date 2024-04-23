LAST_ENEMY_Y_POS = 127
BALL_PREVIOUS_X_POS = 130

def lazy_enemy(self):
    """
    Enemy does not move after returning the shot.
    """
    ram = self.get_ram()
    global LAST_ENEMY_Y_POS, BALL_PREVIOUS_X_POS
    if 0 < ram[11] < 5:
        self.set_ram(21, 127)
        self.set_ram(49, 130)
    if BALL_PREVIOUS_X_POS < ram[49]:
        self.set_ram(21, LAST_ENEMY_Y_POS)
    BALL_PREVIOUS_X_POS = ram[49]
    LAST_ENEMY_Y_POS = ram[21]


def modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        if mod == "lazy_enemy":
            step_modifs.append(lazy_enemy)
        # elif mod == "gravity":
        #     step_modifs.append(gravity)
        # elif mod == "disable_enemies":
        #     step_modifs.append(disable_enemies)
    return step_modifs, reset_modifs