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

    def player_color_white(self):
        """
        Changes the player color to white.
        """
        self.env.set_ram(94, 0)

    def player_color_green(self):
        """
        Changes the player color to green.
        """
        self.env.set_ram(94, 1)

    def player_color_red(self):
        """
        Changes the player color to red.
        """
        self.env.set_ram(94, 2)

    def player_color_yellow(self):
        """
        Changes the player color to yellow.
        """
        self.env.set_ram(94, 3)

    def player_color_purple(self):
        """
        Changes the player color to purple.
        """
        self.env.set_ram(94, 4)

    def player_color_blue(self):
        """
        Changes the player color to blue.
        """
        self.env.set_ram(94, 5)

    def enemy_color_white(self):
        """
        Changes the enemy color to white.
        """
        self.env.set_ram(95, 0)

    def enemy_color_green(self):
        """
        Changes the enemy color to green.
        """
        self.env.set_ram(95, 1)

    def enemy_color_red(self):
        """
        Changes the enemy color to red.
        """
        self.env.set_ram(95, 2)

    def enemy_color_yellow(self):
        """
        Changes the enemy color to yellow.
        """
        self.env.set_ram(95, 3)

    def enemy_color_purple(self):
        """
        Changes the enemy color to purple.
        """
        self.env.set_ram(95, 4)

    def enemy_color_blue(self):
        """
        Changes the enemy color to blue.
        """
        self.env.set_ram(95, 5)

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
            "player_color_white": self.player_color_white,
            "player_color_green": self.player_color_green,
            "player_color_red": self.player_color_red,
            "player_color_yellow": self.player_color_yellow,
            "player_color_purple": self.player_color_purple,
            "player_color_blue": self.player_color_blue,
            "enemy_color_white": self.enemy_color_white,
            "enemy_color_green": self.enemy_color_green,
            "enemy_color_red": self.enemy_color_red,
            "enemy_color_yellow": self.enemy_color_yellow,
            "enemy_color_purple": self.enemy_color_purple,
            "enemy_color_blue": self.enemy_color_blue,
        }

        step_modifs = []
        reset_modifs = []
        post_detection_modifs = []

        for mod in self.active_modifications:
            if mod in modif_mapping:
                reset_modifs.append(modif_mapping[mod])

        return step_modifs, reset_modifs, post_detection_modifs


def modif_funcs(env, active_modifs):
    modifications = GameModifications(env)
    modifications._set_active_modifications(active_modifs)
    return modifications._fill_modif_lists()
