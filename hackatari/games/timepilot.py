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

    def _set_active_modifications(self, active_modifs):
        """
        Specifies which modifications are active.

        :param active_modifs: A list of active modification names.
        """
        self.active_modifications = set(active_modifs)

    def level_1(self):
        """
        Start at level 1
        """
        self.env.set_ram(21, 0)

    def level_2(self):
        """
        Start at level 2
        """
        self.env.set_ram(21, 1)

    def level_3(self):
        """
        Start at level 3
        """
        self.env.set_ram(21, 2)

    def level_4(self):
        """
        Start at level 4
        """
        self.env.set_ram(21, 3)

    def level_5(self):
        """
        Start at level 5
        """
        self.env.set_ram(21, 4)
    
    def enemies_0(self):
        for i in range(4):
            self.env.set_ram(37+i, 0)
    
    def enemies_1(self):
        for i in range(3):
            self.env.set_ram(38+i, 0)
    
    def enemies_2(self):
        for i in range(2):
            self.env.set_ram(39+i, 0)
    
    def enemies_3(self):
        self.env.set_ram(40, 0)
    
    def random_orientation(self):
        """
        Randomizes orientation of enemies. They are no longer aligned.
        """
        ram = self.env.get_ram()
        if ram[45] == ram[46]:
            for i in range(4):
                orientation = random.randint(0, 7)
                self.env.set_ram(45+i, orientation)

    def _fill_modif_lists(self):
        """
        Returns the modification lists (step, reset, and post-detection) with active modifications.

        :return: Tuple of step_modifs, reset_modifs, and post_detection_modifs.
        """
        modif_mapping = {
            "step_modifs":{
                "enemies_0": self.enemies_0,
                "enemies_1": self.enemies_1,
                "enemies_2": self.enemies_2,
                "enemies_3": self.enemies_3,
                "random_orientation": self.random_orientation,
            },
            "reset_modifs": {
                "level_1": self.level_1,
                "level_2": self.level_2,
                "level_3": self.level_3,
                "level_4": self.level_4,
                "level_5": self.level_5,
            },
        }
        
        step_modifs = [modif_mapping["step_modifs"][name]
                       for name in self.active_modifications if name in modif_mapping["step_modifs"]]
        reset_modifs = [modif_mapping["reset_modifs"][name]
                       for name in self.active_modifications if name in modif_mapping["reset_modifs"]]
        post_detection_modifs = []
        return step_modifs, reset_modifs, post_detection_modifs


def modif_funcs(env, active_modifs):
    modifications = GameModifications(env)
    modifications._set_active_modifications(active_modifs)
    return modifications._fill_modif_lists()
