import numpy as np

sprite_maps = {"Player": np.array([ [0, 1, 0, 0, 0, 0, 0],
                                [1, 1, 1, 0, 0, 0, 0],
                                [1, 1, 1, 1, 1, 0, 0],
                                [1, 1, 1, 1, 1, 1, 1],
                                [0, 1, 1, 1, 0, 0, 0]])[..., np.newaxis],
            "Bomber":np.array([ [1, 1, 1, 1, 1],
                                [1, 1, 0, 1, 1],
                                [1, 1, 0, 1, 1],
                                [1, 1, 1, 1, 1]])[..., np.newaxis],
            "Baiter":np.array([ [0, 1, 1, 1, 1, 1, 1, 0],
                                [1, 1, 1, 0, 0, 1, 1, 1],
                                [0, 1, 1, 1, 1, 1, 1, 0]])[..., np.newaxis],
            "Pod": np.array([   [0, 0, 0, 1, 0, 0, 0],
                                [0, 1, 0, 1, 0, 1, 0],
                                [0, 0, 1, 1, 1, 0, 0],
                                [1, 1, 1, 1, 1, 1, 1],
                                [0, 0, 1, 1, 1, 0, 0],
                                [0, 1, 0, 1, 0, 1, 0],
                                [0, 0, 0, 1, 0, 0, 0]])[..., np.newaxis],
            "Swarm":np.array([  [0, 1, 0, 0, 0, 0, 0, 0],
                                [1, 1, 1, 0, 0, 1, 0, 0],
                                [0, 1, 0, 0, 1, 1, 1, 0],
                                [0, 0, 0, 0, 0, 1, 0, 0],
                                [0, 1, 0, 0, 0, 0, 1, 0],
                                [1, 1, 1, 0, 0, 1, 1, 1],
                                [0, 1, 0, 0, 0, 0, 1, 0]])[..., np.newaxis],
            "Lander":np.array([ [0, 0, 0, 1, 1, 0, 0, 0],
                                [0, 0, 1, 1, 1, 1, 0, 0],
                                [0, 0, 1, 1, 1, 1, 0, 0],
                                [0, 0, 0, 1, 1, 0, 0, 0],
                                [0, 0, 1, 0, 0, 1, 0, 0],
                                [0, 1, 1, 1, 1, 1, 1, 0],
                                [1, 1, 1, 1, 1, 1, 1, 1]])[..., np.newaxis],
            "Humanoide_Lander": np.array([  [0, 1, 0, 0, 0, 1, 0, 0],
                                            [0, 0, 1, 1, 1, 1, 0, 0],
                                            [0, 0, 1, 1, 1, 1, 0, 0],
                                            [0, 0, 0, 1, 1, 0, 0, 0],
                                            [0, 0, 1, 0, 0, 1, 0, 0],
                                            [0, 0, 1, 1, 1, 1, 0, 0],
                                            [1, 1, 0, 0, 0, 0, 1, 1]])[..., np.newaxis]
}

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
        self.prev_15 = 0
        self.prev_55 = 0
        self.prev_78 = 0
        self.prev_102 = 0
        self.tick = 1

    def _set_active_modifications(self, active_modifs):
        """
        Specifies which modifications are active.

        :param active_modifs: A list of active modification names.
        """
        self.active_modifications = set(active_modifs)

    def more_bombs(self):
        """
        Increases the amount of smart bombs to 8
        """
        self.env.set_ram(68, 8)

    def quick_start(self):
        """
        Reduces the game start time to 5 frames
        """
        self.env.set_ram(75, 5)

    # necessary since inpainting modif is called every render and is therefore inconsistent if started from a save state
    def no_flickering_step(self):
        """
        Sets the environment variables for the no_flickering modification
        """
        # remove this self.tick if modif functions are only applied once in the step() function of hackatari.core
        if self.tick&1:
            ram = self.env.get_ram()
            self.prev_15 = ram[15]
            self.prev_55 = ram[55]
            self.prev_78 = ram[78]
            self.prev_102 = ram[102]
        self.tick^=1

    def no_flickering_reset(self):
        """
        Reset the tick counter used by the step modif
        """
        self.tick = 1

    def no_flickering(self):
        """
        Uses ALE inpainting to add the missing sprites in the frame.
        """
        ret = []
        background_color = np.array((0, 0, 0))
        ram = self.env.get_ram()
        
        # Player
        if (self.prev_15 == 55 or self.prev_102) and self.env.objects[0].xy != (0, 0):
            object_color = np.array(self.env.objects[0].rgb)
            x, y, w, h = self.env.objects[0].xywh
            if ram[11]&4:
                patch = np.where(sprite_maps["Player"], np.ones((h, w, 3)) * object_color, np.ones((h, w, 3)) * background_color).astype(np.uint8)
            else:
                # inverted sprite
                patch = np.where(sprite_maps["Player"][...,::-1,:], np.ones((h, w, 3)) * object_color, np.ones((h, w, 3)) * background_color).astype(np.uint8)
            ret.append((y, x, h, w, patch))

        # Enemy shot
        if self.env.objects[2].xy != (0, 0):
            object_color = np.array(self.env.objects[2].rgb)
            x, y, w, h = self.env.objects[2].xywh
            patch = (np.ones((h, w, 3)) * object_color).astype(np.uint8)
            ret.append((y, x, h, w, patch))

        # Enemies
        if ram[20]:
            for o in self.env.objects[3:21]:
                if o.xy != (0, 0) and o.x >= 0 and o.y >= 0:
                    object_color = np.array(o.rgb)
                    x, y, w, h = o.xywh
                    patch = np.where(sprite_maps[o.__class__.__name__], np.ones((h, w, 3)) * object_color, np.ones((h, w, 3)) * background_color).astype(np.uint8)
                    # needs swapped positions
                    ret.append((y, x, h, w, patch))

        # Humans
        for i, o in enumerate(self.env.objects[21:26]):
            # skip Human object if it is already visible in the frame
            if i != self.prev_78 and o.xy != (0, 0) and o.x >= 0 and o.y >= 0:
                object_color = np.array(o.rgb)
                x, y, w, h = o.xywh
                patch = (np.ones((h, w, 3)) * object_color).astype(np.uint8)
                # needs swapped positions
                ret.append((y, x, h, w, patch))

        # Radar
        for o in self.env.objects[26:40]:
            if o.xy != (0, 0) and o.x >= 0 and o.y >= 0:
                object_color = np.array(o.rgb)
                x, y, w, h = o.xywh
                patch = (np.ones((h, w, 3)) * object_color).astype(np.uint8)
                # needs swapped positions
                ret.append((y, x, h, w, patch))

        return ret


    def _fill_modif_lists(self):
        """
        Returns the modification lists (step, reset, and post-detection) with active modifications.

        :return: Tuple of step_modifs, reset_modifs, and post_detection_modifs.
        """
        modif_mapping = {
            "step_modifs": {
                "more_bombs": self.more_bombs,
                "no_flickering": self.no_flickering_step,
            },
            "reset_modifs": {
                "no_flickering": self.no_flickering_reset,
                "quick_start": self.quick_start,
            },
            "post_detection_modifs": {
            },
            "inpainting_modifs": {
                "no_flickering": self.no_flickering,
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
