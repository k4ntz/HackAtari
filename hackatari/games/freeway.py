import random 


color_map = {
    1: 0,
    2: 2,
    3: 66,
    4: 15,
    5: 210,
    6: 120,
    7: 145,
    8: 6
}

CARS_COLOR = 0

def modify_ram_for_color(self):
    '''
    Modifies RAM for each car with the specified color.
    '''
    for car in range(77, 87):
        self.set_ram(car, CARS_COLOR)


def modify_ram_for_default(self):
    '''
    Modifies RAM with default color values for specific cars.
    '''
    default_colors = [26, 216, 68, 136, 36, 130, 74, 18, 220, 66, 189]
    for index, value in enumerate(default_colors, start=77):
        self.set_ram(index, value)


def set_ram_value(self, address, value):
    '''
    Sets the value in RAM at a specific address.
    '''
    ram = self.get_ram()
    ram[address] = value
    self.set_ram(address, ram[address])


def custom_biased_random(option_a, option_b, probability_a):
    '''
    This function generates a random selection between two options (a and b) with a user-defined
    probability for option a.
    '''
    choices = [option_a, option_b]
    weights = [probability_a, 1 - probability_a]
    result = random.choices(choices, weights=weights, k=1)[0]
    return result


def handle_car_stop_mode_1(self):
    '''
    Handles random car stop mode 1.
    '''
    # Get a random counter value and a random car position
    counter = custom_biased_random(0, 3, 0.9)
    random_car = random.randint(33, 42)
    # Set RAM value to 100 if counter is greater than 0, else set to 0
    if counter > 0:
        set_ram_value(self, random_car, 100)
    else:
        set_ram_value(self, random_car, 0)


def handle_car_stop_mode_2(self):
    '''
    Handles random car stop mode 2.
    '''
    # Get a random value for all cars and modify RAM accordingly
    car_all = custom_biased_random(0, 1, 0.4)
    for car_pos in range(33, 43):
        if car_all > 0:
            set_ram_value(self, car_pos, 100)
        else:
            set_ram_value(self, car_pos, 0)


def handle_car_stop_mode_3(self):
    '''
    Handles random car stop mode 3.
    '''
    # Ram value 100 stops all cars. Ram Value 15 is the position of the
    # bottom 5 cars and 150 is the position of the top 5 cars.
    for car_stop in range(33, 43):
        self.set_ram(car_stop, 100)
    for new_pos_down in range(108, 113):
        set_ram_value(self, new_pos_down, 15)
    for new_pos_down in range(113, 118):
        set_ram_value(self, new_pos_down, 150)


def _modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        mod_n = int(mod[-1])
        if mod.startswith('s'):
            if mod_n == 1:
                step_modifs.append(handle_car_stop_mode_1)
            elif mod_n == 2:
                step_modifs.append(handle_car_stop_mode_2)
            elif mod_n == 3:
                step_modifs.append(handle_car_stop_mode_3)
            else:
                raise ValueError("Invalid modification number")
        elif mod.startswith('c'):
            global CARS_COLOR
            CARS_COLOR = color_map.get(mod_n, 256)
            step_modifs.append(modify_ram_for_color)
    return step_modifs, reset_modifs