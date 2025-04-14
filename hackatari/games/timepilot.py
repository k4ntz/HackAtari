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

    def _set_active_modifications(self, active_modifs):
        """
        Specifies which modifications are active.

        :param active_modifs: A list of active modification names.
        """
        self.active_modifications = set(active_modifs)

    def level_2(self):
        """
        Start at level 2
        """
        self.env.set_ram(21, 1)

    def level_3(self):
        """
        Start at level 3
        """
        self.env.set_ram(21, 2)

    def level_4(self):
        """
        Start at level 4
        """
        self.env.set_ram(21, 3)

    def level_5(self):
        """
        Start at level 5
        """
        self.env.set_ram(21, 4)


    def _fill_modif_lists(self):
        """
        Returns the modification lists (step, reset, and post-detection) with active modifications.

        :return: Tuple of step_modifs, reset_modifs, and post_detection_modifs.
        """
        modif_mapping = {
            "level_1": self.level_2,
            "level_1": self.level_3,
            "level_1": self.level_4,
            "level_1": self.level_5,
        }

        step_modifs = []
        reset_modifs = [modif_mapping[name]
                       for name in self.active_modifications if name in modif_mapping]
        post_detection_modifs = []
        return step_modifs, reset_modifs, post_detection_modifs


def modif_funcs(env, active_modifs):
    modifications = GameModifications(env)
    modifications._set_active_modifications(active_modifs)
    return modifications._fill_modif_lists()
