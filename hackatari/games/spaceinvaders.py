import numpy as np
from ocatari.ram.game_objects import NoObject


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

    def disable_shield_left(self):
        """
        Disables the left shield.
        """
        for i in range(43, 52):
            self.env.set_ram(i, 0)

    def disable_shield_middle(self):
        """
        Disables the middle shield.
        """
        for i in range(52, 61):
            self.env.set_ram(i, 0)

    def disable_shield_right(self):
        """
        Disables the right shield.
        """
        for i in range(61, 71):
            self.env.set_ram(i, 0)

    def relocate_shields_slight_left(self):
        """
        Relocates the shields to a low position.
        """
        self.env.set_ram(27, 35)

    def shift_shields_one(self):
        """
        Shifts the shields to the right by one pixel.
        """
        self.env.set_ram(27, 44)

    def shift_shields_three(self):
        """
        Shifts the shields to the right by three pixels.
        """
        self.env.set_ram(27, 46)

    def relocate_shields_right(self):
        """
        Relocates the shields to a high position.
        """
        self.env.set_ram(27, 53)

    def controlable_missile(self):
        """
        Allows the missile to be controlled by setting its position to the player's position.
        """
        self.env.set_ram(87, self.env.get_ram()[28])

    def no_danger(self):
        self.disable_shield_left()
        self.disable_shield_middle()
        self.disable_shield_right()
        # self.env.set_ram(16, 0) # not going down
        for i in range(80, 83):
            self.env.set_ram(i, 0)
        for i in range(83, 85):
            self.env.set_ram(i, 255)

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
            "disable_shield_left": self.disable_shield_left,
            "disable_shield_middle": self.disable_shield_middle,
            "disable_shield_right": self.disable_shield_right,
            "relocate_shields_slight_left": self.relocate_shields_slight_left,
            "relocate_shields_off_by_one": self.shift_shields_one,
            "relocate_shields_right": self.relocate_shields_right,
            # "curved_shots_weak": self.curved_shots_weak,
            # "curved_shots_medium": self.curved_shots_medium,
            # "curved_shots_strong": self.curved_shots_strong,
            "controlable_missile": self.controlable_missile,
            "no_danger": self.no_danger,
            "relocate_shields_off_by_three": self.shift_shields_three,
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
