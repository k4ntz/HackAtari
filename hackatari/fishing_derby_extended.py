"""
This module provides an enhanced gaming experience for the Atari game "Fishing Derby".
The following additions have been added:
- options for the behavior of the shark
- options for the behavior of the fish


"""

from time import sleep
from termcolor import colored
import torch
import cv2
import pygame
import numpy as np
import gymnasium as gym
from ocatari.core import OCAtari, DEVICE
from ocatari.utils import parser, load_agent


# Parser argument for enbaling or disabling human mode.
parser.add_argument("-sm", "--sharkmode", default=0, type=int,
                     help="Argument for changing the shark mode. The value has to be between 0"
                     +"  and 4. 0 is the unaltered version.")

# Parser argument for changing the fish
parser.add_argument("-fm", "--fishmode", default=0, type=int,
                     help="Argument for changing the fish mode. The value has to be between 0-3."
                     +" 0 is the unaltered version.")

# Parser argument for enbaling or disabling human mode.
parser.add_argument("-hu", "--human", default=False, type=bool,
                     help="Argument for enabling (True) or disabling (False) human play mode")

opts = parser.parse_args()

TOGGLE_HUMAN_MODE = opts.human
"""
A constant that toggles the state of the agent mode.

This constant is used to toggle between the human mode and the agent mode. 
The value 'True' indicates that the human mode is active, while the value
'False' indicates that the agent mode is active.
"""

SHARK_MODE = opts.sharkmode
"""
A constant used to change the shark mode.
The player can choose between the following modes for the shark:
- 0 = default. No modifications regarding the shark.
- 1 = x-position of the shark is fixed at 105, which is directly below the enemy player
- 2 = x-position of the shark is fixed at 25, which is directly below the player
- 3 = the shark teleports from the left to the right and the other way around when
      x-position 25 or 105 is reached
- 4 = the shark moves from the left to the right with a very high velocity. When
      reaching x-position 120 the shark is set back to x-position 1 and starts to
      move again in the same speed up way as described.
"""
if SHARK_MODE < 0 or SHARK_MODE > 4:
    print(colored('Illegal input for shark mode value. The value has to be between 0 and 4.' +
                   'Continuing with default value 0.', 'red'))
    SHARK_MODE = 0

FISH_MODE = opts.fishmode
"""
A constant used to change the mode for the fish.
The player can choose between the following modes for the fish:
- 0 = default. No modifications regarding the fish.
- 1 = The x-position of the fish is changed. They are mainly on the player's side.
- 2 = The x-position of the fish is changed. They are mainly on the enemy's side.
- 3 = The x-position of the fish is changed. They are in the middle betwen 
      player and enemy.
"""
if FISH_MODE < 0 or FISH_MODE > 3:
    print(colored('Illegal input value for fish mode. The value has to be between 0 and 3.' +
                   'Continuing with default value 0.', 'red'))
    FISH_MODE = 0

def alter_shark(self):
    '''
    alter_shark: Allows for alterations in the behavior of the shark as specified
    by the corresponding command line option
    '''
    # shark modes
    if SHARK_MODE > 0:
        # shark mode: no movement easy
        if SHARK_MODE == 1:
            self.set_ram(75, 105)
        # shark mode: no movement hard
        if SHARK_MODE == 2:
            self.set_ram(75, 25)
        # shark mode: teleport
        if SHARK_MODE == 3:
            current_x_position = self.get_ram()[75]
            if current_x_position == 100:
                self.set_ram(75, 25)
            if current_x_position == 30:
                self.set_ram(75, 105)
        # shark mode: speed mode
        if SHARK_MODE == 4:
            current_x_position = self.get_ram()[75]
            if current_x_position < 120:
                self.set_ram(75, current_x_position+5)
            if current_x_position > 120:
                self.set_ram(75, 1)

def alter_fish(self):
    '''
    alter_fishes: Allows for alterations in the behavior of the fish as specified
    by the corresponding command line option
    '''
    # fish modes
    if FISH_MODE > 0:
        # fish mode 1: fish are all on player's side
        if FISH_MODE == 1:
            for i in range(6):
                if self.get_ram()[69+i] > 86:
                    self.set_ram(69+i, 44)
        # fish mode 2: fish are all on enemy's side
        if FISH_MODE == 2:
            for i in range(6):
                if self.get_ram()[69+i] < 70:
                    self.set_ram(69+i, 116)
        # fish mode 3: fish are always in the middle between player and enemy
        if FISH_MODE == 3:
            for i in range(6):
                if self.get_ram()[69+i] < 70:
                    self.set_ram(69+i, 86)
                if self.get_ram()[69+i] > 86:
                    self.set_ram(69+i, 70)


class SharkModesFishingDerby(OCAtari):
    '''
    SharkModesFishingDerby: Modifies the Atari game "FishingDerby" such that the shark can be
    manipulated.
    '''
    def __init__(self, env_name="FishingDerby", mode="ram",
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
        alter_shark(self)
        alter_fish(self)


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

class SharkModesFishingDerbyHuman(OCAtari):
    '''
    SharkModesFishingDerbyHuman: Enables human play mode for the SharkModesFishingDerby game.
    '''

    env: gym.Env

    def __init__(self, env_name: str):
        '''
        Initializes the SharkModesFishingDerbyHuman environment with the specified environment 
        name.
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
        run: Runs the SharkModesFishingDerbyHuman environment, allowing human interaction
        with the game.
        '''
        self.running = True
        while self.running:
            self._handle_user_input()
            if not self.paused:
                action = self._get_action()
                # Change RAM value here
                alter_fish(self.env)
                alter_shark(self.env)
                # end of RAM changes
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
        _handle_user_input: Handles user input for the SharkModesFishingDerbyHuman environment.
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
    renderer = SharkModesFishingDerbyHuman('FishingDerby')
    renderer.run()
else:
    env = SharkModesFishingDerby(render_mode="human")
    # The following path to the agent has to be modified according to individual user setup
    # and folder names
    dqn_agent = load_agent("../OC_Atari/models/FishingDerby/dqn.gz",
                            env.action_space.n)
    env.reset()

    # Let the agent play the game for 10000 steps
    for i in range(10000):
        action = dqn_agent.draw_action(env.dqn_obs)
        _, _, done1, done2, _ = env.step(action)
        sleep(0.01)
        if done1 or done2:
            env.reset()
