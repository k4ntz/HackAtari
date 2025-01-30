import random


class GameModifications:
    """
    Encapsulates game modifications for managing active modifications and applying them.
    """

    def __init__(self, env):
        """
        Initializes the modification handler with the given environment.
        """
        self.wind_direction_x = 1
        self.wind_direction_y = 1
        self.is_wind_blowing = 0
        self.env = env
        self.active_modifications = set()

    def wind(self):
        """
        Randomly wiggles the ball
        """
        if random.random() < 0.01 and self.is_wind_blowing == 0:
            # randomly wind will start to blow
            self.is_wind_blowing = 10
        elif self.is_wind_blowing > 0:
            # it will blow for 10 steps
            self.is_wind_blowing = self.is_wind_blowing - 1
            
            # it will change direction randomly
            if random.random() < 0.1:
                self.wind_direction_x = self.wind_direction_x * -1
            if random.random() < 0.1:
                self.wind_direction_y = self.wind_direction_y * -1

            ram = self.env.get_ram()
            x,y = ram[52], ram[91]

            new_x = x + self.wind_direction_x
            new_y = y + self.wind_direction_y

            new_x = max(0, min(255, new_x))
            new_y = max(0, min(255, new_y))

            self.env.set_ram(52, new_x)
            self.env.set_ram(91, new_y)

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
            "wind": self.wind,
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