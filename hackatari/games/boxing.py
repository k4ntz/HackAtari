import random
TIMER = 0
global GRAVITY
GRAVITY = 3
PLAYER_COLOR = 0 # Black, Red, Blue, Green
ENEMY_COLOR = 0 # White, Red, Blue, Green
ONCE = 0

colors = [0, 12, 48, 113, 200]

def one_armed(self):
    '''
    one_armed_boxing: disables the "hitting motion" with the right arm permanently
    '''
    self.set_ram(101, 128) 

def gravity(self):
    '''
    gravity_boxing: Increase the value in RAM cell 34 until reaching a certain threshold
    '''
    curr_player_pos = self.get_ram()[34]
    global TIMER
    if curr_player_pos < 87:
        global GRAVITY
        if not TIMER % GRAVITY:
            curr_player_pos += 1
            self.set_ram(34, curr_player_pos)
    TIMER += 1

    # if TOGGLE_HUMAN_MODE:
    #     if curr_player_pos < 87 and not (pygame.K_w in list(self.current_keys_down)):
    #         curr_player_pos += 1
    #         self.set_ram(34, curr_player_pos)

def offensive(self):
    '''
    Moves the player character forward in the game environment.
    '''
    curr_player_pos_x = self.get_ram()[32]
    curr_player_pos_x_enemy = self.get_ram()[33]

    if 0 < curr_player_pos_x < 109 and curr_player_pos_x + 14 != curr_player_pos_x_enemy:
        curr_player_pos_x += 1
        self.set_ram(32, curr_player_pos_x)

def antigravity(self):
    '''
    Moves the player character up in the game environment.
    '''
    curr_player_pos_y = self.get_ram()[34]

    if 0 < curr_player_pos_y < 87:
        curr_player_pos_y -= 1
        self.set_ram(34, curr_player_pos_y)

def defensive(self):
    '''
    Moves the player character backward in the game environment.
    '''
    curr_player_pos_x = self.get_ram()[32]

    if 0 < curr_player_pos_x < 109:
        curr_player_pos_x -= 1
        self.set_ram(32, curr_player_pos_x)

def down(self):
    '''
    Moves the player character down in the game environment.
    '''
    curr_player_pos_y = self.get_ram()[34]

    if 0 < curr_player_pos_y < 87:
        curr_player_pos_y += 1
        self.set_ram(34, curr_player_pos_y)


def drunken_boxing(self):
    '''
    Applies random movements to the players input
    '''
    r = random.randint(0,1)
    if r == 0:
        # Add a counter variable to keep track of the function calls
        self.counter = getattr(self, 'counter', 0)
        do = self.counter % 4
        # Increment the counter for the next function call
        self.counter += 1
    else:
        do = random.randint(0,3)
    
    # Call functions in sequence based on the counter value
    if do == 0:
        offensive(self)
    elif do == 1:
        antigravity(self)
    elif do == 2:
        defensive(self)
    elif do == 3:
        down(self)


def color_player(self):
    '''
    Changes the color of the player to [Black, White, Red, Blue, Green] by choosing a value 0-4
    '''
    self.set_ram(1, colors[PLAYER_COLOR])

def color_enemy(self):
    '''
    Changes the color of the enemy to [Black, White, Red, Blue, Green] by choosing a value 0-4
    '''
    self.set_ram(2, colors[ENEMY_COLOR])


def switch_positions(self):
    '''
    Switches the position of player and enemy
    '''
    global ONCE
    if ONCE:
        self.set_ram(33, 30)
        self.set_ram(35, 4)
        # 109, 87
        self.set_ram(32, 105)
        self.set_ram(34, 85)
        ONCE -= 1

def reset_onc(self):
    global ONCE
    ONCE = 2


def _modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        if mod.startswith("gravity"):
            if mod[-1].isdigit():
                global GRAVITY
                GRAVITY = 7-int(mod[-1])
                assert 1 < GRAVITY < 7, "Invalid Gravity lelvel, choose number 1-5"
            step_modifs.append(gravity)
        elif mod == "one_armed":
            step_modifs.append(one_armed)
        elif mod == "drunken_boxing":
            step_modifs.append(drunken_boxing)
        elif mod.startswith("color_p"):
            if mod[-1].isdigit():
                mod_n = int(mod[-1])
                if mod_n:
                    mod_n += 1
                if mod_n < 0 or mod_n > 3:
                    raise ValueError("Invalid color for player, choose value 0-3 [black, red, blue, green]")
            else:
                raise ValueError("Append value 0-3 [black, red, blue, green] to your color mod-argument")
            global PLAYER_COLOR
            PLAYER_COLOR = mod_n
            step_modifs.append(color_player)
        elif mod.startswith("color_e"):
            if mod[-1].isdigit():
                mod_n = int(mod[-1]) + 1
                if mod_n < 0 or mod_n > 3:
                    raise ValueError("Invalid color for player, choose value 0-3 [white, red, blue, green]")
            else:
                raise ValueError("Append value 0-3 [white, red, blue, green] to your color mod-argument")
            global ENEMY_COLOR
            ENEMY_COLOR = mod_n
            step_modifs.append(color_enemy)
        elif mod.startswith("switch_p"):
            step_modifs.append(switch_positions)
            reset_modifs.append(reset_onc)
        else:
            raise ValueError("Invalid modification")
    return step_modifs, reset_modifs