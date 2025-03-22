import random


# Warning: Doesn't work right now.


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

    def teleport(self):
        """
        ball is teleported randomly at some certain places
        """
        # 67 and 68 can be between [0-255]
        # 67 is how far is the ball from left
        # 68 is how far is the ball from top

        ram = self.env.get_ram()

        # "if 10 < ram[67] < 145:" to prevent teleportations at the left/right tubes
        # randomly teleports the ball to one of these locations
        if 10 < ram[67] < 145:
            if random.random() < 0.001:
                p = random.random()

                if p < 1/7:
                    self.env.set_ram(67, 140)
                    self.env.set_ram(68, 35)
                elif p < 2/7:
                    self.env.set_ram(67, 15)
                    self.env.set_ram(68, 40)
                elif p < 3/7:
                    self.env.set_ram(67, 95)
                    self.env.set_ram(68, 60)
                elif p < 4/7:
                    self.env.set_ram(67, 20)
                    self.env.set_ram(68, 95)
                elif p < 5/7:
                    self.env.set_ram(67, 90)
                    self.env.set_ram(68, 120)
                elif p < 6/7:
                    self.env.set_ram(67, 65)
                    self.env.set_ram(68, 165)
                else:
                    self.env.set_ram(67, 130)
                    self.env.set_ram(68, 160)

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
            "teleport": self.teleport,
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