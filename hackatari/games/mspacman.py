from random import randint, choice

# Global Variables
TOGGLE_ORANGE = 0
TOGGLE_CYAN = 0
TOGGLE_PINK = 0
TOGGLE_RED = 0
NUMBER_POWER_PILLS = 4
LAST_PP_STATUS = 4
IS_INVERTED = False
LVL_NUM = 0
LIVES = 2

TIMER = 1

DOT_STATES = [59, 60, 61, 62, 65, 66, 67, 71, 72, 73, 83, 89, 90, 91, 92, 95, 98, 99, 100]

def make_edible(env, ghost_number,  x_pos, ram_x, y_pos, ram_y):
    ''' A helper function to make a certain ghost edible.
    The position is changed as well to avoid glitches.
    ghost_number: integer between 1 and 4 to choose between the 4 ghosts
    ram_x: integer which defines the ram cell in which the x-position is saved
    x_pos: integer which defines the new x-position of the ghost
    ram_y: integer which defines the ram cell in which the y-position is saved
    y_pos: integer which defines the new y-position of the ghost
    '''
    env.set_ram(ghost_number, 130)
    env.set_ram(ram_x, x_pos)
    env.set_ram(ram_y, y_pos)


def set_start_condition(self):
    ''' A helper function to set the start condition at the beginning of 
    each level/ after a reset'''
    # set the ghost to "edible" and change start location to avoid glitches
    # orange ghost
    make_edible(self, 1, 120, 6, 50, 12)
    # cyan ghost
    make_edible(self, 2, 100, 7, 50, 13)
    # pink ghost
    make_edible(self, 3, 80, 8, 50, 14)
    # red ghost
    make_edible(self, 4, 60 ,9, 50, 15)
    # set the timer to max number
    self.set_ram(116, 255)


def inverted_power_pill(self):
    ''' A helper function to make the ghost "normal" again.
    They will be able to eat Ms. Pacman for a certain amount of time.'''
    i = 1
    while i < 5:
        # make ghosts "normal"
        self.set_ram(i, 0)
        i += 1
    # set timer    
    self.set_ram(116, 62)


def power_pill_is_done(self):
    ''' A helper function to make all ghosts edible again.'''
    i = 1
    while i < 5:
        # make ghosts edible
        self.set_ram(i, 130)
        i += 1
    # set timer   
    self.set_ram(116, 190)


def static_ghosts(self):
    '''
    static_ghosts: Manipulates the RAM cell at position 6-9 and 12-15 to fix the position of
    the ghost inside the square in the middle of the screen.
    '''
    if TOGGLE_ORANGE:
        self.set_ram(6, 93)
        self.set_ram(12, 80)
    if TOGGLE_CYAN:
        self.set_ram(7, 83)
        self.set_ram(13, 80)
    if TOGGLE_PINK:
        self.set_ram(8, 93)
        self.set_ram(14, 67)
    if TOGGLE_RED:
        self.set_ram(9, 83)
        self.set_ram(15, 67)


def number_power_pills(self):
    '''
    number_power_pills: Manipulates the RAM cell at position 117 (= power pills), 
    62 and 95 (= edible tokens). Thus resulting in switching the specified
    number of power pills with normal edible tokens.
    is_at_start: a bool used as a switch to determine if the game was reset.
    current_lives: an integer used to store the current number of lives of Ms. Pacman
    '''

    if NUMBER_POWER_PILLS == 0: # no power pills
        self.set_ram(62, 80)
        self.set_ram(95, 80)
        self.set_ram(117, 0)
    elif NUMBER_POWER_PILLS == 1: # 1 power pill
        self.set_ram(62, 64)
        self.set_ram(95, 80)
        self.set_ram(117, 8)
    elif NUMBER_POWER_PILLS == 2: # two power pills
        self.set_ram(62, 0)
        self.set_ram(95, 80)
        self.set_ram(117, 40)
    elif NUMBER_POWER_PILLS == 3: # three power pills
        self.set_ram(62, 0)
        self.set_ram(95, 64)
        self.set_ram(117, 46)


def edible_ghosts(self):
    '''
    edible_ghosts: Manipulates the RAM cell at position 117 (= power pills), 
    62 and 95 (= edible tokens). Thus resulting in switching all power pills with 
    normal edible tokens.
    Furthermore all ghost will be made edible the entire game using RAM cell 1-4 
    (= ghost status) and the timer for the edible ghost mode (RAM cell 116)
    is_at_start: a bool used as a switch to determine if the game was reset.
    current_lives: an integer used to store the current number of lives of Ms. Pacman
    current_pp_status: an integer used to store the current status of the power pills
    current_timer: an integer used to store the current timer of the edible ghost mode
    current_orange: an integer used to store the current status of the orange ghost
    current_cyan: an integer used to store the current status of the orange ghost
    current_pink: an integer used to store the current status of the pink ghost
    current_red: an integer used to store the current status of the red ghost
    '''
    current_timer = self.get_ram()[116]

    current_orange = self.get_ram()[1]
    current_cyan = self.get_ram()[2]
    current_pink = self.get_ram()[3]
    current_red = self.get_ram()[4]


    # check if timer needs to be adjusted
    if current_timer < 250:
        self.set_ram(116, 255)

    # check if a ghost has been eaten and if needed make them edible again
    # change start location to avoid glitches
    if current_orange == 112:
        make_edible(self, 1, 120, 6, 50, 12)
    if current_cyan == 112:
        make_edible(self, 2, 100, 7, 50, 13)
    if current_pink == 112:
        make_edible(self, 3, 80, 8, 50, 14)
    if current_red == 112 or current_red == 0:
        make_edible(self, 4, 60 ,9, 50, 15)


def inverted_ms_pacman_reset(self):
    set_start_condition(self)
    global LAST_PP_STATUS, IS_INVERTED
    LAST_PP_STATUS = 63
    IS_INVERTED = False


def inverted_ms_pacman(self):
    '''
    inverted_ms_pacman: Manipulates the RAM cell at position 1-4 (= ghost status) so all 
    ghost will be edible the entire game until the player eats a power pill 
    (RAM 117 = power pill status). After eating a power pill the ghost will return to 
    "normal" for a certain amount of time (RAM cell 116 = timer).
    is_at_start: a bool used as a switch to determine if the game was reset.
    is_inverted: a bool used as a switch to determine the current game mode.
    last_pp_status: an integer used to save the last value in the RAM cell for 
    the power pills. The value is needed to determine if a power pill has been eaten.
    current_lives: an integer used to store the current number of lives of Ms. Pacman
    current_pp_status: an integer used to store the current status of the power pills
    current_timer: an integer used to store the current timer of the edible ghost mode
    current_orange: an integer used to store the current status of the orange ghost
    current_cyan: an integer used to store the current status of the orange ghost
    current_pink: an integer used to store the current status of the pink ghost
    current_red: an integer used to store the current status of the red ghost
    '''
    global LAST_PP_STATUS, IS_INVERTED
    current_pp_status = self.get_ram()[117]
    current_timer = self.get_ram()[116]

    current_orange = self.get_ram()[1]
    current_cyan = self.get_ram()[2]
    current_pink = self.get_ram()[3]
    current_red = self.get_ram()[4]
    
    # check if timer needs to be adjusted
    if current_timer < 250 and IS_INVERTED is False:
        self.set_ram(116, 255)

    # check if a power pill has been eaten
    # a range is required because the values in the RAm cells fluctuate
    if not((LAST_PP_STATUS - 3) < current_pp_status < (LAST_PP_STATUS + 3)):
        IS_INVERTED = True
        inverted_power_pill(self)
        LAST_PP_STATUS = current_pp_status

    # check if effect of power pill has run out
    if current_timer == 0:
        IS_INVERTED = False # disable switch
        power_pill_is_done(self)

    # check if a ghost has been eaten and if needed make them edible again
    # change start location to avoid glitches
    if current_orange == 112 and not IS_INVERTED:
        make_edible(self, 1, 120, 6, 50, 12)
    if current_cyan == 112 and not IS_INVERTED:
        make_edible(self, 2, 100, 7, 50, 13)
    if current_pink == 112 and not IS_INVERTED:
        make_edible(self, 3, 80, 8, 50, 14)
    if current_red == 112 and not IS_INVERTED:
        make_edible(self, 4, 60 ,9, 50, 15)

def change_level(self):
    """
    Changes the level according to the argument number 0-3. If not specified, selcts random level.
    """
    global LVL_NUM
    if LVL_NUM is None:
        LVL_NUM = randint(0, 3)
        print(f"Selecting Random Level {LVL_NUM}")
    self.set_ram(0, LVL_NUM)

def maze_man(self):
    self.set_ram(47, 0)
    ram = self.get_ram()

    collected = True

    for i in range(59, 101):
        if ram[i] != 0:
            collected = False

    if collected and ram[39] > 70:
        add = ram[120] + 32
        if add <= 144:
            self.set_ram(120, add)
        else:
            self.set_ram(120, 144)
        global DOT_STATES
        state = choice(DOT_STATES)
        bit = choice([0, 2])
        self.set_ram(state, 16<<bit)#1<<bit)
    
    global LVL_NUM, TIMER, LIVES
    if ram[39] == 69:
        if ram[0] == 0 and ram[119] == 154:
                LVL_NUM = 1
                if LIVES < 3:
                    LIVES+=1
                self.reset()
        elif ram[0] == 1 and ram[119] == 150:
                LVL_NUM = 2
                if LIVES < 3:
                    LIVES+=1
                self.reset()
        elif ram[0] == 2 and ram[119] == 158:
                LVL_NUM = 3
                if LIVES < 3:
                    LIVES+=1
                self.reset()
        elif ram[0] == 3 and ram[119] == 154:
                LVL_NUM = 0
                if LIVES < 3:
                    LIVES+=1
                self.reset()

    if ram[39] == 255 and TIMER == 0:
        if ram[120] < 16 and ram[123] <= 0:
            LVL_NUM = 0
            LIVES = 2
            self.reset()
        elif ram[120] < 16:
            LIVES-=1
            self.reset()
        else:
            self.set_ram(120, ram[120]-16)

    TIMER = (TIMER+1)%150

def maze_man_reset(self):
    global TIMER, LIVES
    TIMER = 1
    for i in range(59, 101):
        self.set_ram(i, 0)
    self.set_ram(19, 0)
    self.set_ram(117, 0)
    self.set_ram(119, 134)
    self.set_ram(120, 144)
    self.set_ram(123, LIVES)


def _modif_funcs(modifs):
    global TOGGLE_CYAN, TOGGLE_PINK, TOGGLE_ORANGE, TOGGLE_RED
    step_modifs, reset_modifs = [], []
    if "edible_ghosts" in modifs and "inverted" in modifs:
        raise ValueError("The modification \"ghosts_edible\" is unnecessary when playing in inverted mode")
    for mod in modifs:
        if mod == "caged_ghosts":
            TOGGLE_CYAN = True
            TOGGLE_ORANGE = True 
            TOGGLE_RED = True
            TOGGLE_PINK = True
            step_modifs.append(static_ghosts)
        elif mod == "disable_orange":
            TOGGLE_ORANGE = True
            step_modifs.append(static_ghosts)
        elif mod == "disable_red":
            TOGGLE_RED = True
            step_modifs.append(static_ghosts)
        elif mod == "disable_cyan":
            TOGGLE_CYAN = True
            step_modifs.append(static_ghosts)
        elif mod == "disable_pink":
            TOGGLE_PINK = True
            step_modifs.append(static_ghosts)
        elif mod.startswith("power"):
            mod_n = int(mod[-1])
            if mod_n < 0 or mod_n > 4:
                raise ValueError("Invalid Number of Power Pills, choose number 0-4")
            global NUMBER_POWER_PILLS
            NUMBER_POWER_PILLS = mod_n
            reset_modifs.append(number_power_pills)
        elif mod == "edible_ghosts":
            step_modifs.append(edible_ghosts)
        elif mod == "inverted":
            step_modifs.append(inverted_ms_pacman)
            reset_modifs.append(inverted_ms_pacman_reset)
        elif "change_level" in mod:
            if mod[-1].isdigit():
                global LVL_NUM
                LVL_NUM =  int(mod[-1])
                assert LVL_NUM < 4, "Invalid Level Number (0, 1, 2 or 3)"
            reset_modifs.append(change_level)
        elif mod == "maze_man":
            reset_modifs.append(change_level)
            TOGGLE_CYAN = True
            TOGGLE_ORANGE = True 
            TOGGLE_RED = True
            TOGGLE_PINK = True
            step_modifs.append(static_ghosts)
            step_modifs.append(maze_man)
            reset_modifs.append(maze_man_reset)
    return step_modifs, reset_modifs