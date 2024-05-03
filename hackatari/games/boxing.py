import random
TIMER = 0

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
    TIMER += 1
    if curr_player_pos < 87:
        if TIMER % 2:
            curr_player_pos += 1
            self.set_ram(34, curr_player_pos)

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

def modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        if mod == "gravity":
            step_modifs.append(gravity)
        elif mod == "one_armed":
            step_modifs.append(one_armed)
        elif mod == "drunken_boxing":
            step_modifs.append(drunken_boxing)
        else:
            raise ValueError("Invalid modification")
    return step_modifs, reset_modifs