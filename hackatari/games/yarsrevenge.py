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

    def _set_active_modifications(self, active_modifs):
        """
        Specifies which modifications are active.

        :param active_modifs: A list of active modification names.
        """
        self.active_modifications = set(active_modifs)

    def static_enemy_position(self):
        """
        Makes the enemy and the blocks unable to move up and down.
        """
        self.set_ram(42, 90)
        self.set_ram(26, 37)


    def disable_enemy_movement(self):
        """
        Completely disables enemy movement.
        """
        self.set_ram(40, 0)
        self.set_ram(41, 0)


    def disable_block_movement(self):
        """
        Completely disables block movement.
        """
        self.set_ram(24, 0)
        self.set_ram(25, 0)


    def _fill_modif_lists(self):
        """
        Returns the modification lists (step, reset, and post-detection) with active modifications.

        :return: Tuple of step_modifs, reset_modifs, and post_detection_modifs.
        """
        modif_mapping = {
        "static": self.static_enemy_position,
        "disable_enemy_movement": self.disable_enemy_movement,
        "disable_block_movement": self.disable_block_movement,
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
