"""
This module provides an enhanced gaming experience for the Atari game "Kangaroo" by introducing
customizable difficulty levels trough modified starting positions,
as well as the ability to disable the monkeys
and/or the falling coconut.

Key Features:
-The ability to select which things to disable/enable through the argument parser.
"""

import argparse
import random
from time import sleep
import gymnasium as gym
import pygame
import torch
import cv2
import numpy as np
from ocatari.core import OCAtari, DEVICE
from ocatari.utils import load_agent

# Set up the argument parser for the Kangaroo game modifications.
# This allows players to customize their gameplay experience through command-line options.
parser = argparse.ArgumentParser(description='Kangaroo Game Argument Setter')

group = parser.add_mutually_exclusive_group(required=False)

# Argument to set the starting floor level.
# Options:
# - 0: Default starting floor (most challenging)
# - 1: Start one floor up (moderate difficulty)
# - 2: Start two floors up (easiest, closest to the goal)
group.add_argument('-f', '--floor', type=int, choices=[0, 1, 2], default=0,
                   help='Set the starting floor (0, 1, or 2)')

# Argument to enable human mode.
# When set, the game will be playable by a human player instead of an AI agent.
parser.add_argument('-hu', '--human', action='store_true',
                    help='Enable human mode')

# Argument to disable monkeys in the game.
# Useful for reducing game difficulty or for specific testing scenarios.
parser.add_argument('-dm', '--disable-monkeys', action='store_true',
                    help='Disable monkeys in the game')

# Argument to disable the falling coconut.
# This can make the game easier or be used for experimental purposes.
parser.add_argument('-dc', '--disable-falling-coconut', action='store_true',
                    help='Disable the falling coconut in the game')

# Argument to enable easy mode.
# When set, the game will let the player start one level higher with each life lost.
group.add_argument('-e', '--easy-mode', action='store_true',
                   help='Enable easy mode')

# Argument to enable random difficulty mode.
# When set, the game will let the player start at a random floor potentially making the game easier.
group.add_argument('-ra', '--random-difficulty', action='store_true',
                   help='Enable random difficulty mode')

args = parser.parse_args()

TOGGLE_HUMAN_MODE = args.human
"""
TOGGLE_HUMAN_MODE reflects the choice to play in human mode,
as determined by the '--human' argument.
If True, the game will be set to human mode, allowing for manual play.
If False, the game operates in agent mode, suitable for AI interactions.
"""

EASY_MODE = args.easy_mode
"""
EASY_MODE reflects the choice to play in easy mode,
as determined by the '--easy-mode' argument.
If True, the game will be set to easy mode, where for each lost live
the player starts one floor higher. The highest floor the player can start
is the second one
"""

RANDOM_DIFFICULTY = args.random_difficulty
"""
RANDOM_DIFFICULTY reflects the choice to play in random difficulty mode,
as determined by the '--random-difficulty' argument.
If True, the game will be set to random difficulty mode, choosing a 
random floor for each round.
"""

FLOOR = args.floor
"""
FLOOR determines the starting floor level based on the '--floor' argument.
- FLOOR = 0 sets the game to start at the default, most challenging level.
- FLOOR = 1 raises the starting position by one floor, reducing difficulty.
- FLOOR = 2 raises the starting position by two floors, offering the easiest starting condition.

"""

DISABLE_MONKEYS = args.disable_monkeys
"""
DISABLE_MONKEYS controls the presence of monkeys in the game.
When set to True via the '--disable-monkeys' argument, monkeys are removed from the game.
"""

DISABLE_COCONUTS = args.disable_falling_coconut
"""
DISABLE_COCONUTS toggles the falling coconut hazard.
If True, set by the '--disable-falling-coconut' argument, the falling coconut is removed,
simplifying the gameplay.
"""

# Constants for clarity and maintainability
KANGAROO_POS_X_INDEX = 17  # RAM index for kangaroo's X position
KANGAROO_POS_Y_INDEX = 16  # RAM index for kangaroo's Y position
LEVEL_2 = 2

# Starting positions based on different conditions
FLOOR_1_LEVEL2_POS = (25, 10)
FLOOR_2_LEVEL2_POS = (100, 6)
FLOOR_1_START_POS = (65, 12)
FLOOR_2_START_POS = (65, 6)
ANY_FLOOR_INSTANT_WIN = (110, 0)


def disable_monkeys(self):
    """
    Disables the monkeys in the game
    by changing the corresponding ram positions
    """
    for x in range(4):
        self.set_ram(11 - x, 127)


def disable_falling_coconut(self):
    """
    Disables the falling coconut in the game,
    by changing the corresponding ram positions
    """
    self.set_ram(33, 255)
    self.set_ram(35, 255)


def set_ram_kang_pos(self, pos_x, pos_y):
    """
    Set the kangaroo's position.
    Args:
    pos_x (int): The x-coordinate for the kangaroo's position.
    pos_y (int): The y-coordinate for the kangaroo's position.
    """
    self.set_ram(KANGAROO_POS_X_INDEX, pos_x)
    self.set_ram(KANGAROO_POS_Y_INDEX, pos_y)


def is_at_start(pos):
    """
    checks whether the given x and y coordinates are in the starting range of the kangaroo.
    Args:
    pos_x (int): The x-coordinate.
    pos_y (int): The y-coordinate.
    """
    return 5 < pos[0] < 11 and 16 < pos[1] < 21


def check_new_level_life(self, current_lives, current_level):
    """
    Checks whether the level or amount of lives changed
    and if either or both did re-enable the changing of the starting
    position and updating the current lives and level
    """
    if current_lives != self.last_lives or current_level != self.last_level:
        self.position_set = False
        self.last_lives = current_lives
        self.last_level = current_level


def set_kangaroo_position(self, current_level, kangaroo_pos, human_mode):
    """
    Sets the kangaroo's starting position depending on the FLOOR argument
    """
    if is_at_start(kangaroo_pos) and not self.position_set:
        if FLOOR == 1:
            # For floor 1, position depends on whether the current level is 2
            new_pos = FLOOR_1_LEVEL2_POS if current_level == LEVEL_2 else FLOOR_1_START_POS
            if not human_mode:
                set_ram_kang_pos(self, *new_pos)
            else:
                set_ram_kang_pos(self.env, *new_pos)
        elif FLOOR == 2:
            # For floor 2, position is set to a different location
            # but also depends on the current level
            new_pos = FLOOR_2_LEVEL2_POS if current_level == LEVEL_2 else FLOOR_2_START_POS
            if not human_mode:
                set_ram_kang_pos(self, *new_pos)
            else:
                set_ram_kang_pos(self.env, *new_pos)
        self.position_set = True


def easy_mode(self, current_level, current_lives, kangaroo_pos, human_mode):
    """
    Checks the current amount of lives and lets the player on a higher floor
    if the amount of lives is low enough.
    """
    if is_at_start(kangaroo_pos) and not self.position_set:
        if current_lives == 1:
            # For floor 1, position depends on whether the current level is 2
            new_pos = FLOOR_1_LEVEL2_POS if current_level == LEVEL_2 else FLOOR_1_START_POS
            if not human_mode:
                set_ram_kang_pos(self, *new_pos)
            else:
                set_ram_kang_pos(self.env, *new_pos)
        elif current_lives == 0:
            # For floor 2, position is set to a different location
            # but also depends on the current level
            new_pos = FLOOR_2_LEVEL2_POS if current_level == LEVEL_2 else FLOOR_2_START_POS
            if not human_mode:
                set_ram_kang_pos(self, *new_pos)
            else:
                set_ram_kang_pos(self.env, *new_pos)
        self.position_set = True



def random_difficulty(self, current_level, kangaroo_pos, human_mode):
    """
    Generates a random number and the lets the player start on that floor.
    """
    random_number = random.randint(0, 2)
    if is_at_start(kangaroo_pos) and not self.position_set:
        if random_number == 1:
            # For floor 1, position depends on whether the current level is 2
            new_pos = FLOOR_1_LEVEL2_POS if current_level == LEVEL_2 else FLOOR_1_START_POS
            if not human_mode:
                set_ram_kang_pos(self, *new_pos)
            else:
                set_ram_kang_pos(self.env, *new_pos)
        elif random_number == 2:
            # For floor 2, position is set to a different location
            # but also depends on the current level
            new_pos = FLOOR_2_LEVEL2_POS if current_level == LEVEL_2 else FLOOR_2_START_POS
            if not human_mode:
                set_ram_kang_pos(self, *new_pos)
            else:
                set_ram_kang_pos(self.env, *new_pos)
        self.position_set = True


class KangarooExtended(OCAtari):
    """
    KangarooExtended: Modifies the Atari game "Kangaroo" to enable the player
    to choose the difficulty of the game, by choosing how many floors should be skipped
    by changing the starting position.
    Making it easier for humans but not necessarily for agents.
    The Monkeys and the falling coconut can be disabled as well.
    """

    # initializing the game from the original game of Kangaroo
    def __init__(self, env_name="Kangaroo", mode="revised", hud=False,
                 obs_mode="dqn", *args, **kwargs):
        """
        __init__: Initializes a OCAtari game environment. The game environment name, the mode
            and the observation mode are preset. The HUD is disabled.
        """
        self.render_mode = kwargs["render_mode"] if "render_mode" in kwargs else None
        super().__init__(env_name, mode, hud, obs_mode, *args, **kwargs)
        self.position_set = False
        self.level_set = False
        self.last_level = self.get_ram()[36]
        self.last_lives = self.get_ram()[45]

    def alter_ram(self):
        """
        alter_ram: sets the starting position depending on the difficulty,
        which is chosen with the FLOOR constant. And disables the
        monkeys/the falling coconut if the corresponding parser arguments
        have been set.
        """
        # get the current ram state
        ram = self.get_ram()

        current_level = ram[36]
        kangaroo_pos = (ram[KANGAROO_POS_X_INDEX], ram[KANGAROO_POS_Y_INDEX])
        current_lives = ram[45]

        if DISABLE_MONKEYS:
            disable_monkeys(self)
        if DISABLE_COCONUTS:
            disable_falling_coconut(self)

        # checks whether the player has finished a level or has lost a live
        # to re-enable the teleportation to the new starting position
        check_new_level_life(self, current_lives, current_level)
        if is_at_start(kangaroo_pos):
            if EASY_MODE:
                easy_mode(self, current_level, current_lives, kangaroo_pos, False)
            elif RANDOM_DIFFICULTY:
                random_difficulty(self, current_level, kangaroo_pos, False)
            else:
                set_kangaroo_position(self, current_level, kangaroo_pos, False)

    def _step_ram(self, *args, **kwargs):
        """
        step_ram: Updates the environment by one ram step
        """
        self.alter_ram()
        ram_step = super()._step_ram(*args, **kwargs)
        return ram_step

    def _fill_buffer_dqn(self):
        """
        _fill_buffer_dqn: Fills the buffer for usage by the dqn agent
        """
        image = self._ale.getScreenGrayscale()
        state = cv2.resize(
            image, (84, 84), interpolation=cv2.INTER_AREA,
        )
        self._state_buffer.append(torch.tensor(state, dtype=torch.uint8,
                                               device=DEVICE))


class KangarooExtendedHuman(OCAtari):
    """
    KangarooExtendedHuman: Enables human play mode for the kangaroo_extended game.
    """

    env: gym.Env

    def __init__(self, env_name: str):
        """
        Initializes the KangarooExtendedHuman environment with the specified environment name.
        """
        self.env = OCAtari(env_name, mode="revised", hud=True, render_mode="human",
                           render_oc_overlay=True, frameskip=1)
        self.env.reset()
        self.env.render()  # Initialize the pygame video system
        self.position_set = False
        self.level_set = False
        self.last_level = self.env.get_ram()[36]
        self.last_lives = self.env.get_ram()[45]

        self.paused = False
        self.current_keys_down = set()
        self.keys2actions = self.env.unwrapped.get_keys_to_action()

    def run(self):
        """
        run: Runs the KangarooExtendedHuman environment, allowing human interaction with the game
        and alters the game depending on the parser arguments.
        """
        self.running = True
        while self.running:
            self._handle_user_input()
            if not self.paused:
                action = self._get_action()

                ram = self.env.get_ram()

                current_level = ram[36]
                kangaroo_pos = (ram[KANGAROO_POS_X_INDEX], ram[KANGAROO_POS_Y_INDEX])
                current_lives = ram[45]

                if DISABLE_MONKEYS:
                    disable_monkeys(self.env)
                if DISABLE_COCONUTS:
                    disable_falling_coconut(self.env)

                # checks whether the player has finished a level or has lost a live
                # to re-enable the teleportation to the new starting position
                check_new_level_life(self, current_lives, current_level)
                if is_at_start(kangaroo_pos):
                    if EASY_MODE:
                        easy_mode(self, current_level, current_lives, kangaroo_pos, True)
                    elif RANDOM_DIFFICULTY:
                        random_difficulty(self, current_level, kangaroo_pos, True)
                    else:
                        set_kangaroo_position(self, current_level, kangaroo_pos, True)

                self.env.step(action)
                self.env.render()
        pygame.quit()

    def _get_action(self):
        """
        _get_action: Gets the action corresponding to the current key press.
        """
        pressed_keys = list(self.current_keys_down)
        pressed_keys.sort()
        pressed_keys = tuple(pressed_keys)
        if pressed_keys in self.keys2actions.keys():
            return self.keys2actions[pressed_keys]
        else:
            return 0  # NOOP

    def _handle_user_input(self):
        """
        _handle_user_input: Handles user input for the KangarooExtendedHuman environment.
        """
        self.current_mouse_pos = np.asarray(pygame.mouse.get_pos())

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:  # Window close button clicked
                self.running = False

            elif event.type == pygame.KEYDOWN:  # Keyboard key pressed
                if event.key == pygame.K_p:  # 'P': Pause/Resume
                    self.paused = not self.paused

                if event.key == pygame.K_r:  # 'R': Reset
                    self.env.reset()

                elif (event.key,) in self.keys2actions.keys():  # Env action
                    self.current_keys_down.add(event.key)

            elif event.type == pygame.KEYUP:  # Keyboard key released
                if (event.key,) in self.keys2actions.keys():
                    self.current_keys_down.remove(event.key)


# code for having an agent play the modified game

if TOGGLE_HUMAN_MODE:
    renderer = KangarooExtendedHuman('Kangaroo')
    renderer.run()
else:
    env = KangarooExtended(render_mode="human")
    # The following path to the agent has to be modified according to individual user setup
    # and folder names
    dqn_agent = load_agent(r"C:\Workspaces\HackAtari\models\Kangaroo\dqn.gz", env.action_space.n)
    env.reset()
    # Let the agent play the game for 10000 steps
    for i in range(10000):
        action = dqn_agent.draw_action(env.dqn_obs)
        _, _, done1, done2, _ = env.step(action)
        sleep(0.01)
        if done1 or done2:
            env.reset()
