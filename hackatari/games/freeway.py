import random


class GameModifications:
    """
    Encapsulates game modifications to ensure thread safety and avoid global variables.
    """

    _color_map = {1: 0, 2: 2, 3: 66, 4: 15, 5: 210, 6: 120, 7: 145, 8: 6}

    def __init__(self, env):
        """
        Initializes the modification handler with the given environment.

        :param env: The game environment to modify.
        """
        self.env = env
        self.active_modifications = set()

    def stop_random_car(self):
        """
        Stops a random car with a biased probability.
        """
        counter = random.choices([0, 1, 2, 3], weights=[
                                 0.1, 0.3, 0.3, 0.3], k=1)[0]
        random_car = random.randint(33, 42)
        self.env.set_ram(random_car, 8 if counter > 0 else 0)

    def align_all_cars(self):
        """
        Stops all cars based on a biased random decision.
        """
        car_all = random.choices([0, 1], weights=[0.6, 0.4], k=1)[0]
        for car_pos in range(33, 43):
            self.env.set_ram(car_pos, 100 if car_all > 0 else 0)

    def reverse_car_speed_bottom(self):
        """
        Reverses the speed of the bottom car (the fastest becomes the slowest and vice versa).
        """
        for i in range(5):
            val = self.env.get_ram()[1] % (i+1)
            self.env.set_ram(33+i, val)

    def reverse_car_speed_top(self):
        """
        Reverses the speed of the top car (the fastest becomes the slowest and vice versa).
        """
        for i in range(5):
            val = self.env.get_ram()[1] % (i+1)
            self.env.set_ram(42-i, val)

    def stop_all_cars(self):
        """
        Stops all cars and repositions some to predefined positions.
        """
        for car_stop in range(33, 43):
            self.env.set_ram(car_stop, 100)
        for new_pos_down in range(108, 113):
            self.env.set_ram(new_pos_down, 35)
        for new_pos_down in range(113, 118):
            self.env.set_ram(new_pos_down, 55)

    def stop_all_cars_edge(self):
        """
        Stops all cars and repositions some to predefined positions.
        """
        for car_stop in range(33, 43):
            self.env.set_ram(car_stop, 100)
        for new_pos_down in range(108, 113):
            self.env.set_ram(new_pos_down, 15)
        for new_pos_down in range(113, 118):
            self.env.set_ram(new_pos_down, 150)

    def all_black_cars(self):
        """
        Colors all cars black.
        """
        for car in range(77, 87):
            self.env.set_ram(car, 0)

    def all_white_cars(self):
        """
        Colors all cars white.
        """
        for car in range(77, 87):
            self.env.set_ram(car, 15)

    def all_red_cars(self):
        """
        Colors all cars red.
        """
        for car in range(77, 87):
            self.env.set_ram(car, 66)

    def all_green_cars(self):
        """
        Colors all cars green.
        """
        for car in range(77, 87):
            self.env.set_ram(car, 210)

    def all_blue_cars(self):
        """
        Colors all cars blue.
        """
        for car in range(77, 87):
            self.env.set_ram(car, 145)

    # My modifications

    def invisible_mode(self):
        """
        Colors all cars invisible.
        """
        for car in range(77, 87):
            self.env.set_ram(car, 6)

    def strobo_mode(self):
        """
        Each car changes color randomly every timestep.
        """
        for car in range(77, 87):
            color = random.randint(0, 255)
            self.env.set_ram(car, color)

    clock_counter = 0

    def phantom_mode(self):
        """
        Each car changes color from black to invisible approximately every second.
        """
        for car in range(77, 87):
            # global clock_counter -> braucht man hier nicht, da durch self schon angegeben wird, dass
            # die Variable außerhalb der Methode gemeint ist.
            if self.clock_counter % 60 == 0:
                self.env.set_ram(car, 1)
            elif self.clock_counter % 30 == 0:
                self.env.set_ram(car, 6)
        self.clock_counter = self.clock_counter + 1

    def blinking_mode(self):
        """
        Each car changes color randomly approximately every second.
        """
        for car in range(77, 87):
            if self.clock_counter % 30 == 0:
                rand_number = random.randint(1, 8)
                self.env.set_ram(car, self._color_map[rand_number])
        self.clock_counter = self.clock_counter + 1

    def speed_mode(self):
        """
        Each car drives with speed 2 (default)
        """
        speed = 2  # default
        ram = self.env.get_ram()
        for car_x in range(108, 113):
            x_value = ram[car_x]
            self.env.set_ram(car_x, x_value+speed)
        for car_x in range(113, 118):
            x_value = ram[car_x]
            new_x = x_value-speed
            if new_x < 0:
                new_x = 0  # to prevent negative x-koordinates
            self.env.set_ram(car_x, new_x)

    def _set_active_modifications(self, active_modifs):
        """
        Specifies which modifications are active.

        :param active_modifs: A list of active modification names.
        """
        self.active_modifications = set(active_modifs)

    def _fill_modif_lists(self):
        """
        Returns modification lists with active modifications.

        :return: Tuple of step_modifs, reset_modifs, and post_detection_modifs lists.
        """
        modif_mapping = {
            "stop_random_car": self.stop_random_car,
            "stop_all_cars_tunnel": self.stop_all_cars,
            "stop_all_cars_edge": self.stop_all_cars_edge,
            "align_all_cars": self.align_all_cars,
            "all_black_cars": self.all_black_cars,
            "all_white_cars": self.all_white_cars,
            "all_red_cars": self.all_red_cars,
            "all_green_cars": self.all_green_cars,
            "all_blue_cars": self.all_blue_cars,
            "invisible_mode": self.invisible_mode,
            "strobo_mode": self.strobo_mode,
            "phantom_mode": self.phantom_mode,
            "blinking_mode": self.blinking_mode,
            "speed_mode": self.speed_mode,
            "reverse_car_speed_bottom": self.reverse_car_speed_bottom,
            "reverse_car_speed_top": self.reverse_car_speed_top,
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
