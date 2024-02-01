'''
no_power_pill_ms_pacman.py implements an altered version of Ms. Pacman,
in which only a choosen number of the power pills is enabled. 
'''

from time import sleep
import torch
import cv2
import pygame
import numpy as np
import gymnasium as gym
from ocatari.core import OCAtari, DEVICE
from ocatari.utils import parser, load_agent

parser.add_argument("-n", "--number", default=0, type=int,
    help="Argument for enabiling a certain number of power pills")
parser.add_argument("-hu", "--human", default=False, type=bool, 
    help="Argument for enabling (True) or disabling (False) human play mode")
opts = parser.parse_args()

TOGGLE_HUMAN_MODE = opts.human

'''
A constant that toggles the state of the play mode.

This constant is used to toggle between the human mode and the agent mode. 
The value 'True' indicates that the human mode is active, while the value
'False' indicates that the agent mode is active.
'''

NUMBER = opts.number

'''
A constant that toggles the number of power pills to be enabeld.

NUM = 0: All power pills are deleted.
NUM = 1: Expect one, all power pills are deleted.
NUM = 2: Expect two, all  power pills are deleted.
NUM = 3: Expect one, all  power pills are enabled.
NUM = 4: All power pills are enabled.

'''

class NoPowerPillMsPacman(OCAtari):
    '''
    NoPowerPillMsPacman: Modifies the Atari game "Ms. Pacman" such that only a certain
    number of power pills is enabled. The number is specified via the command line.
    '''

    def __init__(self, env_name="MsPacman", mode="revised",
                 hud=True, obs_mode="dqn", *args, **kwargs):
        '''
        Initializes an OCAtari game environment with preset values for game name, mode, and 
        observation mode. The Heads-Up Display (HUD) is enabled by default.

        is_at_start: a bool used as a switch to determine if the game was reset.
        '''
        self.render_mode = kwargs["render_mode"] if "render_mode" in kwargs else None
        # Call __init__ to create the OCAtari environment
        super().__init__(env_name, mode, hud, obs_mode, *args, **kwargs)
        self.is_at_start = True # enable switch
        

    def alter_ram(self):
        '''
        alter_ram: Manipulates the RAM cell at position 117 (= power pills), 
        62 and 95 (= edible tokens). Thus resulting in switching the specified
        number of power pills with normal edible tokens.

        is_at_start: a bool used as a switch to determine if the game was reset.
        current_lives: an integer used to store the current number of lives of Ms. Pacman
        '''
        current_lives = self.get_ram()[123]
        current_pp_status = self.get_ram()[117]
        # only do this at the start of each game
        if (current_lives == 2 and self.is_at_start) or (current_pp_status == 63):
            self.is_at_start = False # disable switch
            if NUMBER == 0: # no power pills
                self.set_ram(62, 80)
                self.set_ram(95, 80)
                self.set_ram(117, 0)
            elif NUMBER == 1: # 1 power pill
                self.set_ram(62, 64)
                self.set_ram(95, 80)
                self.set_ram(117, 8)
            elif NUMBER == 2: # two power pills
                self.set_ram(62, 0)
                self.set_ram(95, 80)
                self.set_ram(117, 40)
            elif NUMBER == 3: # three power pills
                self.set_ram(62, 0)
                self.set_ram(95, 64)
                self.set_ram(117, 46)
        # check if switch needs to be reset
        if current_lives == 1 and self.is_at_start is False:
            self.is_at_start = True # enable switch

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

class NoPowerPillMsPacmanHuman(OCAtari):
    '''
    NoPowerPillMsPacmanHuman: Enables human play mode for the NoPowerPillMsPacman game.
    Modifies the Atari game "Ms. Pacman" such that only a certain number of power pills
    is enabled. The number is specified via the command line.
    '''

    env: gym.Env

    def __init__(self, env_name: str):
        '''
        Initializes the NoPowerPillMsPacmanHuman environment with the specified environment name.

        is_at_start: a bool used as a switch to determine if the game was reset.
        '''
        self.env = OCAtari(env_name, mode="revised", hud=True, render_mode="human",
                        render_oc_overlay=True, frameskip=1)
        self.env.reset()
        self.env.render()  # Initialize the pygame video system

        self.paused = False
        self.current_keys_down = set()
        self.keys2actions = self.env.unwrapped.get_keys_to_action()

        self.is_at_start = True

    def run(self):
        '''
        run: Runs the NoPowerPillMsPacmanHuman environment, allowing human interaction
        with the game. Manipulates the RAM cell at position 117 (= power pills), 
        62 and 95 (= edible tokens). Thus resulting in switching the specified
        number of power pills with normal edible tokens.

        is_at_start: a bool used as a switch to determine if the game was reset.
        current_lives: an integer used to store the current number of lives of Ms. Pacman
        '''
        self.running = True
        while self.running:
            self._handle_user_input()
            if not self.paused:
                action = self._get_action()
                current_lives = self.env.get_ram()[123]
                current_pp_status = self.env.get_ram()[117]
                # only do this at the start of each game
                if (current_lives == 2 and self.is_at_start) or (current_pp_status == 63):
                    self.is_at_start = False # disable switch
                    if NUMBER == 0: # no power pills
                        self.env.set_ram(62, 80)
                        self.env.set_ram(95, 80)
                        self.env.set_ram(117, 0)
                    elif NUMBER == 1: # one power pill
                        self.env.set_ram(62, 64)
                        self.env.set_ram(95, 80)
                        self.env.set_ram(117, 8)
                    elif NUMBER == 2: # two power pills
                        self.env.set_ram(62, 0)
                        self.env.set_ram(95, 80)
                        self.env.set_ram(117, 40)
                    elif NUMBER == 3: # three power pills
                        self.env.set_ram(62, 0)
                        self.env.set_ram(95, 64)
                        self.env.set_ram(117, 46)
                # check if switch needs to be reset
                if current_lives == 1 and self.is_at_start is False:
                    self.is_at_start = True # enable switch
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
        _handle_user_input: Handles user input for the NoPowerPillMsPacmanHuman environment.
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
    renderer = NoPowerPillMsPacmanHuman('MsPacman')
    renderer.run()
else:
    env = NoPowerPillMsPacman(render_mode="human")
    # The following path to the agent has to be modified according to individual user setup
    # and folder names
    dqn_agent = load_agent("/home/keeki/Schreibtisch/HackAtari/OC_Atari/models/MsPacman/dqn.gz",
                            env.action_space.n)
    env.reset()

    # Let the agent play the game for 10000 steps
    for i in range(10000):
        action = dqn_agent.draw_action(env.dqn_obs)
        _, _, done1, done2, _ = env.step(action)
        sleep(0.01)
        if done1 or done2:
            env.reset()
