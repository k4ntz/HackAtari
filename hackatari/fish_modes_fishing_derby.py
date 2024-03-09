'''
fish_modes_fishing_derby.py implements an altered version of FishingDerby in which
the behavior of the fish can be changed in various ways. 
The player can choose between the following modes for the fish:
- 0 = default. No modifications regarding the fish.
- 1 = The x-position of the fish is changed. They are mainly on the player's side.
- 2 = The x-position of the fish is changed. They are mainly on the enemy's side.
- 3 = The x-position of the fish is changed. They are in the middle betwen 
      player and enemy.
'''

from time import sleep
from termcolor import colored
import torch
import cv2
import pygame
import numpy as np
import gymnasium as gym
from ocatari.core import OCAtari, DEVICE
from ocatari.utils import parser, load_agent


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

FISH_MODE = opts.fishmode
"""
A constant used to change the mode for the fish.
"""
if FISH_MODE < 0 or FISH_MODE > 3:
    print(colored('Illegal input value for fish mode. The value has to be between 0 and 3.' +
                   'Continuing with default value 0.', 'red'))
    FISH_MODE = 0
    

class FishModeFishingDerby(OCAtari):
    '''
    FishModeFishingDerby: Modifies the Atari game "FishingDerby" such that the fish can 
    be manipulated.
    '''
    def __init__(self, env_name="FishingDerby", mode="revised",
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
        The x-position of the fish is stored in RAM cell 69-74.
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

class FishModeFishingDerbyHuman(OCAtari):
    '''
    FishModeFishingDerbyHuman: Enables human play mode for the FishModeFishingDerby game.
    '''

    env: gym.Env

    def __init__(self, env_name: str):
        '''
        Initializes the FishModeFishingDerbyHuman environment with the specified environment 
        name.
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
        run: Runs the FishModeFishingDerbyHuman environment, allowing human interaction
        with the game.
        '''
        self.running = True
        while self.running:
            self._handle_user_input()
            if not self.paused:
                action = self._get_action()
                
                # fish modes
                if FISH_MODE > 0:
                    # fish mode 1: fish are all on player's side
                    if FISH_MODE == 1:
                        for i in range(6):
                            if self.env.get_ram()[69+i] > 86:
                                self.env.set_ram(69+i, 44)
                    # fish mode 2: fish are all on enemy's side
                    if FISH_MODE == 2:
                        for i in range(6):
                            if self.env.get_ram()[69+i] < 70:
                                self.env.set_ram(69+i, 116)
                    # fish mode 3: fish are always in the middle between player and enemy
                    if FISH_MODE == 3:
                        for i in range(6):
                            if self.env.get_ram()[69+i] < 70:
                                self.env.set_ram(69+i, 86)
                            if self.env.get_ram()[69+i] > 86:
                                self.env.set_ram(69+i, 70)
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
        _handle_user_input: Handles user input for the FishModeFishingDerbyHuman environment.
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
    renderer = FishModeFishingDerbyHuman('FishingDerby')
    renderer.run()
else:
    env = FishModeFishingDerby(render_mode="human")
    # The following path to the agent has to be modified according to individual user setup
    # and folder names
    dqn_agent = load_agent("/home/keeki/Schreibtisch/HackAtari/OC_Atari/models/FishingDerby/dqn.gz",
                            env.action_space.n)
    env.reset()

    # Let the agent play the game for 10000 steps
    for i in range(10000):
        action = dqn_agent.draw_action(env.dqn_obs)
        _, _, done1, done2, _ = env.step(action)
        sleep(0.01)
        if done1 or done2:
            env.reset()
