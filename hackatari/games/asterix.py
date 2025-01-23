class GameModifications:
    """
    Encapsulates game modifications for managing active modifications and applying them.
    """

    def __init__(self, env):
        """
        Initializes the modification handler with the given environment.

        :param env: The game environment to modify.
        """
        self.env = env
        self.active_modifications = set()

    def obelix(self):
        """
        Sets RAM for the Obelix mode.
        """
        self.env.set_ram(54, 5)
        self.speed += 4

    def set_consumable_1(self):
        """
        Sets the consumale to pink (100points)
        """
        self.env.set_ram(54, 1)

    def set_consumable_2(self):
        """
        Sets the consumbale to shields (200points).
        """
        self.env.set_ram(54, 2)

    def unlimited_lives(self):
        """
        Grants unlimited lives.
        """
        self.env.set_ram(83, 3)

    def even_lines_free(self):
        """
        Frees even lines in the game.
        """
        for i in range(1, 9, 2):
            self.env.set_ram(73 + i, i + 1)
            self.env.set_ram(18 - i, 11)

    def odd_lines_free(self):
        """
        Frees odd lines in the game.
        """
        for i in range(0, 8, 2):
            self.env.set_ram(73 + i, i + 1)
            self.env.set_ram(18 - i, 11)

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
            "obelix": self.obelix,
            "set_consumable_1": self.set_consumable_1,
            "set_consumable_2": self.set_consumable_2,
            "unlimited_lives": self.unlimited_lives,
            "even_lines_free": self.even_lines_free,
            "odd_lines_free": self.odd_lines_free,
        }

        step_modifs = [modif_mapping[name]
                       for name in self.active_modifications if name in modif_mapping]
        reset_modifs = []
        post_detection_modifs = []
        return step_modifs, reset_modifs, post_detection_modifs


def modif_funcs(env, active_modifs):
    modifications = GameModifications(env)
    modifications._set_active_modifications(active_modifs)
    return modifications._fill_modif_lists()
