wind_direction_x = 1
wind_direction_y = 1
is_wind_blowing = 0
import random
def wind(self):
    """
    Randomly wiggles the ball
    """
    global wind_direction_x, wind_direction_y, is_wind_blowing

    if random.random() < 0.01 and is_wind_blowing == 0:
        # randomly wind will start to blow
        is_wind_blowing = 10
    elif is_wind_blowing > 0:
        # it will blow for 10 steps
        is_wind_blowing = is_wind_blowing - 1
        
        # it will change direction randomly
        if random.random() < 0.1:
            wind_direction_x = wind_direction_x * -1
        if random.random() < 0.1:
            wind_direction_y = wind_direction_y * -1

        ram = self.get_ram()
        x,y = ram[52], ram[91]

        new_x = x + wind_direction_x
        new_y = y + wind_direction_y

        new_x = max(0, min(255, new_x))
        new_y = max(0, min(255, new_y))

        self.set_ram(52, new_x)
        self.set_ram(91, new_y)

def _modif_funcs(env, modifs):
    for mod in modifs:
        if mod == "wind":
            env.step_modifs.append(wind)
