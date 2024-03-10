"""
This module provides an enhanced gaming experience for the Atari game "Breakout" by introducing
customizable difficulty levels trough the addition of drift in two directions
with three diffrent strength options.

Key Features:
-The ability to select which things to disable/enable through the argument parser.
"""

import argparse
from time import sleep
import torch
import cv2
import pygame
import numpy as np
from ocatari.core import OCAtari, DEVICE
from ocatari.utils import load_agent
import gymnasium as gym
import warnings

warnings.warn("Warning: This modfification only works in agent mode.")

# Set up the argument parser for the Breakuout game modifications.
# This allows players to customize their gameplay experience through command-line options.
parser = argparse.ArgumentParser(description='Breakout Game Argument Setter')

# Argument to set the drift direction
# Options:
# - right: Default - Drift to the right
# - left: Drift to the left

parser.add_argument('-d', '--drift', type=str, choices=['right', 'left'], default='right',
                    help='Set the drift direction "right" or "left"')

# Argument to set the drift strength
# Options:
# - 0: no Drift of 0 pixles/points per step
# - 1: Default - medium drift: 2 pixel per step
# - 2: high drift: 3 pixles per step

parser.add_argument('-s', '--stength', type=int, choices=[0, 1, 2], default=0,
                    help='Set the drift direction (0, 1, or 2) - 0 is no, 1 is low, 2 is high')

# Argument to enable human mode.
# When set, the game will be playable by a human player instead of an AI agent.
parser.add_argument('-hu', '--human', action='store_true',
                    help='Enable human mode')

args = parser.parse_args()

DRIFT = args.drift
"""
DRIFT toggles the drift direction, set by the '--drift' argument, 
- DRIFT = right makes the ball drift to the right,
- DRIFT = left makes the ball drift to the left,
 making the game harder.
"""

STRENGTH = args.stength
"""
SRENGTH toggles the drift strength, set by the '--strength' argument.
- STRENGTH = 0 is no drift,
- STRENGTH = 1 is a drift of 2 pixles per ram step,
- STRENGTH = 2 is a high drift of 3 pixles per ram step,
 making the game harder.
"""

TOGGLE_HUMAN_MODE = args.human
"""
A constant that toggles the state of the agent mode.

This constant is used to toggle between the human mode and the agent mode. 
The value 'True' indicates that the human mode is active, while the value
'False' indicates that the agent mode is active.
"""


def define_drift_strength():
    """
    Defines the drift strength of the ball
    according to the parsed arguement
    """
    drift_strength = 0

    if STRENGTH == 1:
        drift_strength = 2
    if STRENGTH == 2:
        drift_strength = 3

    return drift_strength



def right_drift(self):
    """
    Makes the ball drift to the rigth
    by changing the corresponding ram positions
    """
    drift = define_drift_strength()
    ball_x = self.get_ram()[99]
    ball_y = self.get_ram()[101]
    new_ball_pos = ball_x + drift
    #else the ball isnt there at all or outside of the walls
    if (ball_y + 9 <= 196 and new_ball_pos != 0) and 57 <= new_ball_pos <= 199:
        self.set_ram(99, new_ball_pos)

def left_drift(self):
    """
    Makes the ball drift to the left
    by changing the corresponding ram positions
    """
    drift = define_drift_strength()
    ball_x = self.get_ram()[99]
    ball_y = self.get_ram()[101]
    new_ball_pos = ball_x - drift
    #else the ball isnt there at all or outside of the walls
    if (ball_y + 9 <= 196 and new_ball_pos != 0) and 57 <= new_ball_pos <= 199:
        self.set_ram(99, new_ball_pos)


class DriftBreakout(OCAtari):
    '''
    DriftBreakout: Modifies the Atari game "Breakout" to simulate some force like wind
    influencing the ball, adding an additional difficulty to the game.
    '''

    def __init__(self, env_name="Breakout", mode="raw", hud=False, obs_mode="dqn", *args, **kwargs):
        '''
        Initializes an OCAtari game environment with preset values for game name, mode, and 
        observation mode. The Heads-Up Display (HUD) is disabled by default.
        '''
        self.render_mode = kwargs.get("render_mode", None)
        # Call __init__ to create the OCAtari environment
        super().__init__(env_name, mode, hud, obs_mode, *args, **kwargs)

    def alter_ram(self):
        '''
        alter_ram: Manipulates the RAM cell at positions 99 and 101 to simulate wind.
        The value in the cell is altered according to the current position of the ball
        and the given direction and strength.
        '''

        if DRIFT == "right":
            right_drift(self)
        if DRIFT == "left":
            left_drift(self)


    def _step_ram(self, *args, **kwargs):
        '''
        step_ram: Updates the environment by one RAM step.
        '''
        self.alter_ram()
        out = super()._step_ram(*args, **kwargs)
        return out

    def _fill_buffer_dqn(self):
        '''
        _fill_buffer_dqn: Fills the buffer for usage by the DQN agent.
        '''
        image = self._ale.getScreenGrayscale()
        state = cv2.resize(
            image, (84, 84), interpolation=cv2.INTER_AREA
        )
        self._state_buffer.append(torch.tensor(state, dtype=torch.uint8, device=DEVICE))

class DriftBreakoutHuman(OCAtari): 
    '''
    DriftBreakoutHuman: Enables human play mode for the DriftBreakout game.
    '''

    env: gym.Env

    def __init__(self, env_name: str):
        '''
        Initializes the DriftBreakoutHuman environment with the specified environment name.
        '''
        self.env = OCAtari(env_name, mode="revised", hud=True, render_mode="human",
                        render_oc_overlay=True, frameskip=1)
        self.env.reset()
        self.env.render()  # Initialize the pygame video system

        self.paused = False
        self.current_keys_down = set()
        self.keys2actions = self.env.unwrapped.get_keys_to_action()

    def run(self):
        '''
        run: Runs the DriftBreakoutHuman environment, allowing human interaction with the game.
        '''
        self.running = True
        while self.running:
            self._handle_user_input()
            if not self.paused:
                action = self._get_action()
                # Change RAM value

                if DRIFT == "right":
                    right_drift(self.env)
                if DRIFT == "left":
                    left_drift(self.env)

                self.env.step(action)
                self.env.render()
        pygame.quit()

    def _get_action(self):
        '''
        _get_action: Gets the action corresponding to the current key press.
        '''
        pressed_keys = list(self.current_keys_down)
        pressed_keys.sort()
        pressed_keys = tuple(pressed_keys)
        if pressed_keys in self.keys2actions.keys():
            return self.keys2actions[pressed_keys]
        else:
            return 0  # NOOP

    def _handle_user_input(self):
        '''
        _handle_user_input: Handles user input for the DriftBreakoutHuman environment.
        '''
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

# If statement for switching between human play mode and RL agent play mode
if TOGGLE_HUMAN_MODE:
    renderer = DriftBreakoutHuman('Breakout')
    renderer.run()
else:
    env = DriftBreakout(render_mode="human")
    # The following path to the agent has to be modified according to individual user setup
    # and folder names
    dqn_agent = load_agent("../OC_Atari/models/Breakout/dqn.gz", env.action_space.n)
    env.reset()
    # Let the agent play the game for 10000 steps
    for i in range(10000):
        action = dqn_agent.draw_action(env.dqn_obs)
        _, _, done1, done2, _ = env.step(action)
        sleep(0.01)
        if done1 or done2:
            env.reset()
