import random


class GameModifications:
    """
    Encapsulates game modifications for managing active modifications and applying them.
    """

    def __init__(self, env):
        """
        Initializes the modification handler with the given environment.
        """
        self.speed_sign = 1
        self.env = env
        self.active_modifications = set()

    def mother_ship_color(self):
        """
        mother ship changes color randomly
        """
        if random.random() < 0.01:
            self.env.set_ram(11, random.randint(0, 240))
            self.env.set_ram(12, random.randint(0, 240))

    def player_missle(self):
        """
        randomly speeds up or down the player missle
        """
        ram = self.env.get_ram()
        missle_y = ram[67]
        
        # randomly change it to speeding up or slowing down the missle
        if random.random() < 0.01:
            self.speed_sign = self.speed_sign * -1

        if missle_y != 127 and random.random() < 0.1:
            new_missle_y = missle_y + 7 * self.speed_sign
            new_missle_y = max(0, min(255, new_missle_y))
            self.env.set_ram(67, new_missle_y)

    def enemy_color(self):
        """
        randomly makes enemies change color
        """
        if random.random() < 0.1:
            p = random.random()
            if p<0.33:
                self.env.set_ram(40, 196)
            elif 0.33<p<0.66:
                self.env.set_ram(40, 204)
            elif 0.66<p:
                self.env.set_ram(40, 212)


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
            "mother_ship_color": self.mother_ship_color,
            "player_missle": self.player_missle,
            "enemy_color": self.enemy_color,
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