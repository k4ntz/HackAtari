import random
import numpy as np


class GameModifications:
    """
    Encapsulates game modifications for managing active modifications and applying them.
    """

    COLORS = [0, 48, 113, 200]  # Black, Red, Blue, Green

    def __init__(self, env):
        """
        Initializes the modification handler with the given environment.

        :param env: The game environment to modify.
        """
        self.env = env
        self.active_modifications = set()
        self.level_num = None
        self.already_reset = False

    def disable_monkeys(self):
        """
        Disables the monkeys in the game.
        """
        for x in range(4):
            self.env.set_ram(11 - x, 127)

    def disable_coconut(self):
        """
        Disables the falling coconut in the game.
        """
        self.env.set_ram(33, 255)
        self.env.set_ram(35, 255)

    def disable_thrown_coconut(self):
        """
        Disables the thrown coconut in the game.
        """
        self.env.set_ram(25, 255)
        self.env.set_ram(28, 255)
        self.env.set_ram(31, 0)

    def unlimited_time(self):
        """
        Sets the time to unlimited.
        """
        self.env.set_ram(59, 32)

    def set_kangaroo_position_floor1(self):
        """
        Sets the kangaroo's position for floor 1.
        """
        self._set_kangaroo_position(65, 12)

    def set_kangaroo_position_floor2(self):
        """
        Sets the kangaroo's position for floor 2.
        """
        self._set_kangaroo_position(100, 6)

    def randomize_kangaroo_position(self):
        """
        Randomizes the floor on which the player starts.
        """
        random_number = random.randint(0, 1)
        if random_number == 0:
            self.set_kangaroo_position_floor1()
        else:
            self.set_kangaroo_position_floor2()

    def change_level_0(self):
        """
        Changes the level to 0.
        """
        self.env.set_ram(36, 0)

    def change_level_1(self):
        """
        Changes the level to 1.
        """
        self.env.set_ram(36, 1)

    def change_level_2(self):
        """
        Changes the level to 2.
        """
        self.env.set_ram(36, 2)
    
    def no_danger(self):
        """
        Disables all dangers in the game.
        """
        self.disable_coconut()
        self.disable_thrown_coconut()
        self.disable_monkeys()
    
    def quick_start(self):
        """
        Skips the waiting time at the start of a game.
        """
        self.env.set_ram(19, 0)
        self.env.set_ram(53, 8)
        self.env.set_ram(54, 0)
        self.env.set_ram(57, 1)
    
    # def no_flickering(self):
    #     """
    #     Inserts the missing sprites into the game fram, when the Player is on the same level as a fruit or the child.
    #     """
    #     ram = self.env.get_ram()
    #     patches = []
    #     # Level 1: Fruit_1 13, 21; Fruit_2 10, 15; Fruit_3 7, 12; Bell 0, 9
    #     # Level 2: Fruit_1 17, 21; Fruit_2 11, 16; Fruit_3 8, 13; Bell 0, 9
    #     # Level 3: Fruit_1 14, 21; Fruit_2 11, 16; Fruit_3 7, 12; Bell 0, 9
    #     if ram[108] == 134:
    #         if ram[87] == ram[86]:
    #             y = ram[84:87]
    #         else:
    #             y = ram[85:88]
            
    #         if ram[114] < 10:
    #             switch_state = ram[112]
    #         elif ram[114] < 13 + (1 if ram[36] == 1 else 0):
    #             switch_state = ram[111]
    #         elif ram[114] < 16 + (1 if ram[36] else 0):
    #             switch_state = ram[110]
    #         else:
    #             switch_state = ram[109]

    #         if switch_state == 44:
    #             print("Kangaroo")
    #         else:
    #             for i in range(3):
    #                 if 0 <= ram[114] - y[i] < 6 and not ram[42+i]&128:
    #                     print("Fruit_" + str(3-i))
    #             if ram[114] < 10:
    #                 print("Bell")

    #     return patches

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
                "disable_monkeys": self.disable_monkeys,
                "disable_coconut": self.disable_coconut,
                "disable_thrown_coconut": self.disable_thrown_coconut,
                "unlimited_time": self.unlimited_time,
                "set_kangaroo_position_floor1": self.set_kangaroo_position_floor1,
                "set_kangaroo_position_floor2": self.set_kangaroo_position_floor2,
                "randomize_kangaroo_position": self.randomize_kangaroo_position,
                "change_level_0": self.change_level_0,
                "change_level_1": self.change_level_1,
                "change_level_2": self.change_level_2,
                "no_danger": self.no_danger,
            },
            "reset_modifs": {
                "quick_start": self.quick_start,
            },
            "post_detection_modifs": {
            },
            "inpainting_modifs": {
                # "no_flickering": self.no_flickering,
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

    def _set_kangaroo_position(self, pos_x, pos_y):
        """
        Sets the kangaroo's position.

        :param pos_x: X-coordinate of the kangaroo.
        :param pos_y: Y-coordinate of the kangaroo.
        """
        if not self.already_reset:
            self.env.set_ram(17, pos_x)
            self.env.set_ram(16, pos_y)
            self.env.set_ram(33, 255)
            self.already_reset = True


def modif_funcs(env, active_modifs):
    modifications = GameModifications(env)
    modifications._set_active_modifications(active_modifs)
    return modifications._fill_modif_lists()
