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

    def team_colors_white(self):
        """
        Changes the player and enemy colors to black.
        """
        self.env.set_ram(94, 0)  # Player color
        self.env.set_ram(95, 0)  # Enemy color

    def team_colors_green(self):
        """
        Changes the player and enemy colors to white.
        """
        self.env.set_ram(94, 1)  # Player color
        self.env.set_ram(95, 1)  # Enemy color

    def team_colors_red(self):
        """
        Changes the player and enemy colors to red.
        """
        self.env.set_ram(94, 2)  # Player color
        self.env.set_ram(95, 2)  # Enemy color

    def team_colors_yellow(self):
        """
        Changes the player and enemy colors to blue.
        """
        self.env.set_ram(94, 3)  # Player color
        self.env.set_ram(95, 3)  # Enemy color

    def team_colors_purple(self):
        """
        Changes the player and enemy colors to green.
        """
        self.env.set_ram(94, 4)  # Player color
        self.env.set_ram(95, 4)  # Enemy color

    def team_colors_blue(self):
        """
        Changes the player and enemy colors to yellow.
        """
        self.env.set_ram(94, 5)  # Player color
        self.env.set_ram(95, 5)  # Enemy color

    def set_active_modifications(self, active_modifs):
        """
        Specifies which modifications are active.

        :param active_modifs: A list of active modification names.
        """
        self.active_modifications = set(active_modifs)

    def fill_modif_lists(self):
        """
        Returns the modification lists (step, reset, and post-detection) with active modifications.

        :return: Tuple of step_modifs, reset_modifs, and post_detection_modifs.
        """
        modif_mapping = {
            "team_colors_purple": self.team_colors_purple,
            "team_colors_white": self.team_colors_white,
            "team_colors_red": self.team_colors_red,
            "team_colors_blue": self.team_colors_blue,
            "team_colors_green": self.team_colors_green,
            "team_colors_yellow": self.team_colors_yellow,
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
    modifications.set_active_modifications(active_modifs)
    return modifications.fill_modif_lists()
