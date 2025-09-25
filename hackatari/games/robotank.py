import numpy as np

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
    
    def no_radar_inpainting(self):
        background_color = np.array((80, 0, 132))
        x, y, w, h = 57, 139, 43, 32
        patch = (np.ones((h, w, 3)) * background_color).astype(np.uint8)
        # needs swapped positions
        return [(y, x, h, w, patch)]
    
    def radar_enemy_pos_inpainting(self):
        background_color = np.array((146, 70, 192))
        radar = self.env.objects[4]
        if radar.xy != (0, 0):
            x, y, w, h = radar.xywh
            patch = (np.ones((h, w, 3)) * background_color).astype(np.uint8)
            # needs swapped positions
            return [(y, x, h, w, patch)]
        return []


    def _fill_modif_lists(self):
        """
        Returns the modification lists (step, reset, and post-detection) with active modifications.

        :return: Tuple of step_modifs, reset_modifs, and post_detection_modifs.
        """
        modif_mapping = {
            "step_modifs": {
                "fog": self.fog,
                "snow": self.snow,
                "rain": self.rain,
                "no_radar": self.no_radar,
                "tread_damage": self.tread_damage,
                "canon_damage": self.canon_damage,
                "vision_damage": self.vision_damage,
            },
            "reset_modifs": {
            },
            "post_detection_modifs": {
            },
            "inpainting_modifs": {
                "no_radar_inpainting": self.no_radar_inpainting,
                "radar_enemy_pos_inpainting": self.radar_enemy_pos_inpainting,
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
