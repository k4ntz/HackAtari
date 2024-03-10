"""
This module provides an enhanced gaming experience for the Atari game "Space Invaders".
The following additions have been added:
- A version where the shots travel on a curved path
- Disable the shields
- Relocate the shields
"""

from time import sleep
import argparse
import torch
import cv2
import pygame
import numpy as np
import gymnasium as gym
from ocatari.core import OCAtari, DEVICE
from ocatari.utils import load_agent
from termcolor import colored

# Set up the argument parser for the Space Invaders game modifications.
# This allows players to customize their gameplay experience through command-line options.
parser = argparse.ArgumentParser(description='Space Invaders Game Argument Setter')


parser.add_argument("-pos", "--position", default=43, type=int,
                     help="Argument for setting the offset of the shield position." +
                     " The positional anchor is the left corner of the left shield with position 0."
                     +" The chosen number has to be between 35 and 53.")

# Argument to disable all the shields.
# When set, all the shields will be disabled and stop providing protection for the player.
parser.add_argument('-ds', '--disable-shields', action='store_true',
                    help='Disable all the shields.')

# Argument to disable the shields selectivly.
parser.add_argument("-l", "--left", action='store_true', help="Argument for enabling (1) or disabling (0) the left shield.")
parser.add_argument("-m", "--middle", action='store_true', help="Argument for enabling (1) or disabling (0) the shield in the middle")
parser.add_argument("-r", "--right", action='store_true', help="Argument for enabling (1) or disabling (0) the right shield")

# Argument to enable curved shots.
# When set, the shots will follow a curved path instead of a straight.
parser.add_argument('-c', '--curved', action='store_true',
                    help='Enable curved shots.')


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


CURVED_SHOTS = args.curved
"""
CURVED_SHOTS controls the path the shots take.
When set to True via the '--curved' argument, the shots follow a curved path.
"""

NO_SHIELDS = args.disable_shields
"""
NO_SHIELDS controls the presence of shields. 
When set to True via the '--disable-shields' argument, the shields are disabled.
"""

LEFT = args.left
RIGHT = args.right
MIDDLE = args.middle
"""
LEFT, RIGHT, and MIDDLE control the presence of the respective shields one by one.
"""

SHIELD_POSITION_OFFSET = args.position
if SHIELD_POSITION_OFFSET > 53 or SHIELD_POSITION_OFFSET < 35:
    print(colored('Illegal input for shield position offset. Shield position offset has to be' +
                   'between 35 and 53... Continuing with default position 43.', 'red'))
    SHIELD_POSITION_OFFSET = 43
"""
A Constant that determines the offset which is used to relocate the shields. A check is used to intercept illegal input values. If illegal values are used
a error message is displayed and the game is run using the default shield position as seen in the original game setup.
"""


'''
The following methods allow for disabling the shields selectivly and all together.
'''
def disable_shield_left(self):
    '''
    disable_shield_left: Disables the left shield.
    '''
    shield_status_left = self.get_ram()[43:52]
    if LEFT or NO_SHIELDS:
        for i in range(len(shield_status_left)):
            shield_status_left[i] = 0
            self.set_ram(i+43,shield_status_left[i])

def disable_shield_middle(self):
    '''
    disable_shield_middle: Disables the middle shield.
    '''
    shield_status_middle = self.get_ram()[52:61]
    if MIDDLE or NO_SHIELDS:
        for i in range(len(shield_status_middle)):
            shield_status_middle[i] = 0
            self.set_ram(i+52, shield_status_middle[i])

def disable_shield_right(self):
    '''
    disable_shield_right: Disables the right shield.
    '''
    shield_status_right = self.get_ram()[61:71]
    if RIGHT or NO_SHIELDS:
        for i in range(len(shield_status_right)):
            shield_status_right[i] = 0
            self.set_ram(i+61, shield_status_right[i])

def disable_all_shields(self):
    '''
    disable_all_shields: Disables all the shields at once.
    '''
    if NO_SHIELDS:
        disable_shield_left(self)
        disable_shield_middle(self)
        disable_shield_right(self)


def relocate_shields(self):
    '''
    relocate_shields: Allows for the relocation of the shields via an offset.
    '''
    shield_pos_new = SHIELD_POSITION_OFFSET
    if shield_pos_new < 53 and shield_pos_new >= 35:
        self.set_ram(27, shield_pos_new)

def curved_shots(self):
    '''
    curved_shots: Makes the shots travel on a curved path.
    '''
    if CURVED_SHOTS:
        curr_laser_pos = self.get_ram()[87]
        # Manipulate the value in RAM cell 87 as long as the upper and the lower threshold
        # are not reached.
        if 40 < curr_laser_pos < 122:
            laser_displacement = calculate_x_displacement(curr_laser_pos)
            self.set_ram(87, laser_displacement)

# calculates the x coordinate displacement based on a parabolic function
def calculate_x_displacement(current_x):
    '''
    calculate_x_displacement: calculates the displacement value based on a parabolic function
    and the current x position.
    '''
    if current_x < 81:
        x_out = -0.01 * current_x + current_x
    else:
        x_out = 0.01 * current_x + current_x
    x_out = int(np.round(x_out))
    return int(x_out)


class SpaceInvadersExtended(OCAtari):
    '''
    SpaceInvadersExtended: Enables agent play mode for the SpaceInvadersExtended game.
    Modifies the Atari game "Space Invaders" such that the laser shoots in 
    a parabolic fashion instead of a straight line. The direction of the shooting curve is 
    dependend of the current position on the playing field.
    '''

    def __init__(self, env_name="SpaceInvaders-v4", mode="revised",
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
        alter_ram: Manipulates the RAM cell at position 87 to shift the position of
        the laser to the left or right. The direction is dependend of the current
        position on the playing field.
        The value in the cell is continually manipulated as long as the stored RAM values 
        are inside the defined boundaries.
        '''

        curved_shots(self)
        relocate_shields(self)
        disable_all_shields(self)
        disable_shield_left(self)
        disable_shield_middle(self)
        disable_shield_right(self)

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

class SpaceInvadersExtendedHuman(OCAtari):
    '''
    SpaceInvadersExtendedHuman: Enables human play mode for the SpaceInvadersExtended game.
    '''

    env: gym.Env

    def __init__(self, env_name: str):
        '''
        Initializes the SpaceInvadersExtendedHuman environment with the specified environment name.
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
        run: Runs the SpaceInvadersExtendedHuman environment, allowing human interaction
        with the game.
        '''
        self.running = True
        while self.running:
            self._handle_user_input()
            if not self.paused:
                action = self._get_action()
                # Change RAM value
                curved_shots(self.env)
                relocate_shields(self.env)
                disable_all_shields(self.env)
                disable_shield_left(self.env)
                disable_shield_middle(self.env)
                disable_shield_right(self.env)
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
        _handle_user_input: Handles user input for the SpaceInvadersExtendedHuman environment.
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
    renderer = SpaceInvadersExtendedHuman('SpaceInvaders')
    renderer.run()
else:
    env = SpaceInvadersExtended(render_mode="human")
    # The following path to the agent has to be modified according to individual user setup
    # and folder names
    dqn_agent = load_agent("../OC_Atari/models/SpaceInvaders/dqn.gz",
                            env.action_space.n)
    env.reset()

    # Let the agent play the game for 10000 steps
    for i in range(10000):
        action = dqn_agent.draw_action(env.dqn_obs)
        _, _, done1, done2, _ = env.step(action)
        sleep(0.01)
        if done1 or done2:
            env.reset()
