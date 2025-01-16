# from random import random
PLAYER_COLOR = 1
ENEMY_COLOR = 0


def team_colors(self):
    '''
    Changes colors of the teams according to the mod argument. Colors are the playable options from the main menu (main menu skipped in gymnasium)
    '''
    global PLAYER_COLOR, ENEMY_COLOR
    self.set_ram(94, PLAYER_COLOR)
    self.set_ram(95, ENEMY_COLOR)


def _modif_funcs(env, modifs):
    for mod in modifs:
        if mod.startswith("team_colors"):
            global PLAYER_COLOR, ENEMY_COLOR
            for i in range(11, len(mod)):
                if mod[i] == "p" and mod[i+1].isdigit():
                    mod_n = int(mod[i+1])
                    if mod_n < 0 or mod_n > 5:
                        raise ValueError(
                            "Invalid color for player, choose value 0-5")
                    PLAYER_COLOR = mod_n
                elif mod[i] == "e" and mod[i+1].isdigit():
                    mod_n = int(mod[i+1])
                    if mod_n < 0 or mod_n > 5:
                        raise ValueError(
                            "Invalid color for enemy, choose value 0-5")
                    ENEMY_COLOR = mod_n
            env.reset_modifs.append(team_colors)
        else:
            print('Invalid or unknown modification')
