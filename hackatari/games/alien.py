import random
from ocatari.ram.game_objects import NoObject

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
        self.egg_states = [255, 14, 255, 148, 190, 24, 255, 144, 255, 12, 255, 68, 127,
                           255, 192, 255, 164, 244, 96, 255, 36, 255, 192, 255, 136, 248]

    def last_egg(self):
        """
        Removes all eggs but one.
        """
        ram = self.env.get_ram()
        if ram[11] != 128 and ram[11] != 0:
            self.env.set_ram(11, 0)
            self.env.set_ram(9, 0)
            for i in range(3):
                s_ram = 7-(2*i)
                if ram[s_ram] == 128 or ram[s_ram] < 72:
                    self.env.set_ram(s_ram, (ram[s_ram]+8)&127)
                    break
                else:
                    self.env.set_ram(s_ram, 0)

        if ram[65] and ram[90]:
            self.last_egg_reset()

    def last_egg_reset(self):
        """
        If a level starts, all eggs are removed and only one is added to the game.
        """
        # remove all eggs
        for i in range(65, 91):
            self.env.set_ram(i, 0)
        
        # randomly pick a ram position form the eggs
        state = random.choice(range(0, 26))
        # pick a bit, bits 2-8 determine if an egg is present
        bit = random.choice(range(2,8))

        # if true then the egg would be in a wall
        if not self.egg_states[state]&(2**bit):
            # just choose egg bit until it is not in the wall
            while not self.egg_states[state]&(2**bit):
                bit = random.choice(range(2,8))

        # set egg bit at egg ramposition
        self.env.set_ram(65+state, 2**bit)

        # ram position 91 tracks amount of eggs collected, 106 eggs required to finish the level
        self.env.set_ram(91, 105)
    
    def no_enemies(self):
        """
        Removes the enemies from the maze, and freezes them in the second faze.
        """
        ram = self.env.get_ram()
        if ram[0] and ram[0] != 1:
            for i in range(6):
                self.env.set_ram(66+i, 0)
        else:
            for i in range(3):
                self.env.set_ram(42+i, 0)
                self.env.set_ram(49+i, 0)


    def aliens_0(self):
        """
        Removes all three alien enemies from the maze.
        """
        for i in range(3):
            self.env.set_ram(42+i, 0)
            self.env.set_ram(49+i, 0)

    def aliens_1(self):
        """
        Removes two alien enemies from the maze.
        """
        for i in range(2):
            self.env.set_ram(42+i, 0)
            self.env.set_ram(49+i, 0)

    def aliens_2(self):
        """
        Removes one alien enemy from the maze.
        """
        self.env.set_ram(42, 0)
        self.env.set_ram(49, 0)

    def unlimited_fuel(self):
        """
        Always keeps the flamethrowers fuel at max.
        """
        self.env.set_ram(116, 255)


    def _set_active_modifications(self, active_modifs):
        """
        Specifies which modifications are active.

        :param active_modifs: A list of active modification names.
        """
        self.active_modifications = set(active_modifs)

    def _fill_modif_lists(self):
        """
        Returns the step modification list with active modifications.

        :return: List of step modifications.
        """
        modif_mapping = {
            "last_egg": self.last_egg,
            "no_enemies": self.no_enemies,
            "aliens_0": self.aliens_0,
            "aliens_1": self.aliens_1,
            "aliens_2": self.aliens_2,
            "unlimited_fuel": self.unlimited_fuel,
        }

        step_modifs = [modif_mapping[name]
                       for name in self.active_modifications if name in modif_mapping]
        return step_modifs, [], []


def modif_funcs(env, active_modifs):
    modifications = GameModifications(env)
    modifications._set_active_modifications(active_modifs)
    return modifications._fill_modif_lists()
