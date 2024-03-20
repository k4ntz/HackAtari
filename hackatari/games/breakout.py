STRENGTH = 0
DRIFT = 0

def define_drift_strength():
    """
    Defines the drift strength of the ball
    according to the parsed arguement
    """
    global DRIFT
    DRIFT = 0

    if STRENGTH == 1:
        DRIFT = 2
    if STRENGTH == 2:
        DRIFT = 3

def right_drift(self):
    """
    Makes the ball drift to the rigth
    by changing the corresponding ram positions
    """
    ball_x = self.get_ram()[99]
    ball_y = self.get_ram()[101]
    new_ball_pos = ball_x + DRIFT
    #else the ball isnt there at all or outside of the walls
    if (ball_y + 9 <= 196 and new_ball_pos != 0) and 57 <= new_ball_pos <= 199:
        self.set_ram(99, new_ball_pos)

def left_drift(self):
    """
    Makes the ball drift to the left
    by changing the corresponding ram positions
    """
    ball_x = self.get_ram()[99]
    ball_y = self.get_ram()[101]
    new_ball_pos = ball_x - DRIFT
    #else the ball isnt there at all or outside of the walls
    if (ball_y + 9 <= 196 and new_ball_pos != 0) and 57 <= new_ball_pos <= 199:
        self.set_ram(99, new_ball_pos)

def modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        mod_n = int(mod[-1])
        if mod.startswith('d'):
            if mod_n == "r":
                step_modifs.append(right_drift)
            elif mod_n == "l":
                step_modifs.append(left_drift)
            else:
                raise ValueError("Invalid drift")
        elif mod.startswith('s'):
            global STRENGTH
            STRENGTH = mod_n
            step_modifs.append(define_drift_strength)
    return step_modifs, reset_modifs