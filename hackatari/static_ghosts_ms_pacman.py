'''
static_ghosts_ms_pacman.py implements an altered version of Ms. Pacman, in which 
a choosen number of the ghosts won't leave the square in the middle of the screen. 
'''

from time import sleep
import torch
import cv2
import pygame
import numpy as np
import gymnasium as gym
from ocatari.core import OCAtari, DEVICE
from ocatari.utils import parser, load_agent

parser.add_argument("-orange", "--orange", default=1, type=int,
    help="Argument for enabling (1) or disabling (0) the movement of the orange ghost")
parser.add_argument("-cyan", "--cyan", default=1, type=int, 
    help="Argument for enabling (1) or disabling (0) the movement of the cyan ghost")
parser.add_argument("-pink", "--pink", default=1, type=int,
    help="Argument for enabling (1) or disabling (0) the movement of the pink ghost")
parser.add_argument("-red", "--red", default=1, type=int,
    help="Argument for enabling (1) or disabling (0) the movement of the red ghost")
parser.add_argument("-hu", "--human", default=False, type=bool, 
    help="Argument for enabling (True) or disabling (False) human play mode")

opts = parser.parse_args()

TOGGLE_HUMAN_MODE = opts.human

'''
A constant that toggles the state of the agent mode.

This constant is used to toggle between the human mode and the agent mode. 
The value 'True' indicates that the human mode is active, while the value
'False' indicates that the agent mode is active.
'''

TOGGLE_ORANGE = opts.orange
TOGGLE_CYAN = opts.cyan
TOGGLE_PINK = opts.pink
TOGGLE_RED = opts.red

'''
Four constants that determine which ghots are enabled or disabled.
The values are provided by parser arguments via command line.
The default is 1 for all four. Therefore all ghosts are disabled by default.
'''

class StaticGhostMsPacman(OCAtari):
    '''
    StaticGhostMsPacman: Modifies the Atari game "Ms. Pacman" such that the ghosts are not 
    able to move freely. Instead they will always stay inside the square in the middle of the
    screen, where they won't be able to attack the player. Therefore the player won't be 
    able to eat the ghosts.
    '''

    def __init__(self, env_name="MsPacman", mode="revised",
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
        alter_ram: Manipulates the RAM cell at position 6-9 and 12-15 to fix the position of
        the ghost inside the square in the middle of the screen.
        The representation is as follows: 
        ghosts_position_x = "orange": ram_state[6]
                            "cyan": ram_state[7]
                            "pink": ram_state[8]
                            "red": ram_state[9]
        ghosts_position_y" =    "orange": ram_state[12]
                                "cyan": ram_state[13]
                                "pink": ram_state[14]
                                "red": ram_state[15]
        '''
        if TOGGLE_ORANGE == 1:
            self.set_ram(6, 93)
            self.set_ram(12, 80)
        if TOGGLE_CYAN == 1:
            self.set_ram(7, 83)
            self.set_ram(13, 80)
        if TOGGLE_PINK == 1:
            self.set_ram(8, 93)
            self.set_ram(14, 67)
        if TOGGLE_RED == 1:
            self.set_ram(9, 83)
            self.set_ram(15, 67)

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

class StaticGhostMsPacmanHuman(OCAtari):
    '''
    StaticGhostMsPacmanHuman: Enables human play mode for the StaticGhostMsPacman game.
    '''

    env: gym.Env

    def __init__(self, env_name: str):
        '''
        Initializes the StaticGhostMsPacmanHuman environment with the specified environment name.
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
        run: Runs the StaticGhostMsPacmanHuman environment, allowing human interaction
        with the game.
        '''
        self.running = True
        while self.running:
            self._handle_user_input()
            if not self.paused:
                action = self._get_action()
                # Change RAM value
                if TOGGLE_ORANGE == 1:
                    self.env.set_ram(6, 93)
                    self.env.set_ram(12, 80)
                if TOGGLE_CYAN == 1:
                    self.env.set_ram(7, 83)
                    self.env.set_ram(13, 80)
                if TOGGLE_PINK == 1:
                    self.env.set_ram(8, 93)
                    self.env.set_ram(14, 67)
                if TOGGLE_RED == 1:
                    self.env.set_ram(9, 83)
                    self.env.set_ram(15, 67)
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
        _handle_user_input: Handles user input for the StaticGhostMsPacmanHuman environment.
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
    renderer = StaticGhostMsPacmanHuman('MsPacman')
    renderer.run()
else:
    env = StaticGhostMsPacman(render_mode="human")
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
