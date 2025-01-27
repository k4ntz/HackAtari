wind_direction_x = 1
is_wind_blowing = 0
current_player_x = None
old_player_x = None
older_player_x = None
import random
def missle_guide(self):
    """
    player guides missle left and right
    """
    global current_player_x, old_player_x, older_player_x
    # ram[93] -> missle x between 86-211
    # ram[89] -> missle y between 25-193

    ram = self.get_ram()
    if current_player_x is None and old_player_x is None and older_player_x is None:
        older_player_x = ram[94]
    elif current_player_x is None and older_player_x is None:
        older_player_x = ram[94]
    elif current_player_x is None:
        current_player_x = ram[94]
    else:
        older_player_x = old_player_x
        old_player_x = current_player_x
        current_player_x = ram[94]

        try:
            if current_player_x - older_player_x == 255:
                diff = -1
            else:
                diff = current_player_x - older_player_x
            
            missle_x = ram[93]
            new_missle_x = missle_x + diff * 1
            new_missle_x = max(86, min(211, new_missle_x))
            self.set_ram(93, new_missle_x)
        except:
            pass

def player_drift(self):
    """
    randomly wind blows to player ship
    """
    global wind_direction_x, is_wind_blowing

    if random.random() < 0.01 and is_wind_blowing == 0:
        # randomly wind will start to blow
        is_wind_blowing = 10
    elif is_wind_blowing > 0:
        # it will blow for 10 steps
        is_wind_blowing = is_wind_blowing - 1
        
        # it will change direction randomly
        if random.random() < 0.1:
            wind_direction_x = wind_direction_x * -1

        ram = self.get_ram()
        player_x = ram[94] # between 82 and 207

        new_player_x = player_x + wind_direction_x * 1
        new_player_x = max(82, min(207, new_player_x))
        self.set_ram(94, new_player_x)


def _modif_funcs(env, modifs):
    for mod in modifs:
        if mod == "missle_guide":
            env.step_modifs.append(missle_guide)
        if mod == "player_drift":
            env.step_modifs.append(player_drift)