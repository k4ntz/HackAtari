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

    def fog(self):
        """
        Constant fog weather
        """
        self.env.set_ram(94, 3)

    def snow(self):
        """
        Constant snow weather
        """
        self.env.set_ram(94, 2)

    def rain(self):
        """
        Constant rain weather
        """
        self.env.set_ram(94, 1)
    
    def tread_damage(self):
        """
        Tread sensor always damaged
        """
        ram = self.env.get_ram()
        self.env.set_ram(118, ram[118]|1)
    
    def canon_damage(self):
        """
        Canon sensor always damaged
        """
        ram = self.env.get_ram()
        self.env.set_ram(118, ram[118]|2)
    
    def no_radar(self):
        """
        Disables radar
        """
        ram = self.env.get_ram()
        self.env.set_ram(118, ram[118]|4)
    
    def vision_damage(self):
        """
        Vision sensor always damaged
        """
        ram = self.env.get_ram()
        self.env.set_ram(118, ram[118]|8)


    def _fill_modif_lists(self):
        """
        Returns the modification lists (step, reset, and post-detection) with active modifications.

        :return: Tuple of step_modifs, reset_modifs, and post_detection_modifs.
        """
        modif_mapping = {
            "fog": self.fog,
            "snow": self.snow,
            "rain": self.rain,
            "no_radar": self.no_radar,
            "tread_damage": self.tread_damage,
            "canon_damage": self.canon_damage,
            "vision_damage": self.vision_damage,
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
