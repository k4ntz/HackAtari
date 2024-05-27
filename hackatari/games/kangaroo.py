import random



# Constants for clarity and maintainability
KANGAROO_POS_X_INDEX = 17  # RAM index for kangaroo's X position
KANGAROO_POS_Y_INDEX = 16  # RAM index for kangaroo's Y position
LEVEL_2 = 2
FLOOR = 0 

# Starting positions based on different conditions
FLOOR_1_LEVEL2_POS = (25, 10)
FLOOR_2_LEVEL2_POS = (100, 6)
FLOOR_1_START_POS = (65, 12)
FLOOR_2_START_POS = (65, 6)
ANY_FLOOR_INSTANT_WIN = (110, 0)

LVL_NUM = None

def disable_monkeys(self):
    """
    Disables the monkeys in the game
    by changing the corresponding ram positions
    """
    for x in range(4):
        self.set_ram(11 - x, 127)


def disable_coconut(self):
    """
    Disables the falling coconut in the game,
    by changing the corresponding ram positions
    """
    self.set_ram(33, 255)
    self.set_ram(35, 255)


def set_ram_kang_pos(self, pos_x, pos_y):
    """
    Set the kangaroo's position.
    Args:
    pos_x (int): The x-coordinate for the kangaroo's position.
    pos_y (int): The y-coordinate for the kangaroo's position.
    """
    self.set_ram(KANGAROO_POS_X_INDEX, pos_x)
    self.set_ram(KANGAROO_POS_Y_INDEX, pos_y)
    print("ram set")


def is_at_start(pos):
    """
    checks whether the given x and y coordinates are in the starting range of the kangaroo.
    Args:
    pos_x (int): The x-coordinate.
    pos_y (int): The y-coordinate.
    """
    return 5 < pos[0] < 11 and 16 < pos[1] < 21


def check_new_level_life(self, current_lives, current_level):
    """
    Checks whether the level or amount of lives changed
    and if either or both did re-enable the changing of the starting
    position and updating the current lives and level
    """
    if current_lives != self.last_lives or current_level != self.last_level:
        self.last_lives = current_lives
        self.last_level = current_level


def set_kangaroo_position(self):
    """
    Sets the kangaroo's starting position depending on the FLOOR argument.
    """
    import ipdb;ipdb.set_trace()
    ram = self.get_ram()
    current_level = ram[36]
    kangaroo_pos = (ram[KANGAROO_POS_X_INDEX], ram[KANGAROO_POS_Y_INDEX])
    
    if is_at_start(kangaroo_pos):
        if FLOOR == 1:
            # For floor 1, position depends on whether the current level is 2
            new_pos = FLOOR_1_LEVEL2_POS if current_level == LEVEL_2 else FLOOR_1_START_POS
            set_ram_kang_pos(self, *new_pos)
        elif FLOOR == 2:
            # For floor 2, position is set to a different location
            # but also depends on the current level
            new_pos = FLOOR_2_LEVEL2_POS if current_level == LEVEL_2 else FLOOR_2_START_POS
            set_ram_kang_pos(self, *new_pos)

def random_init(self):
    """
    Randomize the floor on which the player starts.
    """
    ram = self.get_ram()
    current_level = ram[36]
    current_lives = ram[45]
    kangaroo_pos = (ram[KANGAROO_POS_X_INDEX], ram[KANGAROO_POS_Y_INDEX])
    random_number = random.randint(0, 2)
    if is_at_start(kangaroo_pos):
        if random_number == 1:
            # For floor 1, position depends on whether the current level is 2
            new_pos = FLOOR_1_LEVEL2_POS if current_level == LEVEL_2 else FLOOR_1_START_POS
            set_ram_kang_pos(self, *new_pos)
        elif random_number == 2:
            # For floor 2, position is set to a different location
            # but also depends on the current level
            new_pos = FLOOR_2_LEVEL2_POS if current_level == LEVEL_2 else FLOOR_2_START_POS
            set_ram_kang_pos(self, *new_pos)


def change_level(self):
    """
    Changes the level according to the argument number 0-2. If not specified, selcts random level.
    """
    global LVL_NUM
    if LVL_NUM is None:
        LVL_NUM = random.randint(0, 3)
        print(f"Selcting Random Level {LVL_NUM}")
    self.set_ram(36, LVL_NUM)


def _modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    if "random_init" in modifs and "easy_mode" in modifs:
        raise ValueError("Both random_init and easy_mode cannot be enabled at the same time")
    for mod in modifs:
        if mod == "disable_monkeys":
            step_modifs.append(disable_monkeys)
        elif mod == "disable_coconut":
            step_modifs.append(disable_coconut)
        elif mod == "random_init":
            reset_modifs.append(random_init)
        elif "set_floor" in mod:
            if mod[-1].isdigit():
                global FLOOR
                FLOOR = int(mod[-1])
            reset_modifs.append(set_kangaroo_position)
        # elif mod == "easy_mode":
        #     reset_modifs.append(easy_mode)
        elif "change_level" in mod:
            if mod[-1].isdigit():
                global LVL_NUM
                LVL_NUM =  int(mod[-1])
                assert LVL_NUM < 3, "Invalid Level Number (0, 1 or 2)"
            reset_modifs.append(change_level)
    return step_modifs, reset_modifs