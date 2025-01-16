# from random import random
import numpy as np

dark_grey_line = [100] * 38
brick_line1 = [
    180,
    180,
    180,
    180,
    180,
    100,
    180,
    180,
    180,
    180,
    180,
    180,
    100,
    180,
    180,
    180,
    180,
    180,
    180,
    100,
    180,
    180,
    180,
    180,
    180,
    180,
    100,
    180,
    180,
    180,
    180,
    180,
    180,
    100,
    180,
    180,
    180,
    180,
]
brick_line2 = [
    100,
    180,
    180,
    180,
    180,
    180,
    180,
    100,
    180,
    180,
    180,
    180,
    180,
    180,
    100,
    180,
    180,
    180,
    180,
    180,
    180,
    100,
    180,
    180,
    180,
    180,
    180,
    180,
    100,
    180,
    180,
    180,
    180,
    180,
    180,
    100,
    180,
    180,
]
brick_line3 = [
    180,
    180,
    100,
    180,
    180,
    180,
    180,
    180,
    180,
    100,
    180,
    180,
    180,
    180,
    180,
    180,
    100,
    180,
    180,
    180,
    180,
    180,
    180,
    100,
    180,
    180,
    180,
    180,
    180,
    180,
    100,
    180,
    180,
    180,
    180,
    180,
    180,
    100,
]
wall = np.array(
    [
        dark_grey_line,
        brick_line1,
        brick_line1,
        brick_line1,
        dark_grey_line,
        brick_line2,
        brick_line2,
        brick_line2,
        dark_grey_line,
        brick_line3,
        brick_line3,
        brick_line3,
        dark_grey_line,
        dark_grey_line,
    ],
    dtype=np.uint8,
)


def modify_ram_invert_flag(self):
    """
    Invert Flag
    """
    ram = self.get_ram()
    types = ram[70:78]
    cols = ram[78:86]
    for i in range(8):
        if types[i] == 2:
            self.set_ram(78 + i, 4)


def wall_inpaintings():
    background_color = np.array((80, 0, 132))
    wall_rgb = np.stack((wall,) * 3, axis=-1)
    w, h = wall.shape[1], wall.shape[0]
    ladder_poses = [(0, 0)]
    # needs swapped positions
    return [(y, x, h, w, wall_rgb) for x, y in ladder_poses]


def wall_updates(self):
    ram = self.get_ram()
    wall = self.env.env.ale._inpaintings[0][-1]
    w, h = wall.shape[1], wall.shape[0]
    flags = []
    for i in range(8):
        if ram[70 + i] == 2:  # Flag
            x, y = (ram[62 + i], 182 - ram[86 + i])
            height = 75 - ram[90 + i]
            if not (y > 177 or y < 27 or (y in [27, 28] and height < 16)):
                flags.append((x, y))
    self.env.env.ale._env.inpaintings = [(y, x, h, w, wall) for x, y in flags]


def wall_updates_reset(self):
    self.env.env.ale.place_above = []


def _modif_funcs(env, modifs):
    for mod in modifs:
        if mod == "invert_flags":
            env.step_modifs.append(modify_ram_invert_flag)
        elif mod == "walls":
            env.inpaintings = wall_inpaintings()
            env.step_modifs.append(wall_updates)
            env.place_above.append((214, 92, 92))
        else:
            print("Invalid or unknown modification")
