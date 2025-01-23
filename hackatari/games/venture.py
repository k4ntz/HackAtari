import random


class GameModifications:
    """
    Encapsulates game modifications for managing active modifications and applying them.
    """

    COLORS = [0, 12, 48, 113, 200]  # Black, White, Red, Blue, Green

    def __init__(self, env):
        """
        Initializes the modification handler with the given environment.
        """
        self.env = env
        self.active_modifications = set()
        self.enemy_color = 0
        self.enemy_random_colors = [0] * 6
        self.room = 8

    def enemy_color_black(self):
        """
        Changes all enemies to black.
        """
        self._set_enemy_color(0)

    def enemy_color_white(self):
        """
        Changes all enemies to white.
        """
        self._set_enemy_color(1)

    def enemy_color_red(self):
        """
        Changes all enemies to red.
        """
        self._set_enemy_color(2)

    def enemy_color_blue(self):
        """
        Changes all enemies to blue.
        """
        self._set_enemy_color(3)

    def enemy_color_green(self):
        """
        Changes all enemies to green.
        """
        self._set_enemy_color(4)

    def _set_enemy_color(self, color_index):
        """
        Changes the color of all enemies to the specified color.
        """
        ram = self.env.get_ram()
        color_value = self.COLORS[color_index]
        if ram[90] not in [8, 9]:
            for i in range(5):
                self.env.set_ram(37 + i, color_value)
        else:
            for i in range(6):
                self.env.set_ram(36 + i, color_value)

    def random_enemy_colors(self):
        """
        Assigns a random color to each enemy from the five available colors.
        """
        ram = self.env.get_ram()
        if ram[90] not in [8, 9]:
            for i in range(5):
                self.env.set_ram(37 + i, self.enemy_random_colors[i])
        else:
            for i in range(6):
                self.env.set_ram(36 + i, self.enemy_random_colors[i])

        if self.room != ram[90]:
            self.room = ram[90]
            for i in range(6):
                self.enemy_random_colors[i] = random.choice(self.COLORS)

    def reset_random_colors(self):
        """
        Resets the enemy colors to new random values.
        """
        for i in range(6):
            self.enemy_random_colors[i] = random.choice(self.COLORS)

    def _set_active_modifications(self, active_modifs):
        """
        Specifies which modifications are active.
        """
        for mod in active_modifs:
            if mod == "random_enemy_colors":
                self.active_modifications.add("random_enemy_colors")
                self.active_modifications.add("reset_random_colors")
            elif mod == "enemy_color_black":
                self.active_modifications.add("enemy_color_black")
            elif mod == "enemy_color_white":
                self.active_modifications.add("enemy_color_white")
            elif mod == "enemy_color_red":
                self.active_modifications.add("enemy_color_red")
            elif mod == "enemy_color_blue":
                self.active_modifications.add("enemy_color_blue")
            elif mod == "enemy_color_green":
                self.active_modifications.add("enemy_color_green")

    def _fill_modif_lists(self):
        """
        Returns the modification lists (step, reset, and post-detection) with active modifications.
        """
        modif_mapping = {
            "random_enemy_colors": self.random_enemy_colors,
            "reset_random_colors": self.reset_random_colors,
            "enemy_color_black": self.enemy_color_black,
            "enemy_color_white": self.enemy_color_white,
            "enemy_color_red": self.enemy_color_red,
            "enemy_color_blue": self.enemy_color_blue,
            "enemy_color_green": self.enemy_color_green,
        }

        step_modifs = [modif_mapping[name]
                       for name in self.active_modifications if name in modif_mapping]
        reset_modifs = [
            self.reset_random_colors] if "random_enemy_colors" in self.active_modifications else []
        post_detection_modifs = []

        return step_modifs, reset_modifs, post_detection_modifs


def modif_funcs(env, active_modifs):
    modifications = GameModifications(env)
    modifications._set_active_modifications(active_modifs)
    return modifications._fill_modif_lists()
