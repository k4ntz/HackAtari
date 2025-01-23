import random


class GameModifications:
    """
    Encapsulates game modifications for managing active modifications and applying them.
    """

    # Black (Invisible), Orange (Ruby), White (Sword), Yellow (Key), Green (Snake)
    COLORS = [0, 1, 2, 4, 6]
    LEVELS = [0, 1, 2]
    ITEM_ROOMS = [0, 5, 6, 7, 8, 10, 14, 19, 20, 23]
    INVENTORY_FULL = 249

    def __init__(self, env):
        """
        Initializes the modification handler with the given environment.

        :param env: The game environment to modify.
        """
        self.env = env
        self.active_modifications = set()
        self.nb_lives = 5
        self.dead = False
        self.poses = [(77, 235), (88, 192), (128, 192),
                      (133, 148), (33, 148), (22, 192)]

    def random_position_start(self):
        """
        Sets a random starting position for the player.
        """
        ram = self.env.get_ram()
        if ram[3] == 1:
            if ram[58] == self.nb_lives - 1 or self.dead:
                self.dead = True
            if self.dead:
                if ram[2] == 4:
                    pos = self.poses[1]
                    self.nb_lives = ram[58]
                    for i, ram_n in enumerate([42, 43]):
                        self.env.set_ram(ram_n, pos[i])
                    self.dead = False

    def set_level(self, level):
        """
        Sets the game to a specified level.
        """
        if level in self.LEVELS:
            self.env.set_ram(57, level)

    def randomize_items(self):
        """
        Randomizes which items are found in which rooms.
        """
        randomized = self.ITEM_ROOMS.copy()
        random.shuffle(randomized)

    def full_inventory(self):
        """
        Adds all items to the player's inventory.
        """
        self.env.set_ram(65, self.INVENTORY_FULL)

    def unify_item_color(self, color_index):
        """
        Sets all items to a specified color.
        """
        if color_index in range(len(self.COLORS)):
            self.env.set_ram(50, self.COLORS[color_index])

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
            "random_position_start": self.random_position_start,
            "set_level_0": lambda: self.set_level(0),
            "set_level_1": lambda: self.set_level(1),
            "set_level_2": lambda: self.set_level(2),
            "randomize_items": self.randomize_items,
            "full_inventory": self.full_inventory,
            # "unify_item_color_black": lambda: self.unify_item_color(0),
            # "unify_item_color_orange": lambda: self.unify_item_color(1),
            # "unify_item_color_white": lambda: self.unify_item_color(2),
            # "unify_item_color_yellow": lambda: self.unify_item_color(3),
            # "unify_item_color_green": lambda: self.unify_item_color(4),
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
