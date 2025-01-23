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
        self.env.set_ram(random_car, 100 if counter > 0 else 0)

    def align_all_cars(self):
        """
        Stops all cars based on a biased random decision.
        """
        car_all = random.choices([0, 1], weights=[0.6, 0.4], k=1)[0]
        for car_pos in range(33, 43):
            self.env.set_ram(car_pos, 100 if car_all > 0 else 0)

    def stop_all_cars(self):
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
            "stop_all_cars": self.stop_all_cars,
            "align_all_cars": self.align_all_cars,
            "all_black_cars": self.all_black_cars,
            "all_white_cars": self.all_white_cars,
            "all_red_cars": self.all_red_cars,
            "all_green_cars": self.all_green_cars,
            "all_blue_cars": self.all_blue_cars,
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
