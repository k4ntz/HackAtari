import random
from ocatari.ram._helper_methods import _convert_number

def _encode_number(n):
    """
    Encodes a two-digit decimal number into a pseudo-BCD format
    used by some Atari games, where each nibble is a digit.
    Any digit > 9 is clamped to 9.
    """
    tens = min(n // 10, 9)
    ones = min(n % 10, 9)
    return (tens << 4) | ones


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
    
    def write_score_to_ram(self, score):
        """
        Converts a decimal score into the format used by the game RAM and writes it into ram[88], ram[89], ram[90].

        :param score: Integer score to encode (max 999999)
        :param ram: List or bytearray representing the RAM
        """
        # Clamp score to 6 digits max (because 3 * 2 digits)
        score = min(score, 999999)

        # Break score into 3 parts: units, hundreds, ten-thousands
        unit = score % 100
        hundred = (score // 100) % 100
        tenthousand = (score // 10000) % 100

        self.env.set_ram(90, _encode_number(unit))
        self.env.set_ram(89, _encode_number(hundred))
        self.env.set_ram(88, _encode_number(tenthousand))

    def unlimited_gas(self):
        """
        Provides unlimited gas to the player.
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
    
    def two_police_cars(self):
        """
        Replaces 2 banks with police cars. Robbed banks give 50 points.
        """
        ram = self.env.get_ram()
        nb_police = 0
        score = _convert_number(ram[90]) + \
                100 * _convert_number(ram[89]) + \
                10000 * _convert_number(ram[88])
        if self.score != score:
            self.score = score + 50
            self.write_score_to_ram(self.score)
        for i in range(3):
            if ram[24 + i] == 254:
                nb_police += 1
        if nb_police < 2: # change 2 banks to police cars
            for i in range(3):
                if (ram[29+i] < 47 or ram[29 + i] > 120) and 25 < ram[9+i] < 71:
                    if ram[9+i] == 41 or ram[9+i] == 49: # move closeby banks
                        self.env.set_ram(71+i, 1)
                    continue
                if ram[24 + i] == 253:
                    self.env.set_ram(24 + i, 254)
                    # self.env.set_ram(83, 4)
                    nb_police += 1
                if nb_police == 2:
                    if ram[11] == 41 or ram[11] == 49:
                        self.env.set_ram(73, 1)      
                    break
            

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
            "two_police_cars": self.two_police_cars,
            "random_city": self.random_city,
            "revisit_city": self.revisit_city,
        }

        step_modifs = [modif_mapping[name]
                       for name in self.active_modifications if name in modif_mapping]
        self.score = 0
        reset_modifs = []
        if "random_city" in self.active_modifications:
            reset_modifs.append(self.random_city)
        post_detection_modifs = []
        return step_modifs, reset_modifs, post_detection_modifs


def modif_funcs(env, active_modifs):
    modifications = GameModifications(env)
    modifications._set_active_modifications(active_modifs)
    return modifications._fill_modif_lists()
