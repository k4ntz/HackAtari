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

    # def wall_inpaintings(self):
    #     """
    #     Generates inpainting data for walls.
    #     """
    #     background_color = np.array((80, 0, 132))
    #     wall_rgb = np.stack((wall,) * 3, axis=-1)
    #     w, h = wall.shape[1], wall.shape[0]
    #     ladder_poses = [(0, 0)]
    #     return [(y, x, h, w, wall_rgb) for x, y in ladder_poses]

    # def wall_updates(self):
    #     """
    #     Updates the wall rendering based on flag positions.
    #     """
    #     ram = self.env.get_ram()
    #     wall = self.env.env.ale._inpaintings[0][-1]
    #     w, h = wall.shape[1], wall.shape[0]
    #     flags = []
    #     for i in range(8):
    #         if ram[70 + i] == 2:  # Flag
    #             x, y = (ram[62 + i], 182 - ram[86 + i])
    #             height = 75 - ram[90 + i]
    #             if not (y > 177 or y < 27 or (y in [27, 28] and height < 16)):
    #                 flags.append((x, y))
    #     self.env.env.ale._env.inpaintings = [
    #         (y, x, h, w, wall) for x, y in flags]

    # def wall_updates_reset(self):
    #     """
    #     Resets the wall inpainting modifications.
    #     """
    #     self.env.env.ale.place_above = []

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
            "invert_flags": self.modify_ram_invert_flag,
            #    "walls": self.wall_updates,
        }

        step_modifs = [modif_mapping[name]
                       for name in self.active_modifications if name in modif_mapping]
        reset_modifs = [
            self.wall_updates_reset] if "walls" in self.active_modifications else []
        post_detection_modifs = []

        return step_modifs, reset_modifs, post_detection_modifs


def modif_funcs(env, active_modifs):
    modifications = GameModifications(env)
    modifications._set_active_modifications(active_modifs)
    return modifications._fill_modif_lists()
