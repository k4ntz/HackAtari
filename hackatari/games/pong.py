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

    def lazy_enemy(self):
        """
        Enemy does not move after returning the shot.
        """
        ram = self.env.get_ram()
        if 0 < ram[11] < 5:
            self.env.set_ram(21, 127)
            self.env.set_ram(49, 130)
        if self.ball_previous_x_pos < ram[49]:
            self.env.set_ram(21, self.last_enemy_y_pos)
            tmp = self.last_enemy_y_pos
        else:
            tmp = ram[21]
        self.ball_previous_x_pos = ram[49]
        self.last_enemy_y_pos = tmp

    def up_drift(self):
        """
        Makes the ball drift upwards.
        """
        ball_y = self.env.get_ram()[54]
        new_ball_pos = ball_y - 1
        if ball_y != 0 and not self.timer % self.strength:
            self.env.set_ram(54, new_ball_pos)
        self.timer += 1

    def down_drift(self):
        """
        Makes the ball drift downwards.
        """
        ball_y = self.env.get_ram()[54]
        new_ball_pos = ball_y + 1
        if ball_y != 0 and not self.timer % self.strength:
            self.env.set_ram(54, new_ball_pos)
        self.timer += 1

    def right_drift(self):
        """
        Makes the ball drift to the right.
        """
        ball_x = self.env.get_ram()[49]
        new_ball_pos = ball_x + 1
        if ball_x != 0 and not self.timer % self.strength:
            self.env.set_ram(49, new_ball_pos)
        self.timer += 1

    def left_drift(self):
        """
        Makes the ball drift to the left.
        """
        ball_x = self.env.get_ram()[49]
        new_ball_pos = ball_x - 1
        if ball_x != 0 and not self.timer % self.strength:
            self.env.set_ram(49, new_ball_pos)
        self.timer += 1

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
            "lazy_enemy": self.lazy_enemy,
            "up_drift": self.up_drift,
            "down_drift": self.down_drift,
            "left_drift": self.left_drift,
            "right_drift": self.right_drift,
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
    