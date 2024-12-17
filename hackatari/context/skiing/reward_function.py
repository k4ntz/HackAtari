from ocatari.ram.skiing import *

REWARD = 32


def reward_function_old(self) -> float:
    global REWARD
    ram = self.get_ram()
    speed = ram[14] * 0.01
    score = ram[107]
    if ram[15] < 4 or ram[15] > 11:
        reward = speed * 0.2
    else:
        reward = speed

    if score != REWARD:
        reward += 100000

    REWARD = ram[107]
    return reward


def reward_function(self) -> float:
    global REWARD
    ram = self.get_ram()
    orientation = -abs(8-ram[15])*0.5
    speed = ram[14]*.01
    score = ram[107]
    reward = orientation+speed

    if score != REWARD:
        reward += 100000

    REWARD = ram[107]
    return reward
