import random

def teleport(self):
    """
    ball is teleported randomly at some certain places
    """
    # 67 and 68 can be between [0-255]
    # 67 is how far is the ball from left
    # 68 is how far is the ball from top

    ram = self.get_ram()

    # "if 10 < ram[67] < 145:" to prevent teleportations at the left/right tubes
    # randomly teleports the ball to one of these locations
    if 10 < ram[67] < 145:
        if random.random() < 0.001:
            p = random.random()

            if p < 1/7:
                self.set_ram(67, 140)
                self.set_ram(68, 35)
            elif p < 2/7:
                self.set_ram(67, 15)
                self.set_ram(68, 40)
            elif p < 3/7:
                self.set_ram(67, 95)
                self.set_ram(68, 60)
            elif p < 4/7:
                self.set_ram(67, 20)
                self.set_ram(68, 95)
            elif p < 5/7:
                self.set_ram(67, 90)
                self.set_ram(68, 120)
            elif p < 6/7:
                self.set_ram(67, 65)
                self.set_ram(68, 165)
            else:
                self.set_ram(67, 130)
                self.set_ram(68, 160)


def _modif_funcs(env, modifs):
    for mod in modifs:
        if mod == "teleport":
            env.step_modifs.append(teleport)