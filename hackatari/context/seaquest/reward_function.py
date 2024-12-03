from ocatari.ram.seaquest import *

LOW_OXYGEN = False
DIVERS = 0
COLLISION = False
COLLECTED = 0


def check_collision(obj1, obj2):
    """
    Check if two GameObjects collide based on their bounding boxes.
    """
    # Calculate boundaries for object A
    right1 = obj1.x + obj1.w + 5
    bottom1 = obj1.y + obj1.h + 5

    # Calculate boundaries for object B
    right2 = obj2.x + obj2.w
    bottom2 = obj2.y + obj2.h

    # Check for overlap on the x-axis
    collision_x = obj1.x < right2 and right1 > obj2.x

    # Check for overlap on the y-axis
    collision_y = obj1.y < bottom2 and bottom1 > obj2.y

    # Return True if both conditions are met, otherwise False
    return collision_x and collision_y


def reward_function(self) -> float:
    global LOW_OXYGEN
    global DIVERS
    global COLLISION
    global COLLECTED

    game_objects = self.objects
    reward = 0.0

    # Define categories for easy identification
    player = None
    divers = []
    enemies = []
    player_missiles = []
    enemy_missiles = []
    oxygen_bar = None

    # Classify objects
    for obj in game_objects:
        if isinstance(obj, Player):
            player = obj
        elif isinstance(obj, Diver):
            divers.append(obj)
        elif isinstance(obj, Shark) or isinstance(obj, Submarine):
            enemies.append(obj)
        elif isinstance(obj, PlayerMissile):
            player_missiles.append(obj)
        elif isinstance(obj, EnemyMissile):
            enemy_missiles.append(obj)
        elif isinstance(obj, OxygenBar):
            oxygen_bar = obj

    if player:
        for diver in divers:
            if check_collision(player, diver) and COLLECTED != 6:
                COLLISION = True

    if DIVERS > len(divers) and COLLISION:
        reward += 1  # Scaled down reward for collecting a diver
        COLLECTED += 1
        COLLISION = False

    DIVERS = len(divers)

    if player.y == 45:
        if COLLECTED == 6:
            reward += 100
            COLLECTED = 0
        elif COLLECTED > 0:
            COLLECTED -= 1
            if LOW_OXYGEN:
                LOW_OXYGEN = False
                reward += 5
            else:
                reward += 0

    if oxygen_bar and oxygen_bar.value <= 20 and player.y != 45:
        LOW_OXYGEN = True

    return reward
