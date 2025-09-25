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

    def pig_enemies(self):
        """
        Make enemies become pigs.
        """
        ram = self.env.get_ram()
        for i in range(7):
            if ram[73 + i] & 32:
                self.env.set_ram(73 + i, ram[73 + i] | 16)

    def paint_roller_player(self):
        """
        Changes the player to a paint roller.
        """
        ram = self.env.get_ram()
        for i in range(7):
            if not ram[73 + i] & 32:
                self.env.set_ram(73 + i, ram[73 + i] | 16)

    def unlimited_lives(self):
        """
        The player never loses any lives.
        """
        ram = self.env.get_ram()
        self.env.set_ram(86, ram[86] | 3)

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
                "pig_enemies": self.pig_enemies,
                "paint_roller_player": self.paint_roller_player,
                "unlimited_lives": self.unlimited_lives,
            },
            "reset_modifs": {
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
