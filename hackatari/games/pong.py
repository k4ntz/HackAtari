LAST_ENEMY_Y_POS = 127
BALL_PREVIOUS_X_POS = 130

STRENGTH = 6
TIMER = 0

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

def up_drift(self):
    """
    Makes the ball drift upwards by changing the corresponding ram positions
    """
    # ball_x = self.get_ram()[49]
    ball_y = self.get_ram()[54]
    new_ball_pos = ball_y - 1

    global TIMER
    #else the ball isnt there at all or outside of the walls
    if ball_y != 0 and not TIMER%STRENGTH: # if (ball_y + 9 <= 196 and new_ball_pos != 0) and 57 <= new_ball_pos <= 199 and not TIMER%10:
        self.set_ram(54, new_ball_pos)
    TIMER +=1

def down_drift(self):
    """
    Makes the ball drift downwards by changing the corresponding ram positions
    """
    # ball_x = self.get_ram()[49]
    ball_y = self.get_ram()[54]
    new_ball_pos = ball_y + 1

    global TIMER
    #else the ball isnt there at all or outside of the walls
    if ball_y != 0 and not TIMER%STRENGTH: # if (ball_y + 9 <= 196 and new_ball_pos != 0) and 57 <= new_ball_pos <= 199 and not TIMER%10:
        self.set_ram(54, new_ball_pos)
    TIMER +=1

def right_drift(self):
    """
    Makes the ball drift to the right by changing the corresponding ram positions
    """
    ball_x = self.get_ram()[49]
    # ball_y = self.get_ram()[54]
    new_ball_pos = ball_x + 1

    global TIMER
    #else the ball isnt there at all or outside of the walls
    if ball_x != 0 and not TIMER%STRENGTH: # if (ball_y + 9 <= 196 and new_ball_pos != 0) and 57 <= new_ball_pos <= 199 and not TIMER%10:
        self.set_ram(49, new_ball_pos)
    TIMER +=1

def left_drift(self):
    """
    Makes the ball drift to the left by changing the corresponding ram positions
    """
    ball_x = self.get_ram()[49]
    # ball_y = self.get_ram()[54]
    new_ball_pos = ball_x - 1

    global TIMER
    #else the ball isnt there at all or outside of the walls
    if ball_x != 0 and not TIMER%STRENGTH: # if (ball_y + 9 <= 196 and new_ball_pos != 0) and 57 <= new_ball_pos <= 199 and not TIMER%10:
        self.set_ram(49, new_ball_pos)
    TIMER +=1

def _modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        if mod == "lazy_enemy":
            step_modifs.append(lazy_enemy)
        else:
            if mod[-1].isdigit():
                global STRENGTH
                mod_n = int(mod[-1])
                assert 0 < mod_n < 6, "Invalid Gravity lelvel, choose number 1-5"
                mod_n = 6 - mod_n
                if mod_n == 1:
                    STRENGTH = 3
                else:
                    STRENGTH = mod_n*2
            if mod.startswith("up_drift"):
                step_modifs.append(up_drift)
            elif mod.startswith("down_drift"):
                step_modifs.append(down_drift)
            elif mod.startswith("left_drift"):
                step_modifs.append(left_drift)
            elif mod.startswith("right_drift"):
                step_modifs.append(right_drift)
        # elif mod == "gravity":
        #     step_modifs.append(gravity)
        # elif mod == "disable_enemies":
        #     step_modifs.append(disable_enemies)
            else:
                print('Invalid modification')
    return step_modifs, reset_modifs
