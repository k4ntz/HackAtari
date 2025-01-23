class GameModifications:
    """
    Encapsulates game modifications for managing active modifications and applying them.
    """

    COLORS = [0, 48, 113, 200]  # Black, Red, Blue, Green

    def __init__(self, env):
        """
        Initializes the modification handler with the given environment.

        :param env: The game environment to modify.
        """
        self.env = env
        self.active_modifications = set()

    def recolor_ice_black(self):
        """
        Adjusts the ice floes to black.
        """
        self.env.set_ram(43, self.COLORS[0])
        self.env.set_ram(44, self.COLORS[0])
        self.env.set_ram(45, self.COLORS[0])
        self.env.set_ram(46, self.COLORS[0])

    def recolor_ice_red(self):
        """
        Adjusts the ice floes to red.
        """
        self.env.set_ram(43, self.COLORS[1])
        self.env.set_ram(44, self.COLORS[1])
        self.env.set_ram(45, self.COLORS[1])
        self.env.set_ram(46, self.COLORS[1])

    def recolor_ice_blue(self):
        """
        Adjusts the ice floes to blue.
        """
        self.env.set_ram(43, self.COLORS[2])
        self.env.set_ram(44, self.COLORS[2])
        self.env.set_ram(45, self.COLORS[2])
        self.env.set_ram(46, self.COLORS[2])

    def recolor_ice_green(self):
        """
        Adjusts the ice floes to green.
        """
        self.env.set_ram(43, self.COLORS[3])
        self.env.set_ram(44, self.COLORS[3])
        self.env.set_ram(45, self.COLORS[3])
        self.env.set_ram(46, self.COLORS[3])

    def ui_color_black(self):
        """
        Adjusts the UI to black.
        """
        self.env.set_ram(71, self.COLORS[3])

    def ui_color_red(self):
        """
        Adjusts the UI to red.
        """
        self.env.set_ram(71, self.COLORS[1])

    def reposition_floes_easy(self):
        """
        Adjusts the position of the ice floes to an easy layout.
        """
        self.env.set_ram(22, 0)
        for i in range(31, 35):
            self.env.set_ram(i, 80)

    def reposition_floes_medium(self):
        """
        Adjusts the position of the ice floes to a medium layout.
        """
        self.env.set_ram(22, 0)
        for i in range(31, 35):
            self.env.set_ram(i, 80+30*(i-30))

    def reposition_floes_hard(self):
        """
        Adjusts the position of the ice floes to a hard layout.
        """
        self.env.set_ram(22, 0)
        for i in range(31, 35):
            self.env.set_ram(i, 80+20*(i-30))

    def no_birds(self):
        """
        Removes all enemies.
        """
        for i in range(92, 96):
            self.env.set_ram(i, 0)

    def few_enemies(self):
        """
        Sets a few enemies (e.g., easy mode).
        """
        for i in range(92, 96):
            self.env.set_ram(i, 5)

    def many_enemies(self):
        """
        Sets many enemies (e.g., hard mode).
        """
        for i in range(92, 96):
            self.env.set_ram(i, 15)

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
            # are game breaking
            # "recolor_ice_black": self.recolor_ice_black,
            # "recolor_ice_red": self.recolor_ice_red,
            # "recolor_ice_blue": self.recolor_ice_blue,
            # "recolor_ice_green": self.recolor_ice_green,
            "ui_color_red": self.ui_color_red,
            "ui_color_black": self.ui_color_black,
            "reposition_floes_easy": self.reposition_floes_easy,
            "reposition_floes_medium": self.reposition_floes_medium,
            "reposition_floes_hard": self.reposition_floes_hard,
            "no_birds": self.no_birds,
            "few_enemies": self.few_enemies,
            "many_enemies": self.many_enemies,
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
