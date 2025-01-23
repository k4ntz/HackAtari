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

    def endless_oxygen(self):
        """
        Player can no longer run out of oxygen. Will not be set at max, so oxygen can always be picked up.
        """
        self.env.set_ram(113, 255)

    def infinite_lives(self):
        """
        Always maximizes the treasure value (represents the remaining lives).
        """
        self.env.set_ram(73, 3)

    def double_wave_length(self):
        """
        Doubles the time of each wave.
        """
        ram = self.env.get_ram()
        bit = 7
        repeat = True

        if repeat:
            try:
                if ram[114] and not ram[114] & (2 ** bit):
                    self.env.set_ram(114, ram[114] | (2 ** bit))
                    repeat = False
                elif not ram[114] and not ram[115] & (2 ** bit):
                    self.env.set_ram(115, ram[115] | (2 ** bit))
                    repeat = False
            except:
                pass
        else:
            if ram[114] and not ram[114] & (2 ** bit):
                bit -= 1
                repeat = True
            elif not ram[114] and ram[115] & (2 ** bit):
                bit += 1
                repeat = True

    def quick_start(self):
        """
        Skips the intro and starts the game at once.
        """
        self.env.set_ram(65, 10)

    def octopus_start(self):
        """
        Adds the first lane of tentacles for the octopus.
        """
        for i in range(5):
            self.env.set_ram(9 + (10 * i), 64)

    def octopus_rest(self):
        """
        Resets the timer for the octopus tentacles.
        """
        self.env.set_ram(9, 0)

    def _set_active_modifications(self, active_modifs):
        """
        Specifies which modifications are active.
        """
        self.active_modifications = set(active_modifs)

    def _fill_modif_lists(self):
        """
        Returns the modification lists (step, reset, and post-detection) with active modifications.

        :return: Tuple of step_modifs, reset_modifs, and post_detection_modifs.
        """
        modif_mapping = {
            "endless_oxygen": self.endless_oxygen,
            "infinite_lives": self.infinite_lives,
            "double_wave_length": self.double_wave_length,
            "quick_start": self.quick_start,
            "octopus_start": self.octopus_start,
            "octopus_rest": self.octopus_rest,
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
