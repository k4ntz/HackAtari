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
        self.gravity_level = 3
        self.player_color = 0  # Black, Red, Blue, Green
        self.enemy_color = 0  # White, Red, Blue, Green
        self.once = 0
        self.colors = [0, 12, 48, 113, 200]

    def one_armed(self):
        """
        Disables the "hitting motion" with the right arm permanently.
        """
        self.env.set_ram(101, 128)

    def gravity(self):
        """
        Increases the value in RAM cell 34 until reaching a threshold to simulate gravity.
        """
        curr_player_pos = self.env.get_ram()[34]
        if curr_player_pos < 87:
            if not self.env.timer % self.gravity_level:
                curr_player_pos += 1
                self.env.set_ram(34, curr_player_pos)
        self.env.timer += 1

    def offensive(self):
        """
        Moves the player character forward in the game environment.
        """
        curr_player_pos_x = self.env.get_ram()[32]
        curr_player_pos_x_enemy = self.env.get_ram()[33]

        if 0 < curr_player_pos_x < 109 and curr_player_pos_x + 14 != curr_player_pos_x_enemy:
            curr_player_pos_x += 1
            self.env.set_ram(32, curr_player_pos_x)

    def antigravity(self):
        """
        Moves the player character up in the game environment.
        """
        curr_player_pos_y = self.env.get_ram()[34]

        if 0 < curr_player_pos_y < 87:
            curr_player_pos_y -= 1
            self.env.set_ram(34, curr_player_pos_y)

    def defensive(self):
        """
        Moves the player character backward in the game environment.
        """
        curr_player_pos_x = self.env.get_ram()[32]

        if 0 < curr_player_pos_x < 109:
            curr_player_pos_x -= 1
            self.env.set_ram(32, curr_player_pos_x)

    def down(self):
        """
        Moves the player character down in the game environment.
        """
        curr_player_pos_y = self.env.get_ram()[34]

        if 0 < curr_player_pos_y < 87:
            curr_player_pos_y += 1
            self.env.set_ram(34, curr_player_pos_y)

    def drunken_boxing(self):
        """
        Applies random movements to the player's input.
        """
        r = random.randint(0, 1)
        if r == 0:
            self.env.counter = getattr(self.env, "counter", 0)
            do = self.env.counter % 4
            self.env.counter += 1
        else:
            do = random.randint(0, 3)

        if do == 0:
            self.offensive()
        elif do == 1:
            self.antigravity()
        elif do == 2:
            self.defensive()
        elif do == 3:
            self.down()

    def color_player_black(self):
        """
        Changes the player's color to black.
        """
        self.env.set_ram(1, self.colors[0])

    def color_player_white(self):
        """
        Changes the player's color to white.
        """
        self.env.set_ram(1, self.colors[1])

    def color_player_red(self):
        """
        Changes the player's color to red.
        """
        self.env.set_ram(1, self.colors[2])

    def color_player_blue(self):
        """
        Changes the player's color to blue.
        """
        self.env.set_ram(1, self.colors[3])

    def color_player_green(self):
        """
        Changes the player's color to green.
        """
        self.env.set_ram(1, self.colors[4])

    def color_enemy_black(self):
        """
        Changes the enemy's color to black.
        """
        self.env.set_ram(2, self.colors[0])

    def color_enemy_white(self):
        """
        Changes the enemy's color to white.
        """
        self.env.set_ram(2, self.colors[1])

    def color_enemy_red(self):
        """
        Changes the enemy's color to red.
        """
        self.env.set_ram(2, self.colors[2])

    def color_enemy_blue(self):
        """
        Changes the enemy's color to blue.
        """
        self.env.set_ram(2, self.colors[3])

    def color_enemy_green(self):
        """
        Changes the enemy's color to green.
        """
        self.env.set_ram(2, self.colors[4])

    def switch_positions(self):
        """
        Switches the position of player and enemy.
        """
        if self.once:
            self.env.set_ram(33, 30)
            self.env.set_ram(35, 4)
            self.env.set_ram(32, 105)
            self.env.set_ram(34, 85)
            self.once -= 1

    def reset_once(self):
        """
        Resets the "once" variable to its initial value.
        """
        self.once = 2

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
            "one_armed": self.one_armed,
            "gravity": self.gravity,
            "drunken_boxing": self.drunken_boxing,
            "color_player_black": self.color_player_black,
            "color_player_white": self.color_player_white,
            "color_player_red": self.color_player_red,
            "color_player_blue": self.color_player_blue,
            "color_player_green": self.color_player_green,
            "color_enemy_black": self.color_enemy_black,
            "color_enemy_white": self.color_enemy_white,
            "color_enemy_red": self.color_enemy_red,
            "color_enemy_blue": self.color_enemy_blue,
            "color_enemy_green": self.color_enemy_green,
            "switch_positions": self.switch_positions,
        }

        step_modifs = [modif_mapping[name]
                       for name in self.active_modifications if name in modif_mapping]
        reset_modifs = []
        if "switch_positions" in self.active_modifications:
            reset_modifs.append(self.reset_once)
        post_detection_modifs = []
        return step_modifs, reset_modifs, post_detection_modifs


def modif_funcs(env, active_modifs):
    modifications = GameModifications(env)
    modifications._set_active_modifications(active_modifs)
    return modifications._fill_modif_lists()
