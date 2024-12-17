import random
import numpy as np
from ocatari.ram.kangaroo import Ladder


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

VIRTUAL_RAM_19 = 0
LADDER_X = None
KANGAROO_Y = 18
START = False
CLIMBING_VIRTUAL_RAM = 39

ADDED_LADDERS_POSES = None
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


def disable_thrown_coconut(self):
    """
    Disables the falling coconut in the game,
    by changing the corresponding ram positions
    """
    self.set_ram(25, 255)
    self.set_ram(28, 255)
    self.set_ram(31, 0)


def set_ram_kang_pos(self, pos_x, pos_y):
    """
    Set the kangaroo's position.
    Args:
    pos_x (int): The x-coordinate for the kangaroo's position.
    pos_y (int): The y-coordinate for the kangaroo's position.
    """
    if not self._already_reset:
        self.set_ram(KANGAROO_POS_X_INDEX, pos_x)
        self.set_ram(KANGAROO_POS_Y_INDEX, pos_y)
        self.set_ram(33, 255)
        self._already_reset = True


def _check_reseted(self):
    y_pos = self.get_ram()[16]
    if y_pos == 0 or y_pos == 22:
        self.set_ram(33, 255)
        self._already_reset = False


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


def unlimited_time(self):
    """
    Set the time to unlimited.
    """
    self.set_ram(59, 32)


def set_kangaroo_position(self):
    """
    Sets the kangaroo's starting position depending on the FLOOR argument.
    """
    ram = self.get_ram()
    current_level = ram[36]
    kangaroo_pos = (ram[KANGAROO_POS_X_INDEX], ram[KANGAROO_POS_Y_INDEX])
    if is_at_start(kangaroo_pos):
        if FLOOR == 1:
            # For floor 1, position depends on whether the current level is 2
            new_pos = (
                FLOOR_1_LEVEL2_POS if current_level == LEVEL_2 else FLOOR_1_START_POS
            )
            set_ram_kang_pos(self, *new_pos)
        elif FLOOR == 2:
            # For floor 2, position is set to a different location
            # but also depends on the current level
            new_pos = (
                FLOOR_2_LEVEL2_POS if current_level == LEVEL_2 else FLOOR_2_START_POS
            )
            set_ram_kang_pos(self, *new_pos)


def random_init(self):
    """
    Randomize the floor on which the player starts.
    """
    ram = self.get_ram()
    current_level = ram[36]
    kangaroo_pos = (ram[KANGAROO_POS_X_INDEX], ram[KANGAROO_POS_Y_INDEX])
    if is_at_start(kangaroo_pos):
        random_number = random.randint(0, 2)
        if random_number == 1:
            # For floor 1, position depends on whether the current level is 2
            new_pos = (
                FLOOR_1_LEVEL2_POS if current_level == LEVEL_2 else FLOOR_1_START_POS
            )
            set_ram_kang_pos(self, *new_pos)
        elif random_number == 2:
            # For floor 2, position is set to a different location
            # but also depends on the current level
            new_pos = (
                FLOOR_2_LEVEL2_POS if current_level == LEVEL_2 else FLOOR_2_START_POS
            )
            set_ram_kang_pos(self, *new_pos)
        elif random_number == 0:
            self._already_reset = True


def change_level(self):
    """
    Changes the level according to the argument number 0-2. If not specified, selcts random level.
    """
    global LVL_NUM
    if LVL_NUM is None:
        LVL_NUM = random.randint(0, 3)
        print(f"Selcting Random Level {LVL_NUM}")
    self.set_ram(36, LVL_NUM)


def remove_original_ladder_inpaintings():
    background_color = np.array((80, 0, 132))
    w, h = 8, 36
    patch = (np.ones((h, w, 3)) * background_color).astype(np.uint8)
    ladder_poses = [(132, 36), (132, 132), (20, 84)]
    # needs swapped positions
    return [(y, x, h, w, patch) for x, y in ladder_poses]


def _on_ladder(px, py, ladders):
    # py = feet position of kangaroo
    for ladder in ladders:
        if abs(px - ladder[0]) < 4 and ladder[1] - 9 <= py < ladder[1] + 40:
            return True
    return False


def removed_ladder_step(self):
    ram = self.get_ram()
    y_ram = ram[16]
    y_pos = y_ram * 8 + 4
    x_pos = ram[17] + 15
    climbing = ram[18]
    py = y_pos + 24  # feet position
    if ram[18] in [20, 28]:
        py -= 8  # ducking
    if _on_ladder(x_pos, py, self._removed_ladders_poses):
        if climbing == 47:
            self.set_ram(18, 73)
            self.set_ram(16, y_ram + 1)
        elif climbing == 39:
            self.set_ram(18, 65)
            self.set_ram(16, y_ram + 1)


def added_ladder_step(self):
    ram = self.get_ram()
    y_ram = ram[16]
    y_pos = y_ram * 8 + 4
    x_pos = ram[17] + 15
    py = y_pos + 24  # feet position
    if ram[18] in [20, 28]:
        py -= 8  # ducking
    global VIRTUAL_RAM_19, LADDER_X, KANGAROO_Y, START
    if _on_ladder(x_pos, py - 1, ADDED_LADDERS_POSES):
        global CLIMBING_VIRTUAL_RAM
        if LADDER_X is not None and ram[114] not in [21, 15, 9]:
            self.set_ram(17, LADDER_X)
        if ram[16] < KANGAROO_Y:  # climbing up
            print("Climbing Up")
            if ram[18] & 64:
                self.set_ram(18, ram[18] & (not 64) | 32)
                self.set_ram(16, KANGAROO_Y)
            elif ram[16] < 19 and ram[16] & 1:
                self.set_ram(18, 39)
            elif ram[16] < 19:
                self.set_ram(18, 47)
            if VIRTUAL_RAM_19 > 0:
                KANGAROO_Y -= 1
                self.set_ram(16, KANGAROO_Y)
                VIRTUAL_RAM_19 = 0
                # if CLIMBING_VIRTUAL_RAM == 39:
                #     CLIMBING_VIRTUAL_RAM = 47
                #     self.set_ram(18, 47)
                # elif CLIMBING_VIRTUAL_RAM == 47:
                #     CLIMBING_VIRTUAL_RAM = 39
                #     self.set_ram(18, 39)
            VIRTUAL_RAM_19 += 1
        elif ram[16] > KANGAROO_Y and ram[114] not in [21, 15, 9]:  # climbing down
            if ram[18] & 16:
                self.set_ram(18, ram[18] & (not 16) | 32)
                if ram[16] not in [18, 12, 6]:
                    LADDER_X = ram[17]
            elif ram[16] < 19 and ram[16] & 1:
                self.set_ram(18, 39)
            elif ram[16] < 19:
                self.set_ram(18, 47)
            if VIRTUAL_RAM_19 > 65:
                self.set_ram(16, KANGAROO_Y + 1)
                KANGAROO_Y += 1
                VIRTUAL_RAM_19 = 0
            VIRTUAL_RAM_19 += 1
        elif ram[16] > KANGAROO_Y and ram[114] in [15, 9]:  # on platform
            LADDER_X = ram[17]
            self.set_ram(18, ram[18] & (not 16))
            VIRTUAL_RAM_19 = 0
            KANGAROO_Y = ram[16]
    else:
        LADDER_X = None
        VIRTUAL_RAM_19 = 0
        KANGAROO_Y = ram[16]
        # break


def remove_ladders(self):
    self._removed_ladders_poses = [(132, 36), (132, 132), (20, 84)]
    for i, obj in enumerate(self._objects):
        if isinstance(obj, Ladder):
            self._objects[i] = None


def moved_ladders(self):
    self._removed_ladders_poses = [(132, 36), (132, 132), (20, 84)]
    i = 0
    for obj in self._objects:
        if isinstance(obj, Ladder):
            obj.xy = ADDED_LADDERS_POSES[i]
            i += 1


def add_ladders_inpaintings(ladder_poses):
    bg = [[[80, 0, 132]] * 8] * 4
    rung = [[[162, 98, 33]] * 8] * 4
    h, w = 36, 8
    patch = np.array(rung + bg + rung + bg + rung + bg + rung + bg + rung).astype(
        np.uint8
    )
    # needs swapped positions
    return [(y, x, h, w, patch) for x, y in ladder_poses]


def bs(self):
    self.set_ram(96, 148)


# def skip_start(self):
#     self.set_ram(56, 255)


def _modif_funcs(env, modifs):
    if "change_level" in modifs:
        modifs.remove("change_level")
        modifs.insert(
            0, "change_level"
        )  # Change level should be the first modif to be applied
    env.step_modifs.append(_check_reseted)
    env._already_reset = False
    for mod in modifs:
        if mod == "disable_monkeys":
            env.step_modifs.append(disable_monkeys)
        elif mod == "disable_coconut":
            env.step_modifs.append(disable_coconut)
        elif mod == "disable_thrown_coconut":
            env.step_modifs.append(disable_thrown_coconut)
        elif mod == "unlimited_time":
            env.step_modifs.append(unlimited_time)
        elif mod == "random_init":
            env.step_modifs.append(random_init)
            env.reset_modifs.append(random_init)
        elif "set_floor" in mod:
            if mod[-1].isdigit():
                global FLOOR
                FLOOR = int(mod[-1])
            env.reset_modifs.append(set_kangaroo_position)
            env.step_modifs.append(set_kangaroo_position)
        # elif mod == "easy_mode":
        #     env.reset_modifs.append(easy_mode)
        elif "change_level" in mod:
            if mod[-1].isdigit():
                global LVL_NUM
                LVL_NUM = int(mod[-1])
                assert LVL_NUM < 3, "Invalid Level Number (0, 1 or 2)"
            env.step_modifs.append(change_level)
        elif mod == "no_ladder":
            assert (
                "change_level" not in modifs
            ), "Change level can't be used with no_ladder"
            env.inpaintings = remove_original_ladder_inpaintings()
            env.step_modifs.append(removed_ladder_step)
            env.place_above.extend(
                ((223, 183, 85), (227, 151, 89)))  # Player, Monkey
            env.post_detection_modifs.append(remove_ladders)
        elif mod == "invert_ladders":
            assert (
                "change_level" not in modifs
            ), "Change level can't be used with invert_ladders"
            global ADDED_LADDERS_POSES
            # ADDED_LADDERS_POSES = [(80, 36), (85, 132), (90, 84)]
            ADDED_LADDERS_POSES = [(80, 36), (80, 132), (100, 84)]
            env.inpaintings = (
                remove_original_ladder_inpaintings()
                + add_ladders_inpaintings(ADDED_LADDERS_POSES)
            )
            env.step_modifs.extend((removed_ladder_step, added_ladder_step))
            env.place_above.extend(
                ((223, 183, 85), (227, 151, 89)))  # Player, Monkey
            env.post_detection_modifs.append(moved_ladders)
        # elif mod == "skip_start":
        #     env.reset_modifs.append(skip_start)
        elif mod == "bs":
            env.step_modifs.append(bs)
