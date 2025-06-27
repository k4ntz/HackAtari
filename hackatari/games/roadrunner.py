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

    def level_0(self):
        """
        Constant fog weather
        """
        self.env.set_ram(22, 0)

    def level_1(self):
        """
        Constant fog weather
        """
        self.env.set_ram(22, 1)

    def level_2(self):
        """
        Constant fog weather
        """
        self.env.set_ram(22, 2)


    def _fill_modif_lists(self):
        """
        Returns the modification lists (step, reset, and post-detection) with active modifications.

        :return: Tuple of step_modifs, reset_modifs, and post_detection_modifs.
        """
        modif_mapping = {
        }

        step_modifs = [modif_mapping[name]
                       for name in self.active_modifications if name in modif_mapping]
        r_mods = {"level_0":self.level_0, "level_1":self.level_1, "level_2":self.level_2}
        reset_modifs = [r_mods[name] for name in self.active_modifications if name in ["level_0", "level_1", "level_2"]]
        post_detection_modifs = []
        return step_modifs, reset_modifs, post_detection_modifs


def modif_funcs(env, active_modifs):
    modifications = GameModifications(env)
    modifications._set_active_modifications(active_modifs)
    return modifications._fill_modif_lists()
