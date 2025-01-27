import random
def mother_ship_color(self):
    """
    mother ship changes color randomly
    """
    ram = self.get_ram()

    if random.random() < 0.01:
        self.set_ram(11, random.randint(0, 240))
        self.set_ram(12, random.randint(0, 240))

speed_sign = 1
def player_missle(self):
    """
    randomly speeds up or down the player missle
    """
    global speed_sign
    ram = self.get_ram()
    missle_y = ram[67]
    
    # randomly change it to speeding up or slowing down the missle
    if random.random() < 0.01:
        speed_sign = speed_sign * -1

    if missle_y != 127 and random.random() < 0.1:
        new_missle_y = missle_y + 7 * speed_sign
        new_missle_y = max(0, min(255, new_missle_y))
        self.set_ram(67, new_missle_y)

def enemy_color(self):
    """
    randomly makes enemies change color
    """
    if random.random() < 0.1:
        p = random.random()
        if p<0.33:
            self.set_ram(40, 196)
        elif 0.33<p<0.66:
            self.set_ram(40, 204)
        elif 0.66<p:
            self.set_ram(40, 212)

def _modif_funcs(env, modifs):
    for mod in modifs:
        if mod == "mother_ship_color":
            env.step_modifs.append(mother_ship_color)
        if mod == "player_missle":
            env.step_modifs.append(player_missle)
        if mod == "enemy_color":
            env.step_modifs.append(enemy_color)
