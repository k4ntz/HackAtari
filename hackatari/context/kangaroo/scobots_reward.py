import numpy as np


def reward_function(self) -> float:
    for obj in self.objects:
        if "player" in str(obj).lower():
            player = obj
            break

    # Get current platform
    platform = np.ceil(
        (player.xy[1] - player.h - 16) / 48
    )  # 0: topmost, 3: lowest platform

    # Encourage moving to the child
    if platform % 2 == 0:  # even platform, encourage left movement
        reward = -player.dx
    else:  # encourage right movement
        reward = player.dx
    # Encourage upward movement
    reward -= player.dy / 5
    if abs(reward) > 100:  # level end
        reward = 100
    return reward
