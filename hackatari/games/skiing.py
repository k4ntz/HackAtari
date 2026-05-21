import numpy as np


class GameModifications:
    """
    Encapsulates game modifications for managing active modifications and applying them.
    """

    def __init__(self, env):
        """
        Initializes the modification handler with the given environment.
        """
        self.env = env
        self.active_modifications = set()

    def modify_ram_invert_flag(self):
        """
        Invert Flag
        """
        ram = self.env.get_ram()
        types = ram[70:78]
        for i in range(8):
            if types[i] == 2:
                self.env.set_ram(78 + i, 4)

    def moving_flags(self):
        """
        Moves the flags.
        """
        ram = self.env.get_ram()
        speed = (ram[0] < 128)*2 - 1
        if ram[0] % 4 == 0 and ram[17] != 255: # every 4 frames and not in game done state
            for i in range(8):
                if ram[70 + i] == 2:
                    current_x = ram[62 + i]
                    self.env.set_ram(62 + i, current_x + speed)

    
    def moguls_to_trees(self):
        """
        Changes moguls to trees.
        """
        ram = self.env.get_ram()
        for i in range(8):
            if ram[70+i] == 5:
                self.env.set_ram(30+i, 60)
                self.env.set_ram(38+i, 133)
                self.env.set_ram(46+i, 126)
                self.env.set_ram(70+i, 85)
                self.env.set_ram(78+i, 6)

    def _set_active_modifications(self, active_modifs):
        """
        Specifies which modifications are active.
        """
        self.active_modifications = set(active_modifs)

    def _fill_modif_lists(self):
        """
        Returns the modification lists (step, reset, and post-detection) with active modifications.
        """
        modif_mapping = {
            "step_modifs": {
                "invert_flags": self.modify_ram_invert_flag,
                "moguls_to_trees": self.moguls_to_trees,
                "moving_flags": self.moving_flags,
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
