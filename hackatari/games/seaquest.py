import random


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
        self.current_colors = [random.randint(0, 200) for _ in range(4)]
        self.timer = 0

    def gravity(self):
        """
        Enables gravity for the player.
        """
        ram = self.env.get_ram()
        if ram[97] < 105 and not self.timer % 5:
            self.env.set_ram(97, ram[97] + 1)
        self.timer += 1

    def disable_enemies(self):
        """
        Disables all the enemies.
        """
        for x in range(4):  # disables underwater enemies
            self.env.set_ram(36 + x, 0)
        self.env.set_ram(60, 0)  # disables surface enemies

    def is_gamestart(self):
        """
        Determines if it is the start of the game
        via the position of the player and the points.
        """
        ram = self.env.get_ram()
        return ram[97] == 13 and ram[70] == 76 and ram[26] == 80

    def unlimited_oxygen(self):
        """
        Changes the behavior of the oxygen bar to remain filled.
        """
        ram = self.env.get_ram()
        if ram[97] > 13:  # when not surfacing
            self.env.set_ram(102, 63)
        if self.is_gamestart():
            self.env.set_ram(59, 3)  # replace life if lost because of bug

    def random_color_enemies(self):
        """
        The enemies have new random colors each time they go across the screen.
        """
        ram = self.env.get_ram()
        for i in range(4):
            if ram[30 + i] == 200:  # if the enemy is not in frame
                self.current_colors[i] = random.randint(0, 255)
            self.env.set_ram(44 + i, self.current_colors[i])

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
            "unlimited_oxygen": self.unlimited_oxygen,
            "gravity": self.gravity,
            "disable_enemies": self.disable_enemies,
            "random_color_enemies": self.random_color_enemies,
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
