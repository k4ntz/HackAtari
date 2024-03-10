"""
This module provides an enhanced gaming experience for the Atari game "Seaquest" by introducing
the ability to disable the enemies from appearing.

Key Features:
-The ability to select which things to disable/enable through the argument parser.
"""

import argparse
from time import sleep
import gymnasium as gym
import pygame
import torch
import cv2
import numpy as np
from ocatari.core import OCAtari, DEVICE
from ocatari.utils import load_agent


# Set up the argument parser for the Seaquest game modifications.
# This allows players to customize their gameplay experience through command-line options.
parser = argparse.ArgumentParser(description='Seaquest Game Argument Setter')


# Argument to enable human mode.
# When set, the game will be playable by a human player instead of an AI agent.
parser.add_argument('-hu', '--human', action='store_true',
                    help='Enable human mode')

# Argument to disable enemies in the game.
# Useful for reducing game difficulty or for specific testing scenarios.
parser.add_argument('-de', '--disable-enemies', action='store_true',
                    help='Disable enemies in the game')

args = parser.parse_args()

TOGGLE_HUMAN_MODE = args.human
"""
TOGGLE_HUMAN_MODE reflects the choice to play in human mode,
as determined by the '--human' argument.
If True, the game will be set to human mode, allowing for manual play.
If False, the game operates in agent mode, suitable for AI interactions.
"""

DISABLE_ENEMIES = args.disable_enemies
"""
DISABLE_ENEMIES controls the presence of enemies in the game.
When set to True via the '--disable-enemies' argument, enemies are removed from the game.
"""

def disable_enemies(self):
    """
    Disables the enemies from appearing. But doesn't disable
    the divers turning into Missiles.
    """
    for x in range(4):
        self.set_ram(36 + x, 0)



class SeaquestNoEnemies(OCAtari):
    """
    SeaquestNoEnemies: Modifies the Atari game "Seaquest" with the possibility to
    disable the enemies from appearing.
    """

    # initializing the game from the original game of Seaquest
    def __init__(self, env_name="Seaquest", mode="revised", hud=False,
                 obs_mode="dqn", *args, **kwargs):
        """
        __init__: Initializes a OCAtari game environment. The game environment name, the mode
            and the observation mode are preset. The HUD is disabled.
        """
        self.render_mode = kwargs["render_mode"] if "render_mode" in kwargs else None
        super().__init__(env_name, mode, hud, obs_mode, *args, **kwargs)

    def alter_ram(self):
        """
        alter_ram: alters the game depending on parser arguments
        """
        if DISABLE_ENEMIES:
            disable_enemies(self)



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


class SeaquestNoEnemiesHuman(OCAtari):
    """
    SeaquestNoEnemiesHuman: Enables human play mode for the 'seaquest_no_enemies' game.
    """

    env: gym.Env

    def __init__(self, env_name: str):
        """
        Initializes the SeaquestNoEnemiesHuman environment with the specified environment name.
        """
        self.env = OCAtari(env_name, mode="revised", hud=True, render_mode="human",
                           render_oc_overlay=True, frameskip=1)
        self.env.reset()
        self.env.render()  # Initialize the pygame video system

        self.paused = False
        self.current_keys_down = set()
        self.keys2actions = self.env.unwrapped.get_keys_to_action()

    def run(self):
        """
        run: Runs the SeaquestNoEnemiesHuman environment, allowing human interaction with the game
        and alters the game depending on the parser arguments.
        """
        self.running = True
        while self.running:
            self._handle_user_input()
            if not self.paused:
                action = self._get_action()

                if DISABLE_ENEMIES:
                    disable_enemies(self.env)

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
        return 0  # NOOP

    def _handle_user_input(self):
        """
        _handle_user_input: Handles user input for the SeaquestNoEnemiesHuman environment.
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
    renderer = SeaquestNoEnemiesHuman('Seaquest')
    renderer.run()
else:
    env = SeaquestNoEnemies(render_mode="human")
    # The following path to the agent has to be modified according to individual user setup
    # and folder names
    dqn_agent = load_agent(r"C:\Workspaces\OC_Atari\models\Seaquest\dqn.gz", env.action_space.n)
    env.reset()
    # Let the agent play the game for 10000 steps
    for i in range(10000):
        action = dqn_agent.draw_action(env.dqn_obs)
        _, _, done1, done2, _ = env.step(action)
        sleep(0.01)
        if done1 or done2:
            env.reset()
