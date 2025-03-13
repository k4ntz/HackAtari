import numpy as np


class GameModifications:
    """
    Encapsulates game modifications for managing active modifications and applying them.
    """

    def __init__(self, env):
        """
        Initializes the modification handler with the given environment.
        """
        self.env = env
        self.active_modifications = set()

    def disable_shield_left(self):
        """
        Disables the left shield.
        """
        for i in range(43, 52):
            self.env.set_ram(i, 0)

    def disable_shield_middle(self):
        """
        Disables the middle shield.
        """
        for i in range(52, 61):
            self.env.set_ram(i, 0)

    def disable_shield_right(self):
        """
        Disables the right shield.
        """
        for i in range(61, 71):
            self.env.set_ram(i, 0)

    def relocate_shields_slight_left(self):
        """
        Relocates the shields to a low position.
        """
        self.env.set_ram(27, 35)

    def relocate_shields_off_by_one(self):
        """
        Relocates the shields to a medium position.
        """
        self.env.set_ram(27, 44)

    def relocate_shields_right(self):
        """
        Relocates the shields to a high position.
        """
        self.env.set_ram(27, 53)

    def controlable_missile(self):
        """
        Allows the missile to be controlled by setting its position to the player's position.
        """
        self.env.set_ram(87, self.env.get_ram()[28])

#### My modifications

    timer = 0
    def less_aliens(self):
        """
        Just the two upper rows of aliens are spawned.
        """
        if self.timer == 0:
            self.env.set_ram(18,0)
            self.env.set_ram(19,0)
            self.env.set_ram(20,0)
            self.env.set_ram(21,0)
        self.timer += 1

    def triangle_aliens(self):
        """
        The aliens spawn in a triangle shape.
        """
        if self.timer == 0:
            self.env.set_ram(18,0)
            self.env.set_ram(19,0)
            self.env.set_ram(20,0)
            self.env.set_ram(21,12)
            self.env.set_ram(22,30)
        self.timer += 1
    
    def square_aliens(self):
        """
        The aliens spawn in a square shape.
        """
        if self.timer == 0:
            self.env.set_ram(19, 33)
            self.env.set_ram(20, 33)
            self.env.set_ram(21, 33)
            self.env.set_ram(22, 33)
        self.timer += 1

    def frozen_aliens(self):
        """
        The aliens always stay at the same position.
        """
        self.env.set_ram(16, 0)
        self.env.set_ram(26, 40)

    def frozen_satellite(self):
        """
        The satellite always stays at the same position.
        """
        self.env.set_ram(30, 70)
        # Notice: The P1 and P2 score displays aren't visible permanantly.

    def no_shields(self):
        """
        All shields are disabled.
        """
        self.disable_shield_left()
        self.disable_shield_middle()
        self.disable_shield_right()

    def blue_background(self):
        """
        Sets background color to blue.
        """
        self.env.set_ram(71, 112)
        # Notice: For some reason the player is not possible to shoot rockets anymore,
        # if you change this ram position.

    def immortal(self):
        """
        Sets lifes always to 3. The player can't die.
        """
        self.env.set_ram(73, 3)

    def machine_gun(self):
        """
        Sets the y-coordinate of the rocket iteratively to different values, ​​so that all targets 
        in that column are hit.
        The x-coordinate of the bullet is controlled by the player.
        """
        if self.timer % 7 == 1:
            self.env.set_ram(85, 62) # first row of aliens
        if self.timer % 7 == 2:
            self.env.set_ram(85, 53) # second row of aliens
        if self.timer % 7 == 3:
            self.env.set_ram(85, 44)
        if self.timer % 7 == 4:
            self.env.set_ram(85, 35)
        if self.timer % 7 == 5:
            self.env.set_ram(85, 26)
        if self.timer % 7 == 6:
            self.env.set_ram(85, 17)
        if self.timer % 7 == 0:
            self.env.set_ram(85, 8) # satellite
        self.controlable_missile()
        self.timer += 1

    def missfire_mode(self):
        """
        Sets the enemies rackets always to the x-positions next to the player, so that
        they never hit the player.
        """
        ram = self.env.get_ram()
        player_x = ram[28]
        bullet_enemy_1_x = player_x 
        bullet_enemy_2_x = player_x + 8

        # prevent illegal positions
        if bullet_enemy_1_x <= 0:
            bullet_enemy_1_x = 0
        if bullet_enemy_2_x >= 255:
            bullet_enemy_2_x = 255

        self.env.set_ram(83, bullet_enemy_1_x)
        self.env.set_ram(84, bullet_enemy_2_x)
    
    def invisible_shield(self):
        """
        Always respawns the enemies rackets if its y-position is next to the player, 
        and set its x-position to the actual x-position of the player. The player is never hit.
        """
        ram = self.env.get_ram()
        player_x = ram[28] + 4
        if int(ram[81]) >= 85:
            self.env.set_ram(81, 59)
            self.env.set_ram(83, player_x)
        if int(ram[82]) >= 85:
            self.env.set_ram(82, 59) 
            self.env.set_ram(84, player_x)     
    

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
            "disable_shield_left": self.disable_shield_left,
            "disable_shield_middle": self.disable_shield_middle,
            "disable_shield_right": self.disable_shield_right,
            "relocate_shields_slight_left": self.relocate_shields_slight_left,
            "relocate_shields_off_by_one": self.relocate_shields_off_by_one,
            "relocate_shields_right": self.relocate_shields_right,
            # "curved_shots_weak": self.curved_shots_weak,
            # "curved_shots_medium": self.curved_shots_medium,
            # "curved_shots_strong": self.curved_shots_strong,
            "controlable_missile": self.controlable_missile,
            "less_aliens": self.less_aliens,
            "triangle_aliens": self.triangle_aliens,
            "square_aliens": self.square_aliens,
            "frozen_aliens": self.frozen_aliens,
            "frozen_satellite": self.frozen_satellite,
            "no_shields": self.no_shields,
            "blue_background": self.blue_background,
            "immortal": self.immortal,
            "machine_gun": self.machine_gun,
            "missfire_mode": self.missfire_mode,
            "invisible_shield": self.invisible_shield
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
