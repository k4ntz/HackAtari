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
        self.tick = 0
        self.level = 0

    def _set_active_modifications(self, active_modifs):
        """
        Specifies which modifications are active.

        :param active_modifs: A list of active modification names.
        """
        self.active_modifications = set(active_modifs)
    
    def set_level(self):
        if self.tick > 1:
            self.env.set_ram(22, self.level)
            self.tick = 0
            self.env.step_modifs.remove(self.set_level)
        else:
            self.tick += 1

    def level_0(self):
        """
        Changes the active level to 0.
        """
        self.level = 0
        self.env.step_modifs.append(self.set_level)

    def level_1(self):
        """
        Changes the active level to 1.
        """
        self.level = 1
        self.env.step_modifs.append(self.set_level)

    def level_2(self):
        """
        Changes the active level to 2.
        """
        self.level = 2
        self.env.step_modifs.append(self.set_level)
    
    def force_default_coyote(self):
        """
        The coyote cannot use the rocket rollerblades or the rocket shipt.
        """
        ram = self.env.get_ram()
        if ram[62]:
            self.env.set_ram(62, 0)

    def change_coyote(self):
        """
        If the coyote falls back too far, it activates the rocket rollerblades.
        """
        ram = self.env.get_ram()
        if ram[19] == 17 and not ram[62]:
            self.env.set_ram(62, 100)


    def _fill_modif_lists(self):
        """
        Returns the modification lists (step, reset, and post-detection) with active modifications.

        :return: Tuple of step_modifs, reset_modifs, and post_detection_modifs.
        """
        modif_mapping = {
            "step_modifs":{
                "default_coyote": self.force_default_coyote,
                "change_coyote": self.change_coyote,
            },
            "reset_modifs":{
                "level_0": self.level_0,
                "level_1": self.level_1,
                "level_2": self.level_2,
            }
        }

        step_modifs = [modif_mapping["step_modifs"][name]
                       for name in self.active_modifications if name in modif_mapping["step_modifs"]]
        reset_modifs = [modif_mapping["reset_modifs"][name]
                       for name in self.active_modifications if name in modif_mapping["reset_modifs"]]
        post_detection_modifs = []
        return step_modifs, reset_modifs, post_detection_modifs


def modif_funcs(env, active_modifs):
    modifications = GameModifications(env)
    modifications._set_active_modifications(active_modifs)
    return modifications._fill_modif_lists()
