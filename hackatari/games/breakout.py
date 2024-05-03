STRENGTH = 0 # How strong is the drift
global TIMER
TIMER = 0

def right_drift(self):
    """
    Makes the ball drift to the rigth by changing the corresponding ram positions
    """
    ball_x = self.get_ram()[99]
    ball_y = self.get_ram()[101]
    new_ball_pos = ball_x + STRENGTH

    global TIMER
    #else the ball isnt there at all or outside of the walls
    if (ball_y + 9 <= 196 and new_ball_pos != 0) and 57 <= new_ball_pos <= 199 and not TIMER%10:
        self.set_ram(99, new_ball_pos)
    TIMER +=1
    

def left_drift(self):
    """
    Makes the ball drift to the left by changing the corresponding ram positions
    """
    ball_x = self.get_ram()[99]
    ball_y = self.get_ram()[101]
    new_ball_pos = ball_x - STRENGTH

    global TIMER
    #else the ball isnt there at all or outside of the walls
    if (ball_y + 9 <= 196 and new_ball_pos != 0) and 57 <= new_ball_pos <= 199 and not TIMER%10:
        self.set_ram(99, new_ball_pos)
    TIMER +=1

def modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        if mod.startswith('s'):
            global STRENGTH
            mod_n = int(mod[-1])
            STRENGTH = mod_n
        elif mod.startswith('d'):
            if mod[-1] == "r":
                step_modifs.append(right_drift)
            elif mod[-1] == "l":
                step_modifs.append(left_drift)
            else:
                raise ValueError("Invalid drift")
    return step_modifs, reset_modifs