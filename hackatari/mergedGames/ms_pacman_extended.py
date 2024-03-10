'''
This module provides an enhanced gaming experience for the Atari game "Ms Pacman".
The following additions have been added:
- the ability to set ghosts to static
- the ability to disable the power pills selectivly
- a version of the game where ghosts can be eaten all the time
- an inverted version where eating a power pill makes the ghosts dangerous
'''

from time import sleep
import torch
import cv2
import pygame
import numpy as np
import gymnasium as gym
from ocatari.core import OCAtari, DEVICE
import argparse
from ocatari.utils import load_agent

# Set up the argument parser for the Ms Pcman game modifications.
# This allows players to customize their gameplay experience through command-line options.
parser = argparse.ArgumentParser(description='Ms Pacman Game Argument Setter')

# Argument to enable human mode.
# When set, the game will be playable by a human player instead of an AI agent.
parser.add_argument("-hu", "--human", action='store_true',
    help="Argument for enabling (True) or disabling (False) human play mode")


# Argument to set all the ghosts into caged mode.
parser.add_argument("-cg", "--caged-ghosts", action='store_true',
    help="Argument for disabling the movement of all the ghosts.")

# The following arguments allow for setting the ghosts into static mode selectivly.
parser.add_argument("-orange", "--orange",action='store_true', 
    help="Argument for disabling the movement of the orange ghost")
parser.add_argument("-cyan", "--cyan", action='store_true', 
    help="Argument for disabling the movement of the cyan ghost")
parser.add_argument("-pink", "--pink", action='store_true',
    help="Argument for disabling the movement of the pink ghost")
parser.add_argument("-red", "--red", action='store_true',
    help="Argument for disabling the movement of the red ghost")

parser.add_argument("-npp", "--number-power-pills", default=4, type=int,
    help="Argument to enable ir disable a certain number of power pills.")

# Argument to make all ghosts edible.
parser.add_argument("-eg", "--edible-ghosts", action='store_true', 
    help="Argument for making the ghosts edible all the time.")

# Argument to activate inverse ms packman mode.
parser.add_argument("-i", "--inverse", action='store_true', 
    help="Argument for inversing the game.")

args = parser.parse_args()

TOGGLE_HUMAN_MODE = args.human

'''
A constant that toggles the state of the play mode.

This constant is used to toggle between the human mode and the agent mode. 
The value 'True' indicates that the human mode is active, while the value
'False' indicates that the agent mode is active.
'''


GHOSTS_CAGED = args.caged_ghosts

'''
A constant that toggles the ghosts movement.

This constant is used to toggle between the normal mode with moving ghosts
and the static mode with caged ghosts. 
'''

TOGGLE_ORANGE = args.orange
TOGGLE_CYAN = args.cyan
TOGGLE_PINK = args.pink
TOGGLE_RED = args.red

'''
Four constants that determine which ghots are enabled or disabled.
The values are provided by parser arguments via command line.
The default is 1 for all four. Therefore all ghosts are disabled by default.
'''

NUMBER = args.number_power_pills

'''
A constant that toggles the number of power pills to be enabeld.

NUM = 0: All power pills are deleted.
NUM = 1: Expect one, all power pills are deleted.
NUM = 2: Expect two, all  power pills are deleted.
NUM = 3: Expect one, all  power pills are enabled.
NUM = 4: All power pills are enabled.

'''

EDIBLE = args.edible_ghosts
'''
A constants that allows for enabling edible ghosts mode, where the
ghosts can always be eaten without the need for power pills.
'''

INVERSE = args.inverse
'''
A constants that activetes inverse mode where the power pills now make
the ghosts dangerous.
'''

def make_edible(env, ghost_number,  x_pos, ram_x, y_pos, ram_y):
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

def inverted_power_pill(self):
    ''' A helper function to make the ghost "normal" again.
    They will be able to eat Ms. Pacman for a certain amount of time.'''
    i = 1
    while i < 5:
        # make ghosts "normal"
        self.set_ram(i, 0)
        i += 1
    # set timer    
    self.set_ram(116, 62)

def power_pill_is_done(self):
    ''' A helper function to make all ghosts edible again.'''
    i = 1
    while i < 5:
        # make ghosts edible
        self.set_ram(i, 130)
        i += 1
    # set timer   
    self.set_ram(116, 190)

def static_ghosts(self):
    '''
    static_ghosts: Manipulates the RAM cell at position 6-9 and 12-15 to fix the position of
    the ghost inside the square in the middle of the screen.
    '''
    if TOGGLE_ORANGE or GHOSTS_CAGED:
        self.set_ram(6, 93)
        self.set_ram(12, 80)
    if TOGGLE_CYAN or GHOSTS_CAGED:
        self.set_ram(7, 83)
        self.set_ram(13, 80)
    if TOGGLE_PINK or GHOSTS_CAGED:
        self.set_ram(8, 93)
        self.set_ram(14, 67)
    if TOGGLE_RED or GHOSTS_CAGED:
        self.set_ram(9, 83)
        self.set_ram(15, 67)

def number_power_pills(self):
    '''
    number_power_pills: Manipulates the RAM cell at position 117 (= power pills), 
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

def edible_ghosts(self):
    '''
    edible_ghosts: Manipulates the RAM cell at position 117 (= power pills), 
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

def inverted_ms_pacman(self):
    '''
    inverted_ms_pacman: Manipulates the RAM cell at position 1-4 (= ghost status) so all 
    ghost will be edible the entire game until the player eats a power pill 
    (RAM 117 = power pill status). After eating a power pill the ghost will return to 
    "normal" for a certain amount of time (RAM cell 116 = timer).

    is_at_start: a bool used as a switch to determine if the game was reset.
    is_inverted: a bool used as a switch to determine the current game mode.
    last_pp_status: an integer used to save the last value in the RAM cell for 
    the power pills. The value is needed to determine if a power pill has been eaten.
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
        self.last_pp_status = 63
        set_start_condition(self)

    # only do this at the beginning of a new level
    if current_pp_status == 63 and self.last_pp_status != current_pp_status:
        self.is_at_start = False # disable switch
        self.last_pp_status = 63
        set_start_condition(self)

    # check if switchs needs to be reset
    if current_lives == 1 and self.is_at_start is False:
        self.is_at_start = True # enable switch

    # check if timer needs to be adjusted
    if current_timer < 250 and self.is_inverted is False:
        self.set_ram(116, 255)

    # check if a power pill has been eaten
    # a range is required because the values in the RAm cells fluctuate
    if not((self.last_pp_status - 3) < current_pp_status < (self.last_pp_status + 3)):
        self.is_inverted = True
        inverted_power_pill(self)
        self.last_pp_status = current_pp_status
    
    # check if effect of power pill has run out
    if current_timer == 0 and self.is_inverted:
        self.is_inverted = False # disable switch
        power_pill_is_done(self)

    # check if a ghost has been eaten and if needed make them edible again
    # change start location to avoid glitches
    if current_orange == 112 and not self.is_inverted:
        make_edible(self, 1, 120, 6, 50, 12)
    if current_cyan == 112 and not self.is_inverted:
        make_edible(self, 2, 100, 7, 50, 13)
    if current_pink == 112 and not self.is_inverted:
        make_edible(self, 3, 80, 8, 50, 14)
    if current_red == 112 and not self.is_inverted:
        make_edible(self, 4, 60 ,9, 50, 15)
        



class MsPacmanExtended(OCAtari):
    '''
    MsPacmanExtended: Modifies the Atari game "Ms. Pacman" 
    '''

    def __init__(self, env_name="MsPacman", mode="revised",
                 hud=True, obs_mode="dqn", *args, **kwargs):
        '''
        Initializes an OCAtari game environment with preset values for game name, mode, and 
        observation mode. The Heads-Up Display (HUD) is enabled by default.

        is_at_start: a bool used as a switch to determine if the game was reset.
        is_inverted: a bool used as a switch to determine the current game mode.
        last_pp_status: an integer used to save the last value in the RAM cell for 
        the power pills. The value is needed to determine if a power pill has been eaten.
        '''
        self.render_mode = kwargs["render_mode"] if "render_mode" in kwargs else None
        # Call __init__ to create the OCAtari environment
        super().__init__(env_name, mode, hud, obs_mode, *args, **kwargs)
        self.is_at_start = True # enable switch
        self.is_inverted = False # disable switch
        self.last_pp_status = 63
        

    def alter_ram(self):
        '''
        alter_ram: Manipulates certain ram cells via helper functions to enable/disable
        or change certain features about the game.
        '''
        number_power_pills(self)
        static_ghosts(self)

        if EDIBLE:
            edible_ghosts(self)

        if INVERSE:
            inverted_ms_pacman(self)
        
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

class MsPacmanExtendedHuman(OCAtari):
    '''
    InvertedMsPacmanHuman: Enables human play mode for the NoPowerPillMsPacman game.
    Modifies the Atari game "Ms. Pacman" in a way that the function of the power pills is 
    inverted.
    '''

    env: gym.Env

    def __init__(self, env_name: str):
        '''
        Initializes the InvertedMsPacmanHuman environment with the specified environment name.

        is_at_start: a bool used as a switch to determine if the game was reset.
        is_inverted: a bool used as a switch to determine the current game mode.
        last_pp_status: an integer used to save the last value in the RAM cell for 
        the power pills. The value is needed to determine if a power pill has been eaten.
        '''
        self.env = OCAtari(env_name, mode="revised", hud=True, render_mode="human",
                        render_oc_overlay=True, frameskip=1)
        self.env.reset()
        self.env.render()  # Initialize the pygame video system

        self.paused = False
        self.current_keys_down = set()
        self.keys2actions = self.env.unwrapped.get_keys_to_action()

        self.is_at_start = True # enable switch
        self.is_inverted = False # disable switch
        self.last_pp_status = 63

    def run(self):
        '''
        Manipulates certain ram cells via helper functions to enable/disable
        or change certain features about the game.
        '''
        self.running = True
        while self.running:
            self._handle_user_input()
            if not self.paused:
                number_power_pills(self.env)
                static_ghosts(self.env)

                if EDIBLE:
                    edible_ghosts(self.env)

                if INVERSE:
                    inverted_ms_pacman(self.env)

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
        _handle_user_input: Handles user input for the InvertedMsPacmanHuman environment.
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
    renderer = MsPacmanExtendedHuman('MsPacman')
    renderer.run()
else:
    env = MsPacmanExtended(render_mode="human")
    # The following path to the agent has to be modified according to individual user setup
    # and folder names
    dqn_agent = load_agent("../OC_Atari/models/MsPacman/dqn.gz",
                            env.action_space.n)

    env.reset()

    # Let the agent play the game for 10000 steps
    for i in range(10000):
        action = dqn_agent.draw_action(env.dqn_obs)
        _, _, done1, done2, _ = env.step(action)
        sleep(0.01)
        if done1 or done2:
            env.reset()
