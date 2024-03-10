"""
This module provides an enhanced gaming experience for the Atari game "Tennis" by the addition
of wind or drift in the direction of up and right.
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

# Set up the argument parser for the Tennis game modifications.
# This allows players to customize their gameplay experience through command-line options.
parser = argparse.ArgumentParser(description='Tennis Game Argument Setter')

# Argument to enable human mode.
# When set, the game will be playable by a human player instead of an AI agent.
parser.add_argument('-hu', '--human', action='store_true',
                    help='Enable human mode')

# Argument to enable wind.
# When set, the ball will drift as if infuenced by wind.
parser.add_argument('-w', '--wind', action='store_true',
                    help='Enable wind mode')

args = parser.parse_args()

TOGGLE_HUMAN_MODE = args.human
"""
A constant that toggles the state of the agent mode.

This constant is used to toggle between the human mode and the agent mode. 
The value 'True' indicates that the human mode is active, while the value
'False' indicates that the agent mode is active.
"""

WIND = args.wind
"""
A constant that toggles the state of the wind.
"""

def wind(self):
    '''
    wind: Sets the ball in the up and right direction by 3 pixles every single ram step
    to simulate the effect of wind
    '''
    ram = self.get_ram()
    ball_x = ram[16] - 2
    #ball_y isn't always stable, as the ball bounces in some situations
    ball_y = 189 - ram[54]
    #shadow x is always the same as ball_x
    #this ankers the ball when bouncing
    shadow_anker = ram[15]
    shadow_y = 189 - ram[55]
    
        
    #movement up and right - noth-east wind direction stays the same so no indication is needed
    new_ball_x = ball_x + 3 # moves the ball to the right one position every ram step
    new_ball_y = ball_y + 3 # moves the ball up one position every ram step
    new_shadow_y  = shadow_y + 3
    #first part makes sure ball only moves in the air, not if bouncing on the line
    #as ram manipualtion fails when bouncing
    #second part makes sure the ball stops moving when it exits the visible field
    #in the x position to not loop the ram around
    if (ball_y < 140 and ball_y > 10) and (shadow_anker < 140 and shadow_anker > 10) and (ball_x > 2 and ball_x < 155):
        self.set_ram(16, new_ball_x)
        self.set_ram(54, new_ball_y)
        self.set_ram(55, new_shadow_y)

class WindTennis(OCAtari):
    '''
    WindTennis: Modifies the Atari game "Tennis" to simulate windforce on the tennisball, adding an additional difficulty 
    to the game.
    '''

    def __init__(self, env_name="Tennis", mode="raw", hud=False, obs_mode="dqn", *args, **kwargs):
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
        if WIND:
            wind(self)



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

class WindTennisHuman(OCAtari): 
    '''
    WindTennisHuman: Enables human play mode for the WindTennis game.
    '''

    env: gym.Env

    def __init__(self, env_name: str):
        '''
        Initializes the WindTennisHuman environment with the specified environment name.
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
        run: Runs the WindTennis environment, allowing human interaction with the game.
        '''
        self.running = True
        while self.running:
            self._handle_user_input()
            if not self.paused:
                action = self._get_action()
                # Change RAM value for human mode
                if WIND:
                    wind(self.env)

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
        _handle_user_input: Handles user input for the WindTennisHuman environment.
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
    renderer = WindTennisHuman('Tennis')
    renderer.run()
else:
    env = WindTennis(render_mode="human")
    # The following path to the agent has to be modified according to individual user setup
    # and folder names
    dqn_agent = load_agent("../OC_Atari/models/Tennis/dqn.gz", env.action_space.n)
    env.reset()
    # Let the agent play the game for 10000 steps
    for i in range(10000):
        action = dqn_agent.draw_action(env.dqn_obs)
        _, _, done1, done2, _ = env.step(action)
        sleep(0.01)
        if done1 or done2:
            env.reset()
