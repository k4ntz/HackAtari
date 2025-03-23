import random


# Warning: Doesn't work right now.


class GameModifications:
    """
    Encapsulates game modifications for managing active modifications and applying them.
    """

    def __init__(self, env):
        """
        Initializes the modification handler with the given environment.
        """
        self.wind_direction_x = 1
        self.is_wind_blowing = 0
        self.current_player_x = None
        self.old_player_x = None
        self.older_player_x = None
        self.env = env
        self.active_modifications = set()

    def missle_guide(self):
        """
        player guides missle left and right
        """
        # ram[93] -> missle x between 86-211
        # ram[89] -> missle y between 25-193

        ram = self.env.get_ram()
        if self.current_player_x is None and self.old_player_x is None and self.older_player_x is None:
            self.older_player_x = ram[94]
        elif self.current_player_x is None and self.older_player_x is None:
            self.older_player_x = ram[94]
        elif self.current_player_x is None:
            self.current_player_x = ram[94]
        else:
            self.older_player_x = self.old_player_x
            self.old_player_x = self.current_player_x
            self.current_player_x = ram[94]

            try:
                if self.current_player_x - self.older_player_x == 255:
                    diff = -1
                else:
                    diff = self.current_player_x - self.older_player_x
                
                missle_x = ram[93]
                new_missle_x = missle_x + diff * 1
                new_missle_x = max(86, min(211, new_missle_x))
                self.env.set_ram(93, new_missle_x)
            except:
                pass

    def player_drift(self):
        """
        randomly wind blows to player ship
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

            ram = self.env.get_ram()
            player_x = ram[94] # between 82 and 207

            new_player_x = player_x + self.wind_direction_x * 1
            new_player_x = max(82, min(207, new_player_x))
            self.env.set_ram(94, new_player_x)

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
            "missle_guide": self.missle_guide,
            "player_drift": self.player_drift,
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