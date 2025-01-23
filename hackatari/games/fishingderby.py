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
        self.fish_mode = 0  # Default fish mode
        self.shark_mode = 0  # Default shark mode
        self.active_modifications = set()

    def shark_no_movement_easy(self):
        """
        Shark mode: no movement (easy).
        """
        self.env.set_ram(75, 105)

    def shark_no_movement_hard(self):
        """
        Shark mode: no movement (hard).
        """
        self.env.set_ram(75, 25)

    def shark_teleport(self):
        """
        Shark mode: teleport.
        """
        current_x_position = self.env.get_ram()[75]
        if current_x_position == 100:
            self.env.set_ram(75, 25)
        elif current_x_position == 30:
            self.env.set_ram(75, 105)

    def shark_speed_mode(self):
        """
        Shark mode: speed mode.
        """
        current_x_position = self.env.get_ram()[75]
        if current_x_position < 120:
            self.env.set_ram(75, current_x_position + 5)
        elif current_x_position > 120:
            self.env.set_ram(75, 1)

    def fish_on_player_side(self):
        """
        Fish mode: all fish are on the player's side.
        """
        for i in range(6):
            if self.env.get_ram()[69 + i] > 86:
                self.env.set_ram(69 + i, 44)

    def fish_in_middle(self):
        """
        Fish mode: fish are always in the middle between player and enemy.
        """
        for i in range(6):
            if self.env.get_ram()[112] != i + 1 or self.env.get_ram()[113] != i + 1:
                if self.env.get_ram()[69 + i] < 70:
                    self.env.set_ram(69 + i, 86)
                elif self.env.get_ram()[69 + i] > 86:
                    self.env.set_ram(69 + i, 70)

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
            # "shark_no_movement_easy": self.shark_no_movement_easy,
            # "shark_no_movement_hard": self.shark_no_movement_hard,
            "shark_teleport": self.shark_teleport,
            "shark_speed_mode": self.shark_speed_mode,
            "fish_on_player_side": self.fish_on_player_side,
            "fish_in_middle": self.fish_in_middle,
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
