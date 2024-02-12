'''
edible_ghosts_ms_pacman.py implements an altered version of Ms. Pacman,
in which all four ghosts are edible the entire game. 
'''

from time import sleep
import torch
import cv2
import pygame
import numpy as np
import gymnasium as gym
from ocatari.core import OCAtari, DEVICE
from ocatari.utils import parser, load_agent

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

def make_edible(env,ghost_number,  x_pos, ram_x, y_pos, ram_y):
    ''' A helper function to make a certain ghost edible.
    The position is changed as well to avoid glitches.
    ghost_number: integer between 1 and 4 to choose between the 4 ghosts
    ram_x: integer which defines the ram cell in which the x-position is saved
    x_pos: integer which defines the new x-position of the ghost
    ram_y: integer which defines the ram cell in which the y-position is saved
    y_pos: integer which defines the new y-position of the ghost
    '''
    env.set_ram(ghost_number, 130)
    env.set_ram(ram_x, x_pos)
    env.set_ram(ram_y, y_pos)

def set_start_condition(self):
    ''' A helper function to set the start condition at the beginning of 
    each level/ after a reset'''
    # remove power pills
    self.set_ram(62, 80)
    self.set_ram(95, 80)
    self.set_ram(117, 0)
    # set the ghost to "edible" and change start location to avoid glitches
    # orange ghost
    make_edible(self, 1, 120, 6, 50, 12) 
    # cyan ghost
    make_edible(self, 2, 100, 7, 50, 13)
    # pink ghost
    make_edible(self, 3, 80, 8, 50, 14)
    # red ghost
    make_edible(self, 4, 60 ,9, 50, 15)
    # set the timer to max number
    self.set_ram(116, 255)


class EdibleGhostsMsPacman(OCAtari):
    '''
    EdibleGhostsMsPacman: Modifies the Atari game "Ms. Pacman" such that the four ghost
    are edible the entire game and all power pills are switched with normal edible tokens.
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
        62 and 95 (= edible tokens). Thus resulting in switching all power pills with 
        normal edible tokens.
        Furthermore all ghost will be made edible the entire game using RAM cell 1-4 
        (= ghost status) and the timer for the edible ghost mode (RAM cell 116)

        is_at_start: a bool used as a switch to determine if the game was reset.
        current_lives: an integer used to store the current number of lives of Ms. Pacman
        current_pp_status: an integer used to store the current status of the power pills
        current_timer: an integer used to store the current timer of the edible ghost mode
        current_orange: an integer used to store the current status of the orange ghost
        current_cyan: an integer used to store the current status of the orange ghost
        current_pink: an integer used to store the current status of the pink ghost
        current_red: an integer used to store the current status of the red ghost
        '''
        current_lives = self.get_ram()[123]
        current_pp_status = self.get_ram()[117]
        current_timer = self.get_ram()[116]

        current_orange = self.get_ram()[1]
        current_cyan = self.get_ram()[2]
        current_pink = self.get_ram()[3]
        current_red = self.get_ram()[4]
        
        # only do this at the start of each game
        if (current_lives == 2 and self.is_at_start):
            self.is_at_start = False # disable switch
            set_start_condition(self)

        # only do this at the beginning of a new level
        # RAM cell 0 can't be used to extract the current level,
        # but the game will reset the power pills at each new level
        if current_pp_status == 63:
            self.is_at_start = False # disable switch
            set_start_condition(self)

        # check if switch needs to be reset
        if current_lives == 1 and self.is_at_start is False:
            self.is_at_start = True # enable switch

        # check if timer needs to be adjusted
        if current_timer < 250:
            self.set_ram(116, 255)

        # check if a ghost has been eaten and if needed make them edible again
        # change start location to avoid glitches
        if current_orange == 112:
            make_edible(self, 1, 120, 6, 50, 12)
        if current_cyan == 112:
            make_edible(self, 2, 100, 7, 50, 13)
        if current_pink == 112:
            make_edible(self, 3, 80, 8, 50, 14)
        if current_red == 112:
            make_edible(self, 4, 60 ,9, 50, 15)
           
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

class EdibleGhostsMsPacmanHuman(OCAtari):
    '''
    EdibleGhostsMsPacmanHuman: Enables human play mode for the EdibleGhostsMsPacman game.
    Modifies the Atari game "Ms. Pacman" such that the four ghost
    are edible the entire game and all power pills are switched with normal edible tokens.
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
        with the game. alter_ram: Manipulates the RAM cell at position 117 (= power pills), 
        62 and 95 (= edible tokens). 
        Thus resulting in switching all power pills with normal edible tokens.
        Furthermore all ghost will be made edible the entire game using RAM cell 
        1-4 (= ghost status) and the timer for the edible ghost mode (RAM cell 116)

        is_at_start: a bool used as a switch to determine if the game was reset.
        current_lives: an integer used to store the current number of lives of Ms. Pacman
        current_pp_status: an integer used to store the current status of the power pills
        current_timer: an integer used to store the current timer of the edible ghost mode
        current_orange: an integer used to store the current status of the orange ghost
        current_cyan: an integer used to store the current status of the orange ghost
        current_pink: an integer used to store the current status of the pink ghost
        current_red: an integer used to store the current status of the red ghost
        '''
        self.running = True
        while self.running:
            self._handle_user_input()
            if not self.paused:
                action = self._get_action()
                current_lives = self.env.get_ram()[123]
                current_timer = self.env.get_ram()[116]
                current_pp_status = self.env.get_ram()[117]
                current_orange = self.env.get_ram()[1]
                current_cyan = self.env.get_ram()[2]
                current_pink = self.env.get_ram()[3]
                current_red = self.env.get_ram()[4]

                # only do this at the start of each game
                if (current_lives == 2 and self.is_at_start):
                    self.is_at_start = False # disable switch
                    set_start_condition(self.env)

                 # only do this at the beginning of a new level
                 # RAM cell 0 can't be used to extract the current level,
                 # but the game will reset the power pills at each new level 
                if current_pp_status == 63:
                    self.is_at_start = False # disable switch
                    set_start_condition(self.env)

                # check if switch needs to be reset
                if current_lives == 1 and self.is_at_start is False:
                    self.is_at_start = True # enable switch

                # check if timer needs to be adjusted
                if current_timer < 250:
                    self.env.set_ram(116, 255)

                # check if a ghost has been eaten and if needed make them edible again
                # change start location to avoid glitches
                if current_orange == 112:
                    make_edible(self.env, 1, 120, 6, 50, 12)
                if current_cyan == 112:
                    make_edible(self.env, 2, 100, 7, 50, 13)
                if current_pink == 112:
                    make_edible(self.env, 3, 80, 8, 50, 14)
                if current_red == 112:
                    make_edible(self.env, 4, 60 ,9, 50, 15)
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
        _handle_user_input: Handles user input for the EdibleGhostsMsPacmanHuman environment.
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
    renderer = EdibleGhostsMsPacmanHuman('MsPacman')
    renderer.run()
else:
    env = EdibleGhostsMsPacman(render_mode="human")
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
