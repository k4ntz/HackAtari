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
        self.towns_visited = []
        self.remaining_towns = [i for i in range(256)]
        random.shuffle(self.remaining_towns)
        self.current_town = 0
        self.player_x = 0

    def unlimited_gas(self):
        """
        Provides unlimited gas for all enemies.
        """
        self.env.set_ram(86, 0)

    def no_police(self):
        """
        Removes police from the game.
        """
        ram = self.env.get_ram()
        for i in range(3):
            if ram[24 + i] == 254:
                self.env.set_ram(24 + i, 0)

    def only_police(self):
        """
        Replaces all banks with police.
        """
        ram = self.env.get_ram()
        for i in range(3):
            if ram[24 + i] == 253:
                self.env.set_ram(24 + i, 254)

    def random_city(self):
        """
        Randomizes which city is entered next.
        """
        ram = self.env.get_ram()
        city = ram[0]
        if city == self.current_town + 1:  # arrived to new city
            picked_city = self.remaining_towns.pop(0)
            self.current_town = picked_city
            if len(self.remaining_towns) == 0:  # reset
                self.remaining_towns = [i for i in range(256)]
                random.shuffle(self.remaining_towns)
            self.towns_visited.append(picked_city)
            self.env.set_ram(0, picked_city)

    # def random_city_res(self):
    #     """
    #     Resets the city randomizer.
    #     """
    #     self.remaining_towns = [i for i in range(256)]
    #     random.shuffle(self.remaining_towns)
    #     picked_city = self.remaining_towns.pop(0)
    #     self.current_town = picked_city
    #     self.towns_visited.append(picked_city)
    #     self.env.set_ram(0, picked_city)

    def revisit_city(self):
        """
        Allows player to go back to the previous city.
        """
        ram = self.env.get_ram()
        if 16 > self.player_x and ram[28] > 120:
            self.player_x = 0
            if self.current_town == 0:
                self.current_town = 255
            else:
                self.current_town -= 1
            self.env.set_ram(0, self.current_town)
        else:
            self.current_town = ram[0]
        self.player_x = ram[28]

    def _set_active_modifications(self, active_modifs):
        """
        Specifies which modifications are active.

        :param active_modifs: A list of active modification names.
        """
        self.active_modifications = set(active_modifs)

    def _fill_modif_lists(self):
        """
        Returns the modification lists (step, reset, and post-detection) with active modifications.

        :return: Tuple of step_modifs, reset_modifs, and post_detection_modifs.
        """
        modif_mapping = {
            "unlimited_gas": self.unlimited_gas,
            "no_police": self.no_police,
            "only_police": self.only_police,
            "random_city": self.random_city,
            "revisit_city": self.revisit_city,
        }

        step_modifs = [modif_mapping[name]
                       for name in self.active_modifications if name in modif_mapping]
        reset_modifs = []
        if "random_city" in self.active_modifications:
            reset_modifs.append(self.random_city_res)
        post_detection_modifs = []
        return step_modifs, reset_modifs, post_detection_modifs


def modif_funcs(env, active_modifs):
    modifications = GameModifications(env)
    modifications._set_active_modifications(active_modifs)
    return modifications._fill_modif_lists()
