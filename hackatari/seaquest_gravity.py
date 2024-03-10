"""
This module provides an enhanced gaming experience for the Atari game "Seaquest".
The following additions have been added:
- Enable gravity for the player.
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

# Set up the argument parser for the Seaquest game modifications.
# This allows players to customize their gameplay experience through command-line options.
parser = argparse.ArgumentParser(description='Seaquest Game Argument Setter')


# Argument to enable gravity for the player.
parser.add_argument('-gr', '--enable-gravity', action='store_true',
                    help='Enables gravity for the player')

# Argument to enable human mode.
# When set, the game will be playable by a human player instead of an AI agent.
parser.add_argument('-hu', '--human', action='store_true',
                    help='Enable human mode')

args = parser.parse_args()

TOGGLE_HUMAN_MODE = args.human
"""
A constant that toggles the state of the agent mode.

This constant is used to toggle between the human mode and the agent mode. 
The value 'True' indicates that the human mode is active, while the value
'False' indicates that the agent mode is active.
"""
ENABLE_GRAVITY = args.enable_gravity
"""
ENABLE_GRAVITY controls the gravity for the player.
When set to True via the '--enable-gravity' argument, gravity is enabled for the player.
"""


def gravity(self):
    """
    Enables gravity for the player.
    """
    ram = self.get_ram()
    self.set_ram(97, ram[97] + 1)




def is_gamestart(self):
    """
    Determines if it is the start of the game
    via the position of the player and the points
    """
    ram = self.get_ram()
    if ram[97] == 13 and ram[70] == 76 and ram[26] == 80:
        return True
    return False



class SeaquestGravity(OCAtari):
    '''
    SeaquestGravity: Modifies the Atari game "Seaquest" to include diverse extra settings,
    adding additional options to the gameplay making it easier or harder.
    '''

    def __init__(self, env_name="Seaquest", mode="raw", hud=False, obs_mode="dqn", *args, **kwargs):
        '''
        Initializes an OCAtari game environment with preset values for game name, mode, and
        observation mode. The Heads-Up Display (HUD) is disabled by default.
        '''
        self.render_mode = kwargs.get("render_mode", None)
        # Call __init__ to create the OCAtari environment
        super().__init__(env_name, mode, hud, obs_mode, *args, **kwargs)

    def alter_ram(self):
        '''
        alter_ram: alters the game depending on parser arguments
        '''
        if ENABLE_GRAVITY and not is_gamestart(self) and self.get_ram()[97] < 108:
            gravity(self)

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


class SeaquestGravityHuman(OCAtari):
    '''
    SeaquestGravityHuman: Enables human play mode for the SeaquestGravity game.
    '''

    env: gym.Env

    def __init__(self, env_name: str):
        '''
        Initializes the SeaquestGravityHuman environment with the specified environment name.
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
        run: Runs the SeaquestGravity environment, allowing human interaction with the game.
        '''
        self.running = True
        while self.running:
            self._handle_user_input()
            if not self.paused:
                action = self._get_action()
                # Change RAM value for human mode

                if (ENABLE_GRAVITY and not is_gamestart(self.env) and self.env.get_ram()[97] < 108
                        and not pygame.K_w in list(self.current_keys_down)):
                    gravity(self.env)

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
        return 0  # NOOP

    def _handle_user_input(self):
        '''
        _handle_user_input: Handles user input for the SeaquestGravityHuman environment.
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
    renderer = SeaquestGravityHuman('Seaquest')
    renderer.run()
else:
    env = SeaquestGravity(render_mode="human")
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
