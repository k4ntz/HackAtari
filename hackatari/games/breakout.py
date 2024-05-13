STRENGTH = 2 # How strong is the drift
global TIMER
TIMER = 0
PLAYER_COLOR = 0 # Black, White, Red, Blue, Green
BLOCK_COLOR = 0 # Black, White, Red, Blue, Green
ROW_COLORS = [None] *6

colors = [0, 12, 48, 113, 200]

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

def gravity(self):
    """
    Pull the ball down by changing the corresponding ram positions
    """
    # ball_x = self.get_ram()[99]
    ball_y = self.get_ram()[101]
    new_ball_pos = ball_y + STRENGTH

    global TIMER
    #else the ball isnt there at all or outside of the walls
    if 90 <= new_ball_pos <= 165 and not TIMER%10:
        self.set_ram(101, new_ball_pos)
    TIMER +=1

def inverse_gravity(self):
    """
    Pushes the ball up by changing the corresponding ram positions
    """
    # ball_x = self.get_ram()[99]
    ball_y = self.get_ram()[101]
    new_ball_pos = ball_y - STRENGTH

    global TIMER
    #else the ball isnt there at all or outside of the walls
    if 90 <= new_ball_pos <= 180 and not TIMER%10:
        self.set_ram(101, new_ball_pos)
    TIMER +=1

def color_player(self):
    """
    Changes the color of the player to [Black, White, Red, Blue, Green] by choosing a value 0-4
    """
    self.set_ram(62, colors[PLAYER_COLOR])

# 64-69 block colors
def color_block(self):
    """
    Changes the color of all blocks to [Black, White, Red, Blue, Green] by choosing a value 0-4
    """
    for i in range(64, 70):
        self.set_ram(i, colors[BLOCK_COLOR])

def color_rows(self):
    """
    Changes the color of the specified block rows to [Black, White, Red, Blue, Green] by choosing a value 0-5 to specify which row to color and 0-4 to specify its color
    """
    for i in range(6):
        if ROW_COLORS[i] is not None:
            self.set_ram(64+i, ROW_COLORS[i])

def _modif_funcs(modifs):
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
                raise ValueError("Invalid drift, choose 'l' or 'r'")
        elif mod == "gravity":
            step_modifs.append(gravity)
        elif mod == "inverse_gravity":
            step_modifs.append(inverse_gravity)
        elif mod.startswith("color_p"):
            if mod[-1].isdigit():
                mod_n = int(mod[-1])
                if mod_n < 0 or mod_n > 4:
                    raise ValueError("Invalid color for player, choose value 0-4 [black, white, red, blue, green]")
            else:
                raise ValueError("Append value 0-4 [black, white, red, blue, green] to your color mod-argument")
            global PLAYER_COLOR
            PLAYER_COLOR = mod_n
            step_modifs.append(color_player)
        elif mod.startswith("color_b"):
            if mod[-1].isdigit():
                mod_n = int(mod[-1])
                if mod_n < 0 or mod_n > 4:
                    raise ValueError("Invalid color for block, choose value 0-4 [black, white, red, blue, green]")
            else:
                raise ValueError("Append value 0-4 [black, white, red, blue, green] to your color mod-argument")
            global BLOCK_COLOR
            BLOCK_COLOR = mod_n
            step_modifs.append(color_block)
        elif mod.startswith("color_r"):
            has_value = False
            for i in range(7,len(mod)-1):
                if mod[i].isdigit() and mod[i+1].isdigit():
                    mod_r, mod_v = int(mod[i]), int(mod[i+1])
                    if mod_r < 0 or mod_r > 5 or mod_v < 0 or mod_v > 4:
                        raise ValueError("Invalid color and row value\
                                          \nExample: Use 'color_r01-54' to make the bottom row of blocks white and the top row of blocks green\
                                          \n'color_r01-54' == 'color_r0154' and color values 0-4 [black, white, red, blue, green]")
                    else:
                        ROW_COLORS[mod_r] = colors[mod_v]
                        has_value = True
                        i+=1
            if not has_value:
                raise ValueError("Invalid color and row value\
                                  \nExample: Use 'color_r01-54' to make the bottom row of blocks white and the top row of blocks green.\
                                  \n'color_r01-54' == 'color_r0154' and color values 0-4 [black, white, red, blue, green]")
            step_modifs.append(color_rows)
    return step_modifs, reset_modifs