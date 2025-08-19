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

    def no_trucks(self):
        """
        Removes all opposing trucks from the game.
        """
        ram = self.env.get_ram()
        for i in range(3):
            if ram[37+i] < 8:
                self.env.set_ram(37+i, 23)

    def reduced_trucks(self):
        """
        Reduces amount of opposing trucks on screen to one.
        """
        ram = self.env.get_ram()
        for i in range(3):
            if ram[37+i] < 8:
                self.env.set_ram(37+i, 23)

    def more_trucks(self):
        """
        All collectables (not the flags) are turned into trucks.
        """
        ram = self.env.get_ram()
        for i in range(3):
            if 23 < ram[37+i] < 31:
                self.env.set_ram(37+i, ram[37+i]%8)
    
    def short_game(self):
        """
        Halves the amount of flags required to clear a level
        """

        ram = self.env.get_ram()
        if not ram[4]:
            self.env.set_ram(4, 225)
        

        for i in range(3):
            if 23 < ram[37+i] < 31 and (2**(ram[37+i]%8))& 225:
                self.env.set_ram(37+i, 23)

    def level_1(self):
        self.env.set_ram(3, 1)

    def level_2(self):
        self.env.set_ram(3, 2)

    def level_3(self):
        self.env.set_ram(3, 3)

    def _set_active_modifications(self, active_modifs):
        """
        Specifies which modifications are active.

        :param active_modifs: A list of active modification names.
        """
        self.active_modifications = set(active_modifs)

    def _fill_modif_lists(self):
        """
        Returns the step modification list with active modifications.

        :return: List of step modifications.
        """
        modif_mapping = {
            "step_modifs": {
                "no_trucks": self.no_trucks,
                "reduced_trucks": self.reduced_trucks,
                "short_game": self.short_game,
                "more_trucks": self.more_trucks,
            },
            "reset_modifs": {
                "level_1": self.level_1,
                "level_2": self.level_2,
                "level_3": self.level_3,
            },
            "post_detection_modifs": {
            },
            "inpainting_modifs": {
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
