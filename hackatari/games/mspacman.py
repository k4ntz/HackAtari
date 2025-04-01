import random


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
        self.number_power_pills = 4
        self.lvl_num = 0
        self.lives = 2
        self.timer = 1
        self.toggle_cyan = False
        self.toggle_pink = False
        self.toggle_orange = False
        self.toggle_red = False
        self.col = None
        self.line = None
        self.end_game_pills = 0
        self.dot_states = [59, 60, 61, 62, 65, 66, 67, 71, 72, 73, 83, 89, 90, 91, 92, 95, 98, 99, 100]
        self.dot_pattern = [(59, 64), (60, 128), (60, 32), (60, 8), (60, 2), (61, 1), (61, 4), (61, 16), (61, 64),
                            (60, 64), (60, 16), (60, 4), (60, 1), (61, 2), (61, 8), (61, 32), (61, 128), (59, 16)]
        self.grid1 = [
                        [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
                        [1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                        [0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0],
                        [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
                        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
                        [0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
                        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0],
                        [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1],
                        [0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0],
                        [1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
                        [1, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1],
                        [1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    ]
        
        self.timer = 1

    def static_ghosts(self):
        """
        Keeps ghosts fixed inside the square in the middle of the screen.
        """
        if self.toggle_orange:
            self.env.set_ram(6, 93)
            self.env.set_ram(12, 80)
        if self.toggle_cyan:
            self.env.set_ram(7, 83)
            self.env.set_ram(13, 80)
        if self.toggle_pink:
            self.env.set_ram(8, 93)
            self.env.set_ram(14, 67)
        if self.toggle_red:
            self.env.set_ram(9, 83)
            self.env.set_ram(15, 67)

    def edible_ghosts(self):
        """
        Ensures all ghosts remain edible indefinitely.
        """
        for i in range(1, 5):
            self.env.set_ram(i, 130)
        self.env.set_ram(116, 255)

    def set_level_0(self):
        """
        Sets the game level to 0.
        """
        self.env.set_ram(0, 0)

    def set_level_1(self):
        """
        Sets the game level to 1.
        """
        self.env.set_ram(0, 1)

    def set_level_2(self):
        """
        Sets the game level to 2.
        """
        self.env.set_ram(0, 2)

    def set_level_3(self):
        """
        Sets the game level to 2.
        """
        self.env.set_ram(0, 3)

    def end_game(self):
        """
        Simulates an endgame state by spawning only a small cluster of pills.
        """

        for i in range(59, 101):
            self.env.set_ram(i, 0)
        self.env.set_ram(117, 0)
        self.env.set_ram(119, 139)
        line = random.choice(range(0, 14))
        dot = random.choice(range(0, 18))
        if not self.grid1[line][dot]:
            while not self.grid1[line][dot]:
                dot = random.choice(range(0, 18))

        dots = [(line, dot)]
        i = 0

        while len(dots) < 15:
            for move in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                pos1 = dots[i][0] + move[0]
                pos2 = dots[i][1] + move[1]
                if (
                    (0 <= pos1 < 14 and 0 <= pos2 < 18)
                    and self.grid1[pos1][pos2]
                    and ((pos1, pos2) not in dots)
                ):
                    dots.append((pos1, pos2))
            i += 1

        for d in range(15):
            ram = self.env.get_ram()
            pill = self.dot_pattern[dots[d][1]][0] + 3 * dots[d][0]
            value = ram[pill] + self.dot_pattern[dots[d][1]][1]
            self.env.set_ram(pill, value)


    def check_reset(self):
        ram = self.env.get_ram()
        if ram[60]&2:
            self.env.set_ram(0, 0)
            self.end_game()


    def maze_man(self):
        """
        Changes the gameplay. Ghosts are removed and all but one pill have been removed.
        Points now represent a timer.
        The goal of the game is to collect the pill in the maze before the time limit runs out.
        After a pill has been collected, time will be added and a new pill will spawn.
        If the player collects 20 pills, the game goes into the next level.
        """
        ram = self.env.get_ram()
        if ram[60]&2:
            self.maze_man_reset()

        # makes red ghost invisible (is glitchy)
        self.env.set_ram(47, 0)

        # check if pill was collected
        collected = True

        # checks the pill states, set collected to false if there is one remaining on the map
        for i in range(59, 101):
            if ram[i] != 0:
                collected = False

        # if no pill on the map
        if collected and ram[39] > 70:
            # increase the timer (inplace of score)
            add = ram[120] + 32
            if add <= 144:
                self.env.set_ram(120, add)
            else:
                self.env.set_ram(120, 144)

            # better choice alogorithm from endgame
            line = random.choice(range(0, 14))
            dot = random.choice(range(0, 18))
            if not self.grid1[line][dot]:
                while not self.grid1[line][dot]:
                    dot = random.choice(range(0, 18))
            pill = self.dot_pattern[dot][0] + 3*line
            value = ram[pill] + self.dot_pattern[dot][1]
            self.env.set_ram(pill, value)

        # change or reset level on success/failure
        if ram[39] == 69 and ram[119] == 154:
            lives = ram[123]
            if lives < 3:
                self.env.set_ram(123, lives+1)
            self.maze_man_reset()

        # Use ram state and TIMER variable as tick
        if ram[39] == 255 and self.timer == 0:
            lives = ram[123]
            # resets the whole game if no lives remaining
            if ram[120] < 16 and lives <= 0:
                self.maze_man_reset()
            # decrease lives if
            elif ram[120] < 16:
                self.env.set_ram(123, lives-1)
                self.maze_man_reset()
            else:
                self.env.set_ram(120, ram[120]-16)

        # increase timer
        self.timer = (self.timer + 1) % 150


    def maze_man_reset(self):
        for i in range(59, 101):
            self.env.set_ram(i, 0)
        self.timer = 1
        # mini man stuff
        # if LINE is not None:
        #     global COL, COL_POS, LINE_POS
        #     self.env.set_ram(10, COL_POS[COL])
        #     self.env.set_ram(16, LINE_POS[LINE])
        self.env.set_ram(0, 0)
        self.env.set_ram(19, 0)
        self.env.set_ram(117, 0)
        self.env.set_ram(119, 134)
        self.env.set_ram(120, 144)

    def _set_active_modifications(self, active_modifs):
        """
        Specifies which modifications are active.
        """
        for mod in active_modifs:
            if mod == "caged_ghosts":
                self.toggle_cyan = self.toggle_orange = self.toggle_red = self.toggle_pink = True
                self.active_modifications.add("static_ghosts")
            elif mod == "disable_orange":
                self.toggle_orange = True
                self.active_modifications.add("static_ghosts")
            elif mod == "disable_red":
                self.toggle_red = True
                self.active_modifications.add("static_ghosts")
            elif mod == "disable_cyan":
                self.toggle_cyan = True
                self.active_modifications.add("static_ghosts")
            elif mod == "disable_pink":
                self.toggle_pink = True
                self.active_modifications.add("static_ghosts")
            elif mod == "edible_ghosts":
                self.active_modifications.add("edible_ghosts")
            elif mod == "set_level_0":
                self.active_modifications.add("set_level_0")
            elif mod == "set_level_1":
                self.active_modifications.add("set_level_1")
            elif mod == "set_level_2":
                self.active_modifications.add("set_level_2")
            elif mod == "set_level_3":
                self.active_modifications.add("set_level_3")
            elif mod == "end_game":
                self.active_modifications.add("end_game")
            elif mod == "maze_man":
                self.toggle_cyan = self.toggle_orange = self.toggle_red = self.toggle_pink = True
                self.active_modifications.add("static_ghosts")
                self.active_modifications.add("maze_man")

    def _fill_modif_lists(self):
        """
        Returns the modification lists (step, reset, and post-detection) with active modifications.
        """
        modif_mapping = {
            "static_ghosts": self.static_ghosts,
            # "edible_ghosts": self.edible_ghosts,
            "set_level_0": self.set_level_0,
            "set_level_1": self.set_level_1,
            "set_level_2": self.set_level_2,
            "set_level_3": self.set_level_3,
            "end_game": self.check_reset,
            "maze_man": self.maze_man,
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
