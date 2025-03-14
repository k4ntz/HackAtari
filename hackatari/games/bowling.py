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

    def _set_active_modifications(self, active_modifs):
        """
        Specifies which modifications are active.

        :param active_modifs: A list of active modification names.
        """
        self.active_modifications = set(active_modifs)
    
    def shift_player(self):
        """
        Shifts the player to the left.
        """
        ram = self.env.get_ram()
        all_down = True
        for r in range(57, 67):
            if ram[r] != 255:
                all_down = False
                break
        if ram[42] == 184 and not all_down:
            self.env.set_ram(29, 20)
            self.env.set_ram(30, 27)
            player, ball = self.env.objects[0: 2]
            player.x = 28
            ball.x = 34

    def horizontal_pins(self):
        """
        Draws the pins horizontally instead of vertically.
        """
        ram = self.env.get_ram()
        for r in range(97, 117):
            if ram[r] == 2 and ram[r+1] == 2:
                self.env.set_ram(r, 3)
                self.env.set_ram(r+1, 0)
            elif ram[r] == 8 and ram[r+1] == 8:
                self.env.set_ram(r, 12)
                self.env.set_ram(r+1, 0)
            elif ram[r] == 34 and ram[r+1] == 34:
                self.env.set_ram(r, 51)
                self.env.set_ram(r+1, 0)
            elif ram[r] == 136 and ram[r+1] == 136:
                self.env.set_ram(r, 204)
                self.env.set_ram(r+1, 0)

    def small_pins(self):
        """
        Decreases pin size to 1 pixel.
        """
        ram = self.env.get_ram()
        for r in range(97, 117):
            if ram[r] == 2 and ram[r+1] == 2:
                self.env.set_ram(r+1, 0)
            elif ram[r] == 8 and ram[r+1] == 8:
                self.env.set_ram(r+1, 0)
            elif ram[r] == 34 and ram[r+1] == 34:
                self.env.set_ram(r+1, 0)
            elif ram[r] == 136 and ram[r+1] == 136:
                self.env.set_ram(r+1, 0)


    def top_pins(self):
        """
        Removes all but the top two pins
        """
        ram = self.env.get_ram()
        if ram[57] != 255:
            for i in range(57, 67):
                if i != 60 and i != 63:
                    self.env.set_ram(i, 255)
                    self.env.set_ram(i+10, 255)
            for i in range(97, 112):
                self.env.set_ram(i, 0)

    def middle_pins(self):
        """
        Removes all but the two middle pins
        """
        ram = self.env.get_ram()
        if ram[57] != 255:
            for i in range(58, 67):
                if i != 61:
                    self.env.set_ram(i, 255)
                    self.env.set_ram(i+10, 255)
            for i in range(97, 117):
                if i != 106 and i != 107:
                    self.env.set_ram(i, 0)

    def bottom_pins(self):
        """
        Removes all but the bottom two pins
        """
        ram = self.env.get_ram()
        if ram[57] != 255:
            for i in range(57, 66):
                if i != 62:
                    self.env.set_ram(i, 255)
                    self.env.set_ram(i+10, 255)
            for i in range(102, 117):
                self.env.set_ram(i, 0)

    def _fill_modif_lists(self):
        """
        Returns the modification lists (step, reset, and post-detection) with active modifications.

        :return: Tuple of step_modifs, reset_modifs, and post_detection_modifs.
        """
        modif_mapping = {
            "top_pins": self.top_pins,
            "middle_pins": self.middle_pins,
            "bottom_pins": self.bottom_pins,
            "shift_player": self.shift_player,
            "horizontal_pins": self.horizontal_pins,
            "small_pins": self.small_pins,
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
