from ocatari.ram.skiing import *

REWARD = 32


def reward_function(self) -> float:
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
