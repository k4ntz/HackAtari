"""
This module provides an enhanced gaming experience for the Atari game "Boxing".
The following additions have been added:
- One armed bxing disables the right arm of the player charakter
- gravity boxing adds a constant donward movemnt to the player charakter
- drunken boxing makes the player chrakter move in random directions

"""
from time import sleep
import argparse
import torch
import cv2
import pygame
import numpy as np
from ocatari.core import OCAtari, DEVICE
from ocatari.utils import load_agent
import gymnasium as gym


# Set up the argument parser for the Boxing game modifications.
# This allows players to customize their gameplay experience through command-line options.
parser = argparse.ArgumentParser(description='Boxing Game Argument Setter')


# Argument to enable the one armed boxing mode
parser.add_argument('-oa', '--one-armed', action='store_true',
                    help='Enable one armed boxing mode in the game')

# Argument to enable the gravity boxing mode
parser.add_argument('-g', '--gravity', action='store_true',
                    help='Enable gravity pull on the PC')

# Argument to enable the drunken boxing mode
parser.add_argument('-db', '--drunken-boxing', action='store_true',
                    help='Enable drunke boxing mode')

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

ONE_ARMED_MODE = args.one_armed
"""
ONE_ARMED_MODE controls the one_armed boxing mode.
When set to True via the '--one-armed' argument, one_armed Mode is enabled.
"""


GRAVITY_BOXING = args.gravity
"""
ONE_ARMED_MODE controls the gravity boxing mode.
When set to True via the '--gravity' argument, gravity Mode is enabled.
"""

DRUNKEN_BOXING = args.drunken_boxing
"""
ONE_ARMED_MODE controls the drunken boxing mode.
When set to True via the '--drunken-boxing' argument, drunken boxing Mode is enabled.
"""

def one_armed_boxing(self):
    '''
    one_armed_boxing: disables the "hitting motion" with the right arm permanently
    '''
    self.set_ram(101, 128) 

def gravity_boxing(self):
    '''
    gravity_boxing: Increase the value in RAM cell 34 until reaching a certain threshold
    '''
    curr_player_pos = self.get_ram()[34]
    if curr_player_pos < 87 and not TOGGLE_HUMAN_MODE:
        curr_player_pos += 1
        self.set_ram(34, curr_player_pos)

    if TOGGLE_HUMAN_MODE:
        if curr_player_pos < 87 and not (pygame.K_w in list(self.current_keys_down)):
            curr_player_pos += 1
            self.set_ram(34, curr_player_pos)

def forward(self):
    '''
    Moves the player character forward in the game environment.
    '''
    curr_player_pos_x = self.get_ram()[32]
    curr_player_pos_x_enemy = self.get_ram()[33]

    if 0 < curr_player_pos_x < 109 and curr_player_pos_x + 14 != curr_player_pos_x_enemy:
        curr_player_pos_x += 1
        self.set_ram(32, curr_player_pos_x)

def move_up(self):
    '''
    Moves the player character up in the game environment.
    '''
    curr_player_pos_y = self.get_ram()[34]

    if 0 < curr_player_pos_y < 87:
        curr_player_pos_y -= 1
        self.set_ram(34, curr_player_pos_y)

def backward(self):
    '''
    Moves the player character backward in the game environment.
    '''
    curr_player_pos_x = self.get_ram()[32]

    if 0 < curr_player_pos_x < 109:
        curr_player_pos_x -= 1
        self.set_ram(32, curr_player_pos_x)

def down(self):
    '''
    Moves the player character down in the game environment.
    '''
    curr_player_pos_y = self.get_ram()[34]

    if 0 < curr_player_pos_y < 87:
        curr_player_pos_y += 1
        self.set_ram(34, curr_player_pos_y)


def drunken_boxing(self):
    # Add a counter variable to keep track of the function calls
        self.counter = getattr(self, 'counter', 0)

        # Call functions in sequence based on the counter value
        if self.counter % 4 == 0:
            forward(self)
        elif self.counter % 4 == 1:
            move_up(self)
        elif self.counter % 4 == 2:
            backward(self)
        elif self.counter % 4 == 3:
            down(self)

        # Increment the counter for the next function call
        self.counter += 1

        # Introduce a sleep of 1 second (adjust the sleep duration as needed)
        #time.sleep(1)

class BoxingExtended(OCAtari):
    '''
    BoxingExtended: Modifies the Atari game "Boxing" to simulate gravity pulling the player character
    constantly to the right (down on the screen), adding an additional difficulty 
    to the game.
    '''

    def __init__(self, env_name="Boxing", mode="raw", hud=False, obs_mode="dqn", *args, **kwargs):
        '''
        Initializes an OCAtari game environment with preset values for game name, mode, and 
        observation mode. The Heads-Up Display (HUD) is disabled by default.
        '''
        self.render_mode = kwargs.get("render_mode", None)
        # Call __init__ to create the OCAtari environment
        super().__init__(env_name, mode, hud, obs_mode, *args, **kwargs)

    def alter_ram(self):
        '''
        alter_ram: Manipulates the RAM cell at position 34 to simulate gravity.
        The value in the cell is continually increased until the threshold is reached.
        '''
        if ONE_ARMED_MODE:
            one_armed_boxing(self)
        if GRAVITY_BOXING:
            gravity_boxing(self)
        if DRUNKEN_BOXING:
            drunken_boxing(self)

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


class BoxingExtendedHuman(OCAtari): 
    '''
    BoxingExtendedHuman: Enables human play mode for the BoxingExtended game.
    '''

    env: gym.Env

    def __init__(self, env_name: str):
        '''
        Initializes the BoxingExtendedHuman environment with the specified environment name.
        '''
        self.env = OCAtari(env_name, mode="ram", hud=True, render_mode="human",
                            render_oc_overlay=True, frameskip=1)
        self.env.reset()
        self.env.render()  # Initialize the pygame video system

        self.paused = False
        self.current_keys_down = set()
        self.keys2actions = self.env.unwrapped.get_keys_to_action()

    def run(self):
        '''
        run: Runs the BoxingExtendedHuman environment, allowing human interaction with the game.
        '''
        self.running = True
        while self.running:
            self._handle_user_input()
            if not self.paused:
                action = self._get_action()
                # Change RAM value
                if ONE_ARMED_MODE:
                    one_armed_boxing(self.env)
                if GRAVITY_BOXING:
                    gravity_boxing(self.env)
                if DRUNKEN_BOXING:
                    drunken_boxing(self.env)
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
        _handle_user_input: Handles user input for the BoxingExtendedHuman environment.
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
    renderer = BoxingExtendedHuman('Boxing')
    renderer.run()
else:
    env = BoxingExtended(render_mode="human")
    # The following path to the agent has to be modified according to individual user setup
    # and folder names
    dqn_agent = load_agent("../OC_Atari/models/Boxing/dqn.gz", env.action_space.n)
    env.reset()
    # Let the agent play the game for 10000 steps
    for i in range(10000):
        action = dqn_agent.draw_action(env.dqn_obs)
        _, _, done1, done2, _ = env.step(action)
        sleep(0.01)
        if done1 or done2:
            env.reset()
