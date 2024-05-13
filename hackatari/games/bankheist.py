import random 

TOWNS_VISITED = []
REMAINING_TOWNS = [i for i in range(256)]
random.shuffle(REMAINING_TOWNS)
CURRENT_TOWN = 0
PLAYER_X = 0


def unlimited_gas(self):
    """
    Unlimited gas all the enemies.
    """
    self.set_ram(86, 0)


def no_police(self):
    """
    Removes police from the game.
    """
    ram = self.get_ram()
    for i in range(3):
        if ram[24+i] == 254:
            self.set_ram(24+i, 0)


def only_police(self):
    """
    No banks only police.
    """
    ram = self.get_ram()
    for i in range(3):
        if ram[24+i] == 253:
            self.set_ram(24+i, 254)


def random_city(self):
    """
    Randomizes which city is entered next.
    """
    global TOWNS_VISITED, REMAINING_TOWNS, CURRENT_TOWN
    ram = self.get_ram()
    city = ram[0]
    if city == CURRENT_TOWN + 1: # arrived to new city
        picked_city = REMAINING_TOWNS.pop(0)
        CURRENT_TOWN = picked_city
        if len(REMAINING_TOWNS) == 0: # reset
            REMAINING_TOWNS = [i for i in range(256)]
            random.shuffle(REMAINING_TOWNS)
        TOWNS_VISITED.append(picked_city)
        self.set_ram(0, picked_city)
    
    
def random_city_res(self):
    """
    Resets the city randomizer.
    """
    global TOWNS_VISITED, REMAINING_TOWNS, CURRENT_TOWN
    ram = self.get_ram()
    REMAINING_TOWNS = [i for i in range(256)]
    random.shuffle(REMAINING_TOWNS)
    picked_city = REMAINING_TOWNS.pop(0)
    CURRENT_TOWN = picked_city
    TOWNS_VISITED.append(picked_city)
    self.set_ram(0, picked_city)
    

def revisit_city(self):
    """
    Allows player to go back one city.
    """
    global PLAYER_X, CURRENT_TOWN
    ram = self.get_ram()
    if 16 > PLAYER_X and ram[28] > 120:
        PLAYER_X = 0
        if CURRENT_TOWN == 0:
            CURRENT_TOWN = 255
        else:
            CURRENT_TOWN = CURRENT_TOWN - 1
        self.set_ram(0, CURRENT_TOWN)
    else:
        CURRENT_TOWN = ram[0]
    PLAYER_X = ram[28]


def _modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        if mod == "unlimited_gas":
            step_modifs.append(unlimited_gas)
        elif mod == "no_police":
            step_modifs.append(no_police)
        elif mod == "only_police":
            step_modifs.append(only_police)
        elif mod == "random_city":
            step_modifs.append(random_city)
            reset_modifs.append(random_city_res)
        elif mod == "revisit_city":
            step_modifs.append(revisit_city)
    return step_modifs, reset_modifs