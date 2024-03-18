"""
This module provides an enhanced gaming experience for the Atari game "Frostbite".
The following additions have been added:
- the option to relocate the ice floes
- the option to change the number of enemies
- the option to change the game colors
- the option to change the UI colors

"""
from time import sleep
from termcolor import colored
import torch
import cv2
import pygame
import numpy as np
import gymnasium as gym
import argparse
from ocatari.core import OCAtari, DEVICE
from ocatari.utils import load_agent

# Set up the argument parser for the Frostbite game modifications.
# This allows players to customize their gameplay experience through command-line options.
parser = argparse.ArgumentParser(description='Fristbite Game Argument Setter')

# Parser arguments for color value inputs.
parser.add_argument("-c", "--color", default=12, type=int,
                     help="Argument for setting the color of line 1 of the ice floes." +
                     " The chosen value has to be between 0 and 255. The default value is 12" +
                     " = white."
                     )

# Parser arguments for choosing lines to recoloring.
parser.add_argument("-l", "--line", default=1, type=int,
                    help="Argument for choosing a line of ice floes for color changing." +
                    " The chosen value has to be between 1 and 4. The dedault value is 1."
                    )

# Parser argument for enbaling or disabling human mode.
parser.add_argument("-hu", "--human", action='store_true',
                     help="Argument for enabling human play mode")

# Parser argument for enabling the 3 color change mode.
parser.add_argument("-c3", "--color3", action='store_true',
                     help="Argument for enabling the 3 color mode." +
                     "This mode recolors 3 lines at once.")

# Parser arguments for ui color value inputs.
parser.add_argument("-cui", "--colorui", default=0, type=int,
                     help="Argument for setting the color of the UI for temperature, life and points." +
                     " The chosen value has to be between 6 and 254. The default value is 0" +
                     " = white."
                     )

# Parser argument for enbaling positional changes to the floes.
parser.add_argument("-cfp", "--change-floes-position", action='store_true',
                     help="Argument for enabling position changes to the floes.")

# Parser argument for setting the new x value.
parser.add_argument("-fp", "--floes-position", default=100, type=int,
                     help="Argument for setting the x-position of the ice floes." +
                        " The input value has to be between 0 and 255."
                     )

# Parser argument for changing enemies number
parser.add_argument("-en", "--number-enemies", default=0, type=int,
                     help="Argument for changing the enemies number."
                     + "The value has to be between 0 and 3."
                     +" 0 is the unaltered version.")

opts = parser.parse_args()

TOGGLE_HUMAN_MODE = opts.human
"""
A constant that toggles the state of the agent mode.

This constant is used to toggle between the human mode and the agent mode. 
The value 'True' indicates that the human mode is active, while the value
'False' indicates that the agent mode is active.
"""

COLOR_VALUE = opts.color
if COLOR_VALUE < 0 or COLOR_VALUE > 255:
    print(colored('Illegal input for color value. Color value has to be between 0 and 255.' +
                   'Continuing with default color value 12.', 'red'))
    COLOR_VALUE = 12
"""
A constant for setting the desired color for the ice floes based on user input."""

TOGGLE_LINE = opts.line
if TOGGLE_LINE < 0 or TOGGLE_LINE > 4:
    print(colored('Illegal input for line number. Line number has to be between 1 and 4.' +
                   'Continuing with default color value 1.', 'red'))
"""
A constant for choosing the line of ice floes to recolor.
"""

TOGGLE_3C = opts.color3
"""
A constant for enabling or disabling the 3 color mode which recolors 3 lines at once.
"""

COLOR_VALUE_UI = opts.colorui
if COLOR_VALUE_UI in range(1,6) or COLOR_VALUE_UI > 254:
    print(colored('Illegal input for color value. Color value has to be between 6 and 254.' +
                   'Continuing with default color value 0.', 'red'))
    COLOR_VALUE_UI = 0
"""
A constant for setting the desired color for the UI based on user input.
"""

POSITION_CHANGES_ENABLED = opts.change_floes_position
"""
A constant that stores true if the position change mode is enabled.
"""

NEW_X_POS = opts.floes_position
"""
A constant that stores the new x-position for the ice floes.
"""
if NEW_X_POS < 0 or NEW_X_POS > 255:
    print(colored('Illegal input for x position. The value for x has to be between 0 and 255.' +
                   ' Continuing with default x value 100.', 'red'))
    NEW_X_POS = 100

ENEMIES_NUMBER = opts.number_enemies
"""
A constant used to change the mode for the number of enemies.
"""
def change_colors(self):
    '''
    Adjusts the colors of the ice floes bases on the specified values.
    '''
    if TOGGLE_3C:
        self.set_ram(44, COLOR_VALUE)
        self.set_ram(45, COLOR_VALUE)
        self.set_ram(46, COLOR_VALUE)
    else:
        if TOGGLE_LINE == 4:
            self.set_ram(43, COLOR_VALUE)
        if TOGGLE_LINE == 3:
            self.set_ram(44, COLOR_VALUE)
        if TOGGLE_LINE == 2:
            self.set_ram(45, COLOR_VALUE)
        if TOGGLE_LINE == 1:
            self.set_ram(46, COLOR_VALUE)

def alter_ui_color(self):
    '''
    Adjusts the colors of the ui bases on the specified values.
    '''
    self.set_ram(71, COLOR_VALUE_UI)

def relocate_floes(self):
    '''
    Adjusts the memory based on the specified new position of the ice floes.
    '''
    self.set_ram(22, 0)
    self.set_ram(31, NEW_X_POS)
    self.set_ram(32, NEW_X_POS)
    self.set_ram(33, NEW_X_POS)
    self.set_ram(34, NEW_X_POS)

def adjust_enemies(self):
    '''
    Adjusts the memory based on the specified number of enemies selected by the user.
    '''
    if ENEMIES_NUMBER > 0:
        # enemies number 1: easy mode with 0 enemies
        if ENEMIES_NUMBER == 1:
            value = 0
        # enemies number 2: medium mode with 8 enemies
        elif ENEMIES_NUMBER == 2:
            value = 5
        # enemies number 3: medium mode with 12 enemies
        elif ENEMIES_NUMBER == 3:
            value = 15
        for rows in range(92, 96):
            self.set_ram(rows, value)

class ColorChangedFrostbite(OCAtari):
    '''
    ColorChangedFrostbite: Modifies the Atari game "Frostbite" such that a line of ice floes
    can be recolored based on user input.
    '''
    def __init__(self, env_name="Frostbite", mode="ram",
                 hud=True, obs_mode="dqn", *args, **kwargs):
        '''
        Initializes an OCAtari game environment with preset values for game name, mode, and 
        observation mode. The Heads-Up Display (HUD) is enabled by default.
        '''
        self.render_mode = kwargs["render_mode"] if "render_mode" in kwargs else None
        # Call __init__ to create the OCAtari environment
        super().__init__(env_name, mode, hud, obs_mode, *args, **kwargs)

    def alter_ram(self):
        '''
        alter_ram: Manipulates the RAM.
        '''
        change_colors(self)
        alter_ui_color(self)
        adjust_enemies(self)
        if POSITION_CHANGES_ENABLED:
            relocate_floes(self)


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

class ColorChangedFrostbiteHuman(OCAtari):
    '''
    ColorChangedFrostbiteHuman: Enables human play mode for the ColorChangedFrostbite game.
    '''

    env: gym.Env

    def __init__(self, env_name: str):
        '''
        Initializes the ColorChangedFrostbiteHuman environment with the specified environment name.
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
        run: Runs the ColorChangedFrostbiteHuman environment, allowing human interaction
        with the game.
        '''
        self.running = True
        while self.running:
            self._handle_user_input()
            if not self.paused:
                action = self._get_action()
                # Change RAM value here
                change_colors(self.env)
                alter_ui_color(self.env)
                adjust_enemies(self.env)
                if POSITION_CHANGES_ENABLED:
                    relocate_floes(self.env)
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
        _handle_user_input: Handles user input for the ColorChangedFrostbiteHuman environment.
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
    renderer = ColorChangedFrostbiteHuman('Frostbite')
    renderer.run()
else:
    env = ColorChangedFrostbite(render_mode="human")
    # The following path to the agent has to be modified according to individual user setup
    # and folder names
    dqn_agent = load_agent("../OC_Atari/models/Frostbite/dqn.gz",
                            env.action_space.n)
    env.reset()

    # Let the agent play the game for 10000 steps
    for i in range(10000):
        action = dqn_agent.draw_action(env.dqn_obs)
        _, _, done1, done2, _ = env.step(action)
        sleep(0.01)
        if done1 or done2:
            env.reset()
