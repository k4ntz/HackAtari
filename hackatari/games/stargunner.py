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

    def static_bomber(self):
        """
        Stops the bomber at the top from moving
        """
        self.env.set_ram(31, 91)

    def static_flyers(self):
        """
        Stops the bomber at the top from moving
        """
        ram = self.env.get_ram()
        for i in range(74, 77):
            if ram[i]:
                self.env.set_ram(i, 91)
                self.env.set_ram(i-3, 91)
    
    def remove_mountains(self):
        for i in range(42, 69):
            self.env.set_ram(i, 0)
    
    def static_mountains(self):
        """
        Sets the mountains to static.
        """
        ram = self.env.get_ram()
        for i, el in enumerate([240, 255, 255, 255, 255, 255, 255, 
                                126, 60, 255, 249, 240, 224, 192, 
                                128, 0, 0, 0, 255, 255, 255, 254, 
                                252, 248, 240, 224, 192, 5]):
            self.env.set_ram(42+i, el)

    def _fill_modif_lists(self):
        """
        Returns the modification lists (step, reset, and post-detection) with active modifications.

        :return: Tuple of step_modifs, reset_modifs, and post_detection_modifs.
        """
        modif_mapping = {
            "step_modifs": {
                "static_bomber": self.static_bomber,
                "static_flyers": self.static_flyers,
                "remove_mountains": self.remove_mountains,
                "static_mountains": self.static_mountains,
            },
            "reset_modifs": {
            },
            "post_detection_modifs": {
            },
            "inpainting_modifs": {
            },
            "place_above_modifs": {
            }
        }

        step_modifs = [modif_mapping["step_modifs"][name]
                       for name in self.active_modifications if name in modif_mapping["step_modifs"]]
        reset_modifs = [modif_mapping["reset_modifs"][name]
                       for name in self.active_modifications if name in modif_mapping["reset_modifs"]]
        post_detection_modifs = [modif_mapping["post_detection_modifs"][name]
                       for name in self.active_modifications if name in modif_mapping["post_detection_modifs"]]
        inpainting_modifs = [modif_mapping["inpainting_modifs"][name]
                       for name in self.active_modifications if name in modif_mapping["inpainting_modifs"]]
        place_above_modifs = [modif_mapping["place_above_modifs"][name]
                       for name in self.active_modifications if name in modif_mapping["place_above_modifs"]]
        
        return step_modifs, reset_modifs, post_detection_modifs, inpainting_modifs, place_above_modifs


def modif_funcs(env, active_modifs):
    modifications = GameModifications(env)
    modifications._set_active_modifications(active_modifs)
    return modifications._fill_modif_lists()
