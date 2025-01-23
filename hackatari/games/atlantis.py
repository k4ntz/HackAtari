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

    def no_last_line(self):
        """
        Removes enemies from the last (lowest) line.
        """
        self.env.set_ram(36, 0)

    def jets_only(self):
        """
        Replaces all enemies with Bandit-Bombers.
        """
        ram = self.env.get_ram()
        for i in range(4):
            if ram[82 - i] and ram[82 - i] < 80:
                self.env.set_ram(82 - i, 80)
                if ram[78 - i] == 1:
                    self.env.set_ram(78 - i, 2)
                elif ram[78 - i] == 255:
                    self.env.set_ram(78 - i, 254)

    def random_enemies(self):
        """
        Randomly assigns enemy types, instead of following the standardized pattern.
        """
        ram = self.env.get_ram()
        types = [32, 64, 80]
        for i in range(4):
            if ram[79 + i] and ram[79 + i] < 81:
                enemy = random.choice(types)
                self.env.set_ram(79 + i, enemy)
                if enemy < 80:
                    if ram[75 + i] == 2:
                        self.env.set_ram(75 + i, 1)
                    elif ram[75 + i] == 254:
                        self.env.set_ram(75 + i, 255)
                else:
                    if ram[75 + i] == 1:
                        self.env.set_ram(75 + i, 2)
                    elif ram[75 + i] == 255:
                        self.env.set_ram(75 + i, 254)

    def speed_mode_slow(self):
        """
        Sets a slow speed for all enemy ships.
        """
        self._adjust_speed(2)

    def speed_mode_medium(self):
        """
        Sets a normal speed for all enemy ships.
        """
        self._adjust_speed(4)

    def speed_mode_fast(self):
        """
        Sets a fast speed for all enemy ships.
        """
        self._adjust_speed(6)

    def speed_mode_ultrafast(self):
        """
        Sets an ultra-fast speed for all enemy ships.
        """
        self._adjust_speed(8)

    def _adjust_speed(self, speed):
        """
        Adjusts the speed of all enemy ships.

        :param speed: The speed value to set.
        """
        ram = self.env.get_ram()
        for i in range(4):
            if ram[79 + i] == 80:
                if ram[75 + i] & 128:
                    self.env.set_ram(75 + i, 255 - speed)
                elif ram[75 + i] > 0:
                    self.env.set_ram(75 + i, 1 + speed)
            else:
                if ram[75 + i] & 128:
                    self.env.set_ram(75 + i, 256 - speed)
                elif ram[75 + i] > 0:
                    self.env.set_ram(75 + i, speed)

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
            "no_last_line": self.no_last_line,
            "jets_only": self.jets_only,
            "random_enemies": self.random_enemies,
            "speed_mode_slow": self.speed_mode_slow,
            "speed_mode_medium": self.speed_mode_medium,
            "speed_mode_fast": self.speed_mode_fast,
            "speed_mode_ultrafast": self.speed_mode_ultrafast,
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
