import random


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

    def wind_effect(self):
        """
        Applies a wind effect: moves the ball up and right by 3 pixels per frame.
        """
        ram = self.env.get_ram()
        ball_x = ram[16]
        ball_y = 189 - ram[54]
        shadow_anker = ram[15]
        shadow_y = 189 - ram[55]

        new_ball_x = ball_x
        new_ball_y = ball_y
        new_shadow_y = shadow_y
        if random.randint(0, 1) < 0.5:
            new_ball_x += 1
            new_ball_y += 1
            new_shadow_y += 1

        if (
            (10 < ball_y < 140)
            and (10 < shadow_anker < 140)
            and (2 < ball_x < 155)
        ):
            self.env.set_ram(16, new_ball_x)
            self.env.set_ram(54, new_ball_y)
            self.env.set_ram(55, new_shadow_y)

    def always_upper_pitches(self):
        """
        Ensures the upper player always pitches.
        """
        ram = self.env.get_ram()
        if ram[15] == 7:
            self.env.set_ram(15, 142)
            self.env.set_ram(74, 0)

    def always_lower_pitches(self):
        """
        Ensures the lower player always pitches.
        """
        ram = self.env.get_ram()
        if ram[15] == 142:
            self.env.set_ram(15, 7)
            self.env.set_ram(74, 1)

    def always_upper_player(self):
        """
        Ensures the player is always on the upper field.
        """
        self.env.set_ram(80, 0)

    def always_lower_player(self):
        """
        Ensures the player is always on the lower field.
        """
        self.env.set_ram(80, 1)

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
            "wind_effect": self.wind_effect,
            "always_upper_pitches": self.always_upper_pitches,
            "always_lower_pitches": self.always_lower_pitches,
            "always_upper_player": self.always_upper_player,
            "always_lower_player": self.always_lower_player,
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
