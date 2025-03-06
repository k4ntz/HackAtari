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

    def static_ghosts(self):
        """
        Keeps ghosts fixed inside the square in the middle of the screen.
        """
        if self.toggle_orange:
            self.env.set_ram(6, 93) # ram pos 6: orange ghost x-coordinate
            self.env.set_ram(12, 80) # ram pos 12: orange ghost y-coordinate
        if self.toggle_cyan:
            self.env.set_ram(7, 83)
            self.env.set_ram(13, 80)
        if self.toggle_pink:
            self.env.set_ram(8, 93)
            self.env.set_ram(14, 67)
        if self.toggle_red:
            self.env.set_ram(9, 83)
            self.env.set_ram(15, 67)

    def edible_ghosts(self):    # doesnt work
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

    def end_game(self):
        """
        Simulates an endgame state by spawning only a small cluster of pills.
        """
        for i in range(59, 101):
            if i == self.end_game_pills:
                continue
            self.env.set_ram(i, 0)
        self.env.set_ram(117, 0)


#### My modifications        

    pos_ghost_orange = [93, 80]
    pos_ghost_cyan = [83, 80]
    pos_ghost_pink = [89, 67]
    pos_ghost_red = [83, 67]
    def slow_ghosts(self):
        """
        The ghosts go one step back every 3 timesteps.
        """
        ram = self.env.get_ram()
        if (self.timer % 3) == 0: # every 3 timesteps
            # orange
            self.env.set_ram(6, self.pos_ghost_orange[0]) 
            self.env.set_ram(12, self.pos_ghost_orange[1]) 
            # cyan
            self.env.set_ram(7, self.pos_ghost_cyan[0]) 
            self.env.set_ram(13, self.pos_ghost_cyan[1])
            # pink
            self.env.set_ram(8, self.pos_ghost_pink[0]) 
            self.env.set_ram(14, self.pos_ghost_pink[1])
            # red
            self.env.set_ram(9, self.pos_ghost_red[0]) 
            self.env.set_ram(15, self.pos_ghost_red[1])
        else:
            # update ghost positions
            self.pos_ghost_orange = [ram[6], ram[12]]
            self.pos_ghost_cyan = [ram[7], ram[13]]
            self.pos_ghost_pink = [ram[8], ram[14]]
            self.pos_ghost_red = [ram[9], ram[15]]
        self.timer += 1

    def ghost_reset(self):
        """
        The ghosts jump back to their start position every 200 timesteps.
        """
        if (self.timer % 200) == 0: # every 200 timesteps
            # orange
            self.env.set_ram(6, 93) 
            self.env.set_ram(12, 80)
            # cyan
            self.env.set_ram(7, 83)
            self.env.set_ram(13, 80)
            # pink
            self.env.set_ram(8, 93)
            self.env.set_ram(14, 67)
            # red
            self.env.set_ram(9, 83)
            self.env.set_ram(15, 67)
        self.timer += 1

    def fruit_pretzel(self):
        """
        Spawns a pretzel as fruit.
        """
        if self.timer == 1:
            self.env.set_ram(123, 62) # ram position 123: Affects which kind of fruit appears.
        # Note: For some reason the number at position 123 also indicates the number of lifes (how often the player may restart).
        # The ram position 123 modulo 4 indicates the number of shown restarts symbols (0, 1, 2 or 3). 
        # -> Problem: If you died 2 times, the ram position 123 is 60, and you should lose the game if you die again.
        # But, if you die again, the ram position 123 will be 59 and you are shown 3 lifes. 
        self.timer += 1

    def fruit_orange(self): 
        """
        Spawns an orange as fruit.
        """
        self.env.set_ram(123, 46)

    def fruit_banana(self): 
        """
        Spawns a banana as fruit.
        """
        self.env.set_ram(123, 110)

    def fruit_strawberry(self): 
        """
        Spawns a strawberry as fruit.
        """
        self.env.set_ram(123, 26)
    
    def fruit_apple(self): 
        """
        Spawns an apple as fruit.
        """
        self.env.set_ram(123, 70)

    def fruit_pear(self): 
        """
        Spawns a pear as fruit.
        """
        self.env.set_ram(123, 90)

    def immortality(self):
        """
        Player has infinitely many lifes.
        """
        self.env.set_ram(123, 3)

    def fruit_display_glitch(self):
        """
        3 smiley symbols appear at the fruit display.
        """
        self.env.set_ram(19, 2) 

    def set_level_3(self):
        """
        Sets the game level to 3.
        """
        self.env.set_ram(0, 3) # Ram position 0: indicates the Level (the map)

    def player_respawn(self):
        """
        The player jumps to start point every 300 timesteps.
        """
        if (self.timer % 300) == 0: # Every 300 timesteps
            self.env.set_ram(10, 88) # Ram position 10: indicates the x-coordinate of the player
            self.env.set_ram(16, 98)  # Ram position 10: indicates the y-coordinate of the player
        self.timer += 1

    pos_ghost_snake = [[88, 50] for _ in range(61)]
    def ghost_snake(self):
        """
        The orange, cyan and pink ghost follow the red ghost in a line.
        """
        ram = self.env.get_ram()
        self.pos_ghost_snake = [[ram[9],ram[15]]] + self.pos_ghost_snake
        self.pos_ghost_snake = self.pos_ghost_snake[:61]
        # orange
        self.env.set_ram(6, self.pos_ghost_snake[20][0]) 
        self.env.set_ram(12, self.pos_ghost_snake[20][1])
        # cyan
        self.env.set_ram(7, self.pos_ghost_snake[40][0])
        self.env.set_ram(13, self.pos_ghost_snake[40][1])
        # pink
        self.env.set_ram(8, self.pos_ghost_snake[60][0])
        self.env.set_ram(14, self.pos_ghost_snake[60][1])

    def player_shield(self):
        """
        The player can't be catched by ghosts. If any ghost is next to the player it respawns at the start point.
        """
        ram = self.env.get_ram()
        pos_player = [ram[10], ram[16]]
        pos_orange_ghost = [ram[6], ram[12]]
        pos_cyan_ghost = [ram[7], ram[13]]
        pos_pink_ghost = [ram[8], ram[14]]
        pos_red_ghost = [ram[9], ram[15]]
        if self.manhattan_dist(pos_player, pos_red_ghost) <= 6: # If the red ghost is 6 steps next to the player respawn the ghost.
            self.env.set_ram(9, 83)
            self.env.set_ram(15, 67)
        if self.manhattan_dist(pos_player, pos_orange_ghost) <= 6:  # orange
            self.env.set_ram(6, 93)
            self.env.set_ram(12, 80)
        if self.manhattan_dist(pos_player, pos_cyan_ghost) <= 6:  # cyan
            self.env.set_ram(7, 83)
            self.env.set_ram(13, 80)
        if self.manhattan_dist(pos_player, pos_pink_ghost) <= 6:  # pink
            self.env.set_ram(8, 89)
            self.env.set_ram(14, 67)

    def manhattan_dist(self, a, b):
        """
        Param:
        a ([int, int]): Coordinates of the point a.
        b ([int, int]): Coordinates of the point b.
        Return:
        int: The L1-distance (manhattan distance) between a and b.
        """
        return abs(int(a[0])-int(b[0])) + abs(int(a[1])-int(b[1]))
        

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
            elif mod == "end_game":
                self.end_game_pills = random.randint(59, 101)
                self.active_modifications.add("end_game")
            elif mod == "slow_ghosts":
                self.active_modifications.add("slow_ghosts")
            elif mod == "ghost_reset":
                self.active_modifications.add("ghost_reset")
            elif mod == "fruit_pretzel":
                self.active_modifications.add("fruit_pretzel")
            elif mod == "fruit_orange":
                self.active_modifications.add("fruit_orange")
            elif mod == "fruit_banana":
                self.active_modifications.add("fruit_banana")
            elif mod == "fruit_strawberry":
                self.active_modifications.add("fruit_strawberry")
            elif mod == "fruit_apple":
                self.active_modifications.add("fruit_apple")
            elif mod == "fruit_pear":
                self.active_modifications.add("fruit_pear")
            elif mod == "immortality":
                self.active_modifications.add("immortality")
            elif mod == "fruit_display_glitch":
                self.active_modifications.add("fruit_display_glitch")
            elif mod == "set_level_3":
                self.active_modifications.add("set_level_3")
            elif mod == "player_respawn":
                self.active_modifications.add("player_respawn")
            elif mod == "ghost_snake":
                self.active_modifications.add("ghost_snake")
            elif mod == "player_shield":
                self.active_modifications.add("player_shield")

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
            "end_game": self.end_game,
            "slow_ghosts": self.slow_ghosts,
            "ghost_reset": self.ghost_reset,
            "fruit_pretzel": self.fruit_pretzel,
            "fruit_orange": self.fruit_orange,
            "fruit_banana": self.fruit_banana,
            "fruit_strawberry": self.fruit_strawberry,
            "fruit_apple": self.fruit_apple,
            "fruit_pear": self.fruit_pear,
            "immortality": self.immortality,
            "fruit_display_glitch": self.fruit_display_glitch,
            "set_level_3": self.set_level_3,
            "player_respawn": self.player_respawn,
            "ghost_snake": self.ghost_snake,
            "player_shield": self.player_shield
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
