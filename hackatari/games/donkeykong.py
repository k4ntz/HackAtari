class GameModifications:
    """
    Encapsulates game modifications for managing active modifications and applying them.
    """

    INIT_RAM = [
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 255, 0, 49, 8, 127, 255, 141, 255, 3, 106, 154,
        45, 0, 0, 0, 0, 0, 0, 2, 0, 107, 26, 126, 28, 0, 6,
        2, 2, 0, 0, 0, 0, 0, 0, 0, 63, 27, 27, 63, 123, 
        117, 118, 123, 63, 31, 62, 15, 219, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 16, 253, 113, 255, 227, 254, 2, 254, 93, 252,
        91, 249, 42, 12, 68, 68, 0, 0, 0, 0, 255, 169, 247,
        216, 247, 93, 93, 93, 93, 93, 93, 48, 76, 34, 34,
        34, 34, 13, 243,
    ]

    def __init__(self, env):
        """
        Initializes the modification handler with the given environment.

        :param env: The game environment to modify.
        """
        self.env = env
        self.active_modifications = set()
        self.nb_lives = 2
        self.random_start = False
        self.lasty = None

    def no_barrel(self):
        """
        Removes barrels from the game.
        """
        self.env.set_ram(25, 255)

    def unlimited_time(self):
        """
        Provides unlimited time for the player.
        """
        self.env.set_ram(36, 70)

    def change_level_0(self):
        """
        Changes the level to level 0.
        """
        self._change_level(0)

    def change_level_1(self):
        """
        Changes the level to level 1.
        """
        self._change_level(1)

    def change_level_2(self):
        """
        Changes the level to level 2.
        """
        self._change_level(2)

    def _change_level(self, level):
        """
        Internal method to change the level based on the specified level.

        :param level: Level number to change to.
        """
        if self.env.get_ram()[16] == 1:
            for i, el in enumerate(self.INIT_RAM):
                if i not in [35, 36]:  # lives & scores
                    self.env.set_ram(i, el)
            if self.random_start:
                self._randomize_pos()

    def random_start_step(self):
        """
        Handles the random starting position for each step.
        """
        ram = self.env.get_ram()
        if self.nb_lives != ram[35]:
            self._randomize_pos()
            self.nb_lives = ram[35]

    def _randomize_pos(self):
        """
        Randomizes the starting position of the player.
        """
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

        rndinit = 7
        for i, el in enumerate(self.INIT_RAM):
            if i not in [35, 36]:  # lives & scores
                self.env.set_ram(i, el)
        startp = pot_start_pos[rndinit]
        for rp, sp in zip([19, 27], startp):
            self.env.set_ram(rp, sp)
        self.lasty = startp[1]

    def _set_active_modifications(self, active_modifs):
        """
        Specifies which modifications are active.

        :param active_modifs: A list of active modification names.
        """
        self.active_modifications = set(active_modifs)

    def _fill_modif_lists(self):
        """
        Returns the modification lists (step, reset, and post-detection) with active modifications.

        :return: Tuple of step_modifs, reset_modifs, and post_detection_modifs.
        """
        modif_mapping = {
            "no_barrel": self.no_barrel,
            "unlimited_time": self.unlimited_time,
            # "change_level_0": self.change_level_0,
            # "change_level_1": self.change_level_1,
            # "change_level_2": self.change_level_2,
            "random_start": self.random_start_step,
        }

        step_modifs = []
        reset_modifs = []

        for mod in self.active_modifications:
            if mod in modif_mapping:
                if mod == "random_start":
                    reset_modifs.append(self._randomize_pos)
                    self.random_start = True
                step_modifs.append(modif_mapping[mod])

        return step_modifs, reset_modifs, []


def modif_funcs(env, active_modifs):
    modifications = GameModifications(env)
    modifications._set_active_modifications(active_modifs)
    return modifications._fill_modif_lists()
