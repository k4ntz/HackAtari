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

    def no_damage(self):
        """
        Always sets the player health to max, making them invincible.
        """
        self.env.set_ram(75, 39)

    def infinite_time(self):
        """
        Provides unlimited time to clear the level.
        """
        self.env.set_ram(27, 32)
        self.env.set_ram(28, 1)

    def infinite_lives(self):
        """
        Always sets the player lives to max, making them infinite.
        """
        self.env.set_ram(29, 3)

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
            "no_damage": self.no_damage,
            "infinite_time": self.infinite_time,
            "infinite_lives": self.infinite_lives,
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
