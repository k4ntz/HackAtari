import random

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
        Enemy does not move after returning the shot, until the player hit the ball back.
        """
        ram = self.env.get_ram()
        if 0 < ram[11] < 5:  
            self.env.set_ram(21, 10) # ram 21: enemy y-position
            self.env.set_ram(49, 130) # ram 49: x-position of the ball
        if self.ball_previous_x_pos < ram[49]: # if ball is moving to the right
            self.env.set_ram(21, self.last_enemy_y_pos)
            tmp = self.last_enemy_y_pos
        else:
            tmp = ram[21] # if the ball is not moving to the right update the last_enemy_y_pos
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

    #### My modifications

    def left_up_drift(self):
        """
        Makes the ball drift left up.
        """
        ball_x = self.env.get_ram()[49] # x-position of the ball in ram
        new_ball_x = ball_x - 1
        ball_y = self.env.get_ram()[54] # y-position of the ball in ram
        new_ball_y = ball_y - 1
        if ball_y != 0 and not self.timer % 2:
            self.env.set_ram(54, new_ball_y)
        if ball_x != 0 and not self.timer % 2:
            self.env.set_ram(49, new_ball_x)
        self.timer += 1

    ball_x_prev = 130
    ball_y_prev = 129
    # movement direction
    x_direction = -1
    y_direction = 1
    def speed_ball(self):
        """
        Makes the ball moves faster in every direction.
        """
        ball_x_actual = self.env.get_ram()[49]
        ball_y_actual = self.env.get_ram()[54]

        # movement
        diff_x = int(ball_x_actual) - int(self.ball_x_prev) # Cast Unsigned 8-Bit-Integer to Integer
        diff_y = int(ball_y_actual) - int(self.ball_y_prev)

        if (diff_x <= 0):
            self.x_direction = -1
        else:
            self.x_direction = 1
        
        if (diff_y <= 0):
            self.y_direction = -1
        else:
            self.y_direction = 1

        # new position
        new_ball_x = ball_x_actual + 1*self.x_direction
        new_ball_y = ball_y_actual + 1*self.y_direction
        
        if ball_y_actual != 0 and not self.timer % 2:
            self.env.set_ram(54, new_ball_y)
        if ball_x_actual != 0 and not self.timer % 2:
            self.env.set_ram(49, new_ball_x)

        self.ball_x_prev = self.env.get_ram()[49]
        self.ball_y_prev = self.env.get_ram()[54]
        self.timer += 1

    ball_x_prev = 130
    ball_y_prev = 129
    # movement direction
    x_direction = -1
    y_direction = 1
    def slow_ball(self):
        """
        Makes the ball moves slower in every direction.
        """
        ball_x_actual = self.env.get_ram()[49]
        ball_y_actual = self.env.get_ram()[54]
      
        if ball_y_actual != 0 and not self.timer % 3:
            self.env.set_ram(54, self.ball_y_prev)
        if ball_x_actual != 0 and not self.timer % 3:
            self.env.set_ram(49, self.ball_x_prev)

        self.ball_x_prev = self.env.get_ram()[49]
        self.ball_y_prev = self.env.get_ram()[54]
        self.timer += 1

    def jump_ball(self):
        """
        The ball jumps to a random position in the middle of the field every 200 timesteps.
        """
        if not self.timer % 200:
            rand_number = random.randint(70, 135)
            self.env.set_ram(54, rand_number)
        if not self.timer % 200:
            rand_number = random.randint(70, 135)
            self.env.set_ram(49, rand_number)
        self.timer += 1

    def jump_enemy(self):
        """
        Enemy jums to a random position every 200 timesteps.
        """
        ram = self.env.get_ram()
        if 0 < ram[11] < 5:  
            self.env.set_ram(21, 10) 
            self.env.set_ram(49, 130) 
        if not self.timer % 200:
            rand_number = random.randint(38, 203)
            self.env.set_ram(21, rand_number)  
        self.timer += 1

    def mirror_enemy(self):
        """
        The Enemy is always at the same y-position as the player.
        """
        ram = self.env.get_ram()
        player_y_pos = ram[51]
        self.env.set_ram(21, player_y_pos)


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
            "left_up_drift": self.left_up_drift,
            "speed_ball": self.speed_ball,
            "slow_ball": self.slow_ball,
            "jump_ball": self.jump_ball,
            "jump_enemy": self.jump_enemy,
            "mirror_enemy": self.mirror_enemy
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
    