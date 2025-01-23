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

    def no_flying_ducks(self):
        """
        Ducks in the last row disappear instead of turning into flying ducks.
        """
        self.env.set_ram(1, 79)

    def unlimited_ammo(self):
        """
        Ammunition doesn't decrease.
        """
        self.env.set_ram(3, 40)

    def missile_speed_small_increase(self):
        """
        The projectiles fired from the players are faster (slow increase).
        """
        missile_y = self.env.get_ram()[55]
        if missile_y >= 5:
            self.env.set_ram(55, missile_y - 1)

    def missile_speed_medium_increase(self):
        """
        The projectiles fired from the players are faster (medium increase).
        """
        missile_y = self.env.get_ram()[55]
        if missile_y >= 5:
            self.env.set_ram(55, missile_y - 2)

    def missile_speed_large_increase(self):
        """
        The projectiles fired from the players are faster (fast increase).
        """
        missile_y = self.env.get_ram()[55]
        if missile_y >= 5:
            self.env.set_ram(55, missile_y - 3)

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
            "no_flying_ducks": self.no_flying_ducks,
            "unlimited_ammo": self.unlimited_ammo,
            "missile_speed_small_increase": self.missile_speed_small_increase,
            "missile_speed_medium_increase": self.missile_speed_medium_increase,
            "missile_speed_large_increase": self.missile_speed_large_increase,
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
