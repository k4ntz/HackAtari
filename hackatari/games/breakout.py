import random

import numpy as np


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
        self.strength = 2
        self.timer = 0
        self.colors = [0, 12, 48, 113, 200]
        self.colors_bricks = [134, 198, 22, 38, 54, 70]
        self.player_and_ball_color = 0  # Black, White, Red, Blue, Green
        self.all_blocks_color = 0  # Black, White, Red, Blue, Green
        self.row_colors = [None] * 6
        self.already_reset = False

    def right_drift(self):
        """
        Makes the ball drift to the right by changing the corresponding RAM positions.
        """
        ball_x = self.env.get_ram()[99]
        ball_y = self.env.get_ram()[101]
        new_ball_pos = ball_x + self.strength

        if (
            (ball_y + 9 <= 196 and new_ball_pos != 0)
            and 57 <= new_ball_pos <= 199
            and not self.timer % 10
        ):
            self.env.set_ram(99, new_ball_pos)
        self.timer += 1

    def left_drift(self):
        """
        Makes the ball drift to the left by changing the corresponding RAM positions.
        """
        ball_x = self.env.get_ram()[99]
        ball_y = self.env.get_ram()[101]
        new_ball_pos = ball_x - self.strength

        if (
            (ball_y + 9 <= 196 and new_ball_pos != 0)
            and 57 <= new_ball_pos <= 199
            and not self.timer % 10
        ):
            self.env.set_ram(99, new_ball_pos)
        self.timer += 1

    def gravity(self):
        """
        Pulls the ball down by changing the corresponding RAM positions.
        """
        ball_y = self.env.get_ram()[101]
        new_ball_pos = ball_y + self.strength

        if 90 <= new_ball_pos <= 165 and not self.timer % 10:
            self.env.set_ram(101, new_ball_pos)
        self.timer += 1

    def inverse_gravity(self):
        """
        Pushes the ball up by changing the corresponding RAM positions.
        """
        ball_y = self.env.get_ram()[101]
        new_ball_pos = ball_y - self.strength

        if 90 <= new_ball_pos <= 180 and not self.timer % 10:
            self.env.set_ram(101, new_ball_pos)
        self.timer += 1

    def color_player_and_ball_black(self):
        self.env.set_ram(62, self.colors[0])

    def color_player_and_ball_white(self):
        self.env.set_ram(62, self.colors[1])

    def color_player_and_ball_red(self):
        self.env.set_ram(62, self.colors[2])

    def color_player_and_ball_blue(self):
        self.env.set_ram(62, self.colors[3])

    def color_player_and_ball_green(self):
        self.env.set_ram(62, self.colors[4])

    def strobo_mode_player_and_ball(self):
        color = random.randint(0, 255)
        self.env.set_ram(62, color)

    def strobo_mode_player_and_ball_no_black(self):
        color = random.randint(1, 255)
        self.env.set_ram(62, color)

    def color_blocks(self, color):
        for i in range(64, 70):
            self.env.set_ram(i, color)

    def color_all_blocks_black(self):
        self.color_blocks(self.colors[0])

    def color_all_blocks_white(self):
        self.color_blocks(self.colors[1])

    def color_all_blocks_red(self):
        self.color_blocks(self.colors[2])

    def color_all_blocks_blue(self):
        self.color_blocks(self.colors[3])

    def color_all_blocks_green(self):
        self.color_blocks(self.colors[4])

    def strobo_mode_blocks(self):
        for i in range(64, 70):
            color = random.randint(0, 255)
            self.env.set_ram(i, color)

    def strobo_mode_blocks_no_black(self):
        for i in range(64, 70):
            color = random.randint(1, 255)
            self.env.set_ram(i, color)

    def sample_new_player_and_ball_color(self):
        if not self.already_reset:
            color = random.choice(self.colors_bricks)
            self.player_and_ball_color = color
            self.already_reset = True
        self.env.set_ram(62, self.player_and_ball_color)

    def sample_new_brick_colors(self):
        if not self.already_reset:
            colors = self.colors_bricks.copy()
            np.random.shuffle(colors)
            for idx, i in enumerate(range(64, 70)):
                self.row_colors[idx] = colors[idx]
            self.already_reset = True

        for idx, i in enumerate(range(64, 70)):
            self.env.set_ram(i, self.row_colors[idx])

    def reset(self):
        self.already_reset = False

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
            "right_drift": self.right_drift,
            "left_drift": self.left_drift,
            "gravity": self.gravity,
            "inverse_gravity": self.inverse_gravity,
            "color_player_and_ball_black": self.color_player_and_ball_black,
            "color_player_and_ball_white": self.color_player_and_ball_white,
            "color_player_and_ball_red": self.color_player_and_ball_red,
            "color_player_and_ball_blue": self.color_player_and_ball_blue,
            "color_player_and_ball_green": self.color_player_and_ball_green,
            "color_all_blocks_black": self.color_all_blocks_black,
            "color_all_blocks_white": self.color_all_blocks_white,
            "color_all_blocks_red": self.color_all_blocks_red,
            "color_all_blocks_blue": self.color_all_blocks_blue,
            "color_all_blocks_green": self.color_all_blocks_green,
            "strobo_mode_blocks": self.strobo_mode_blocks,
            "strobo_mode_player_and_ball": self.strobo_mode_player_and_ball,
            "strobo_mode_blocks_no_black": self.strobo_mode_blocks_no_black,
            "strobo_mode_player_and_ball_no_black": self.strobo_mode_player_and_ball_no_black,
            "sample_new_player_and_ball_color": self.sample_new_player_and_ball_color,
            "sample_new_brick_colors": self.sample_new_brick_colors,
        }
        step_modifs = [
            modif_mapping[name]
            for name in self.active_modifications
            if name in modif_mapping
        ]
        reset_modifs = [self.reset]

        post_detection_modifs = []
        return step_modifs, reset_modifs, post_detection_modifs


def modif_funcs(env, active_modifs):
    modifications = GameModifications(env)
    modifications._set_active_modifications(active_modifs)
    return modifications._fill_modif_lists()
