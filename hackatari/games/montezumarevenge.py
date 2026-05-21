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
        self.nb_lives = 5
        self.dead = False
        self.poses = [(77, 235), (88, 192), (128, 192),
                      (133, 148), (33, 148), (22, 192)]
        # Black (Invisible), Orange (Ruby), White (Sword), Yellow (Key), Green (Snake)
        self.COLORS = [0, 1, 2, 4, 6]
        self.LEVELS = [0, 1, 2]
        self.ITEM_ROOMS = [0, 5, 6, 7, 8, 10, 14, 19, 20, 23]
        self.ITEMS = [          [1, 0], None, None,
                    None, None, [6, 0], [2, 0], [4, 0],
                [4, 0], None, [1, 0], None, None, None, [4, 0],
            None, None, None, None, [4, 0], [1, 4], None, None, [1, 3]]
        self.INVENTORY_FULL = 249

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

        new_items = self.ITEMS.copy()
        for j, i in enumerate(self.ITEM_ROOMS):
            new_items[i] = self.ITEMS[randomized[j]]
        self.ITEMS = new_items
    
    def change_items(self):
        """
        Applies item changes, if items are randomized.
        """
        ram = self.env.get_ram()
        if ram[3] != 1 and ram[49] != 0 and self.ITEMS[ram[3]] is not None:
            item_type = self.ITEMS[ram[3]][0]
            if item_type < 3:
                color = item_type
            else:
                color = 4
            self.env.set_ram(49, self.ITEMS[ram[3]][0])
            self.env.set_ram(50, color)
            self.env.set_ram(84, self.ITEMS[ram[3]][1])

    def full_inventory(self):
        """
        Adds all items to the player's inventory.
        """
        self.env.set_ram(65, self.INVENTORY_FULL)

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
            "step_modifs": {
                "randomize_items": self.change_items,
            },
            "reset_modifs": {
                "set_level_0": lambda: self.set_level(0),
                "set_level_1": lambda: self.set_level(1),
                "set_level_2": lambda: self.set_level(2),
                "random_position_start": self.random_position_start,
                "randomize_items": self.randomize_items,
                "full_inventory": self.full_inventory,
            },
            "post_detection_modifs": {
            },
            "inpainting_modifs": {
            },
            "place_above_modifs": {
            }
        }

        step_modifs = [modif_mapping["step_modifs"][name]
                       for name in self.active_modifications if name in modif_mapping["step_modifs"]]
        reset_modifs = [modif_mapping["reset_modifs"][name]
                       for name in self.active_modifications if name in modif_mapping["reset_modifs"]]
        post_detection_modifs = [modif_mapping["post_detection_modifs"][name]
                       for name in self.active_modifications if name in modif_mapping["post_detection_modifs"]]
        inpainting_modifs = [modif_mapping["inpainting_modifs"][name]
                       for name in self.active_modifications if name in modif_mapping["inpainting_modifs"]]
        place_above_modifs = [modif_mapping["place_above_modifs"][name]
                       for name in self.active_modifications if name in modif_mapping["place_above_modifs"]]
        
        return step_modifs, reset_modifs, post_detection_modifs, inpainting_modifs, place_above_modifs


def modif_funcs(env, active_modifs):
    modifications = GameModifications(env)
    modifications._set_active_modifications(active_modifs)
    return modifications._fill_modif_lists()
