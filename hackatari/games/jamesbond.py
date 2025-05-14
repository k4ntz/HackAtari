class GameModifications():
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
        self.strength = 6
        self.timer = 0
        self.last_enemy_y_pos = 127
        self.ball_previous_x_pos = 130

    def constant_jump(self):
        """
        Makes the player character jump constantly.
        """
        self.env.set_ram(25, 60)
        self.env.set_ram(36, 0)
    
    def fast_backward(self):
        ram = self.env.get_ram()
        if self.prevpx > ram[27]:
            self.prevpx = max(ram[27]-1, 10)
            self.env.set_ram(27, self.prevpx)
        else:
            self.prevpx = ram[27]
    
    def mobile_player(self):
        self.constant_jump()
        self.fast_backward()
    
    def straight_shots(self):
        """
        Makes the player character shoot straight.
        """
        ram = self.env.get_ram()
        if ram[38]:
            if self.prev38 == 0:
                self.prev38 = ram[38] - 8
            else:
                self.env.set_ram(38, self.prev38)
        else:
            self.prev38 = 0
        self.env.objects[1].x += 2
        self.env.objects[1].y += 1

    def unlimited_lives(self):
        """
        The players lives do not decrease.
        """
        self.env.set_ram(6, 5)

    def _set_active_modifications(self, active_modifs):
        """
        Specifies which modifications are active.
        """
        self.active_modifications = set(active_modifs)

    def _fill_modif_lists(self):
        """
        Returns the modification lists (step, reset, and post-detection) with active modifications.
        """
        self.prev38 = 0
        self.prevpx = 0
        modif_mapping = {
            "constant_jump": self.constant_jump,
            "straight_shots": self.straight_shots,
            "fast_backward": self.fast_backward,
            "mobile_player": self.mobile_player,
            "unlimited_lives": self.unlimited_lives,
        }

        step_modifs = [modif_mapping[name]
                       for name in self.active_modifications if name in modif_mapping]
        reset_modifs = []
        post_detection_modifs = step_modifs
        return step_modifs, reset_modifs, post_detection_modifs


def modif_funcs(env, active_modifs):
    modifications = GameModifications(env)
    modifications._set_active_modifications(active_modifs)
    return modifications._fill_modif_lists()
