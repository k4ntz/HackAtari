from ocatari.ram.riverraid import riverraid_score

def overright_score(env, score):
    """
    Returns the current score for River Raid. Each digit up to the hundreds of thousands position
    has its own RAM position. However in the RAM is the digit value times 8 represented f.e.
    ram value 24 represents a three on screen.

    Args:
        ram: current RAM representation of the game

    Returns:
        score (int): current score
    """
    is_zero = True
    tenthousands = score // 10000
    if tenthousands:
        env.set_ram(79, int(8 * tenthousands))
        is_zero = False
    else:
        env.set_ram(79, 88)
    score = score - tenthousands * 10000
    thousands = score // 1000
    if thousands or not is_zero:
        env.set_ram(81, int(8 * thousands))
        is_zero = False
    else:
        env.set_ram(81, 88)
    score = score - thousands * 1000
    hundreds = score // 100
    if hundreds or not is_zero:
        env.set_ram(83, int(8 * hundreds))
        is_zero = False
    else:
        env.set_ram(83, 88)
    score = score - hundreds * 100
    tens = score // 10
    if tens or not is_zero:
        env.set_ram(85, int(8 * tens))
        is_zero = False
    else:
        env.set_ram(85, 88)
    score = score - tens * 10
    env.set_ram(87, int(8 * score))
    



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

    def no_fuel(self):
        """
        Removes the fuel deposits from the game.
        """
        ram = self.env.get_ram()
        self.env.set_ram(55, 255)
        for i in range(6):
            obj_type = ram[32 + i]
            if obj_type == 10:  # fuel deposit
                self.env.set_ram(32 + i, 0)

    def red_river(self):
        """
        Turns the river red.
        """
        self.env.set_ram(13, 0xFF)

    def GameColorChange01(self):
        """
        Turns all elements of the game to another colorset (01)
        """
        self.env.set_ram(119, 144)

    def GameColorChange02(self):
        """
        Turns all elements of the game to another colorset (02)
        """
        self.env.set_ram(119, 164)

    def GameColorChange03(self):
        """
        Turns all elements of the game to another colorset (03)
        """
        self.env.set_ram(76, 184)

    def ObjectColorChange01(self):
        """
        Turns all elements of the game to another colorset (01)
        """
        self.env.set_ram(76, 144)

    def ObjectColorChange02(self):
        """
        Turns all elements of the game to another colorset (02)
        """
        self.env.set_ram(76, 164)

    def ObjectColorChange03(self):
        """
        Turns all elements of the game to another colorset (03)
        """
        self.env.set_ram(119, 184)

    def linear_river(self):
        """
        Makes the river straight, however objects still spwan at their normal position making them unreachable in the worst case
        """
        for i in range(14, 20):
            self.env.set_ram(i, 0x05)
        for i in range(38, 44):
            self.env.set_ram(i, 35)
        for i in range(44, 50):
            self.env.set_ram(i, 0)
    
    def exploding_fuels(self):
        """
        Shooting the fuel deposits will now provides -80 points (instead of 20).
        """
        ram = self.env.get_ram()
        nsc = riverraid_score(ram)
        diff = nsc - self.score
        if diff == 80:
            nsc = max(0, nsc - 160)
            overright_score(self.env, int(nsc))
        self.score = nsc
    
    def unlimited_lives(self):
        """
        The number of lives will always stay 3.
        """
        self.env.set_ram(64, 24)
        
    
    def restricted_firing(self):
        """
        Makes the player only able to shoot in critical situation, facing a bridge 
        or in a corridor.
        """
        ram = self.env.get_ram()
        bridge_present = False
        corridor = False
        for i in range(6):
            obj_type = ram[32 + i]
            if obj_type == 8:
                bridge_present = True
                break
        for r in range(38, 43):
            if ram[r] in [56, 57, 88, 117, 144, 169] or ram[r] == 7 and ram[r-24] == 1:
                corridor = True
                break
        if not bridge_present and not corridor:
            self.env.set_ram(50, 180)
        if not ram[58]: # invisible player => game over
            self.game_active = False
        if ram[7]: # player is shooting or player is moving
            self.game_active = True
        self.score = riverraid_score(ram)
        if self.game_active:
            if ram[11] < self._last11:
                self.score += 50
                overright_score(self.env, self.score)
            self._last11 = ram[11]
            

            
        # for i in range(6):
        #     obj_type = ram[32 + i]
        #     if obj_type == 10:

    def _set_active_modifications(self, active_modifs):
        """
        Specifies which modifications are active.
        """
        self.active_modifications = set(active_modifs)

    def _fill_modif_lists(self):
        """
        Returns the modification lists (step, reset, and post-detection) with active modifications.
        """
        self.score = 0
        self.game_active = False
        self._last11 = 0
        modif_mapping = {
            "no_fuel": self.no_fuel,
            "red_river": self.red_river,
            "linear_river": self.linear_river,
            "game_color_change01": self.GameColorChange01,
            "game_color_change02": self.GameColorChange02,
            "game_color_change03": self.GameColorChange03,
            "object_color_change01": self.ObjectColorChange01,
            "object_color_change02": self.ObjectColorChange02,
            "object_color_change03": self.ObjectColorChange03,
            "exploding_fuels": self.exploding_fuels,
            "restricted_firing": self.restricted_firing,
            "unlimited_lives": self.unlimited_lives,

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
