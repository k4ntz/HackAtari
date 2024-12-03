LVL_NUM = 0

init_ram = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    255,
    0,
    49,
    8,
    127,
    255,
    141,
    255,
    3,
    106,
    154,
    45,
    0,
    0,
    0,
    0,
    0,
    0,
    2,
    0,
    107,
    26,
    126,
    28,
    0,
    6,
    2,
    2,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    63,
    27,
    27,
    63,
    123,
    117,
    118,
    123,
    63,
    31,
    62,
    15,
    219,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    16,
    253,
    113,
    255,
    227,
    254,
    2,
    254,
    93,
    252,
    91,
    249,
    42,
    12,
    68,
    68,
    0,
    0,
    0,
    0,
    255,
    169,
    247,
    216,
    247,
    93,
    93,
    93,
    93,
    93,
    93,
    48,
    76,
    34,
    34,
    34,
    34,
    13,
    243,
]


def _randomize_pos(self):
    pot_start_pos = [
        (49, 154),
        (110, 154),
        (49, 127),
        (111, 132),
        (111, 99),
        (50, 71),
        (53, 48),
        (111, 43),
        (111, 21),
    ]

    # rndinit = random.randint(0, len(pot_start_pos)-1)
    rndinit = 7
    for i, el in enumerate(init_ram):
        if i not in [35, 36]:  # lives & scores
            self.set_ram(i, el)
    startp = pot_start_pos[rndinit]
    for rp, sp in zip([19, 27], startp):
        self.set_ram(rp, sp)
    self.lasty = startp[1]


def no_barrel(self):
    # if self.get_ram()[16] == 0:
    self.set_ram(25, 255)


def unlimited_time(self):
    # if self.get_ram()[16] == 0:
    self.set_ram(36, 70)


def change_level(self):
    """
    Changes the level according to the argument number 0-2. If not specified, selcts random level.
    """
    if self.get_ram()[16] == 1:
        for i, el in enumerate(init_ram):
            if i not in [35, 36]:  # lives & scores
                self.set_ram(i, el)
        if self.random_start:
            _randomize_pos(self)


def random_start_step(self):
    ram = self.get_ram()
    if self.nb_lives != ram[35]:
        _randomize_pos(self)
        self.nb_lives = ram[35]


def _modif_funcs(env, modifs):
    env.nb_lives = 2
    for mod in modifs:
        if mod == "no_barrel":
            env.step_modifs.append(no_barrel)
        if mod == "unlimited_time":
            env.step_modifs.append(unlimited_time)
        elif "change_level" in mod:
            env.step_modifs.append(change_level)
        elif mod == "random_start":
            env.reset_modifs.append(_randomize_pos)
            env.step_modifs.append(random_start_step)
            env.random_start = True
        else:
            print("Invalid modification")
