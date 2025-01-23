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
        self.number_power_pills = 4
        self.lvl_num = 0
        self.lives = 2
        self.timer = 1
        self.toggle_cyan = False
        self.toggle_pink = False
        self.toggle_orange = False
        self.toggle_red = False
        self.col = None
        self.line = None
        self.end_game_pills = 0

    def static_ghosts(self):
        """
        Keeps ghosts fixed inside the square in the middle of the screen.
        """
        if self.toggle_orange:
            self.env.set_ram(6, 93)
            self.env.set_ram(12, 80)
        if self.toggle_cyan:
            self.env.set_ram(7, 83)
            self.env.set_ram(13, 80)
        if self.toggle_pink:
            self.env.set_ram(8, 93)
            self.env.set_ram(14, 67)
        if self.toggle_red:
            self.env.set_ram(9, 83)
            self.env.set_ram(15, 67)

    def edible_ghosts(self):
        """
        Ensures all ghosts remain edible indefinitely.
        """
        for i in range(1, 5):
            self.env.set_ram(i, 130)
        self.env.set_ram(116, 255)

    def set_level_0(self):
        """
        Sets the game level to 0.
        """
        self.env.set_ram(0, 0)

    def set_level_1(self):
        """
        Sets the game level to 1.
        """
        self.env.set_ram(0, 1)

    def set_level_2(self):
        """
        Sets the game level to 2.
        """
        self.env.set_ram(0, 2)

    def end_game(self):
        """
        Simulates an endgame state by spawning only a small cluster of pills.
        """
        for i in range(59, 101):
            if i == self.end_game_pills:
                continue
            self.env.set_ram(i, 0)
        self.env.set_ram(117, 0)

    def _set_active_modifications(self, active_modifs):
        """
        Specifies which modifications are active.
        """
        for mod in active_modifs:
            if mod == "caged_ghosts":
                self.toggle_cyan = self.toggle_orange = self.toggle_red = self.toggle_pink = True
                self.active_modifications.add("static_ghosts")
            elif mod == "disable_orange":
                self.toggle_orange = True
                self.active_modifications.add("static_ghosts")
            elif mod == "disable_red":
                self.toggle_red = True
                self.active_modifications.add("static_ghosts")
            elif mod == "disable_cyan":
                self.toggle_cyan = True
                self.active_modifications.add("static_ghosts")
            elif mod == "disable_pink":
                self.toggle_pink = True
                self.active_modifications.add("static_ghosts")
            elif mod == "edible_ghosts":
                self.active_modifications.add("edible_ghosts")
            elif mod == "set_level_0":
                self.active_modifications.add("set_level_0")
            elif mod == "set_level_1":
                self.active_modifications.add("set_level_1")
            elif mod == "set_level_2":
                self.active_modifications.add("set_level_2")
            elif mod == "end_game":
                self.end_game_pills = random.randint(59, 101)
                self.active_modifications.add("end_game")

    def _fill_modif_lists(self):
        """
        Returns the modification lists (step, reset, and post-detection) with active modifications.
        """
        modif_mapping = {
            "static_ghosts": self.static_ghosts,
            # "edible_ghosts": self.edible_ghosts,
            "set_level_0": self.set_level_0,
            "set_level_1": self.set_level_1,
            "set_level_2": self.set_level_2,
            "end_game": self.end_game,
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
