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

    def no_fuel(self):
        """
        Removes the fuel deposits from the game.
        """
        ram = self.env.get_ram()
        self.env.set_ram(55, 255)
        for i in range(6):
            obj_type = ram[32 + i]
            if obj_type == 10:  # fuel deposit
                self.env.set_ram(32 + i, 0)

    def red_river(self):
        """
        Turns the river red.
        """
        self.env.set_ram(13, 0xFF)

    def GameColorChange01(self):
        """
        Turns all elements of the game to another colorset (01)
        """
        self.env.set_ram(119, 144)

    def GameColorChange02(self):
        """
        Turns all elements of the game to another colorset (02)
        """
        self.env.set_ram(119, 164)

    def GameColorChange03(self):
        """
        Turns all elements of the game to another colorset (03)
        """
        self.env.set_ram(76, 184)

    def ObjectColorChange01(self):
        """
        Turns all elements of the game to another colorset (01)
        """
        self.env.set_ram(76, 144)

    def ObjectColorChange02(self):
        """
        Turns all elements of the game to another colorset (02)
        """
        self.env.set_ram(76r, 164)

    def ObjectColorChange03(self):
        """
        Turns all elements of the game to another colorset (03)
        """
        self.env.set_ram(119, 184)

    def LinearRiver(self):
        """
        Makes the river straight, however objects still spwan at their normal position making them unreachable in the worst case
        """
        for i in range(14, 20):
            self.env.set_ram(i, 0x05)
        for i in range(38, 44):
            self.env.set_ram(i, 35)
        for i in range(44, 50):
            self.env.set_ram(i, 0)

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
            "no_fuel": self.no_fuel,
            "red_river": self.red_river,
            "linear_river": self.LinearRiver,
            "game_color_change01": self.GameColorChange01,
            "game_color_change02": self.GameColorChange02,
            "game_color_change03": self.GameColorChange03,
            "object_color_change01": self.ObjectColorChange01,
            "object_color_change02": self.ObjectColorChange02,
            "object_color_change03": self.ObjectColorChange03,

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
