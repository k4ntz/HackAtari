import numpy as np
goRight = True
onLetter = False

def reward_function(self) -> float:
    global goRight
    global onLetter

    for obj in self.objects:
        if 'player' in str(obj).lower():
            player = obj
            break
    
    if player.dx != 0 and onLetter:
        goRight = not goRight
        onLetter = False

    if player.dy == -1 and player.dx == 0:
        onLetter = True
    
    if goRight == 0:  # even platform, encourage left movement
        reward = - player.dx
    else:  # encourage right movement
        reward = player.dx
    # Encourage upward movement
    reward -= player.dy / 5
    if abs(reward) > 50: # level end
        reward = 100
    return reward