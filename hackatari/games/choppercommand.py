class GameModifications:
    """
    Encapsulates game modifications for managing active modifications and applying them.
    """

    COLORS = [38, 40, 23, 86, 48]  # Black, White, Red, Blue, Green

    def __init__(self, env):
        """
        Initializes the modification handler with the given environment.

        :param env: The game environment to modify.
        """
        self.env = env
        self.active_modifications = set()

    def delay_shots(self):
        """
        Puts time delay between shots.
        """
        if not hasattr(self, "shot_count"):
            self.shot_count = 100

        if self.shot_count == 100 and (self.env._get_action() == 1 or self.env._get_action() >= 10):
            self.shot_count = 0
        elif 25 < self.shot_count < 100:
            for ram_n in [49, 52, 55, 58, 61, 64]:
                self.env.set_ram(ram_n, 0)
            self.env.set_ram(45, 0)
        if self.shot_count < 100:
            self.shot_count += 1

    def no_enemies(self):
        """
        Removes all enemies from the game.
        """
        for ram_n in range(6, 13):
            self.env.set_ram(ram_n, 0)

    def no_radar(self):
        """
        Removes the radar content.
        """
        self.env.set_ram(118, 37)

    def invisible_player(self):
        """
        Makes the player invisible.
        """
        self.env.set_ram(118, 38)

    def color_black(self):
        """
        Changes the background and enemies' color to black.
        """
        self.env.set_ram(117, self.COLORS[0])

    def color_white(self):
        """
        Changes the background and enemies' color to white.
        """
        self.env.set_ram(117, self.COLORS[1])

    def color_red(self):
        """
        Changes the background and enemies' color to red.
        """
        self.env.set_ram(117, self.COLORS[2])

    def color_blue(self):
        """
        Changes the background and enemies' color to blue.
        """
        self.env.set_ram(117, self.COLORS[3])

    def color_green(self):
        """
        Changes the background and enemies' color to green.
        """
        self.env.set_ram(117, self.COLORS[4])

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
            "delay_shots": self.delay_shots,
            "no_enemies": self.no_enemies,
            "no_radar": self.no_radar,
            "invisible_player": self.invisible_player,
            "color_black": self.color_black,
            "color_white": self.color_white,
            "color_red": self.color_red,
            "color_blue": self.color_blue,
            "color_green": self.color_green,
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
