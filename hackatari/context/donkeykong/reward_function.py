goRight = True
onLetterUp = False
onLetterDown = False
startLetterFromBottom = False


def reward_function(self) -> float:
    global goRight
    global onLetterUp
    global onLetterDown
    global startLetterFromBottom

    for obj in self.objects:
        if "player" in str(obj).lower():
            player = obj
            break

    if player.dx != 0 and (onLetterUp or onLetterDown):
        if onLetterUp and startLetterFromBottom:
            goRight = not goRight
        if onLetterDown and not startLetterFromBottom:
            goRight = not goRight
        onLetterUp = False
        onLetterDown = False

    if player.dy == -1 and player.dx == 0:
        if not (onLetterDown or onLetterUp):
            startLetterFromBottom = True
        onLetterUp = True
        onLetterDown = False
    elif player.dy == 1 and player.dx == 0:
        if not (onLetterDown or onLetterUp):
            startLetterFromBottom = False
        onLetterDown = True
        onLetterUp = False

    if goRight == 0:  # even platform, encourage left movement
        reward = -player.dx
    else:  # encourage right movement
        reward = player.dx
    # Encourage upward movement
    reward -= player.dy
    if abs(reward) > 50:  # level end
        reward = 100
    # print( onLetterDown, onLetterUp, startLetterFromBottom, reward)
    return reward
