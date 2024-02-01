'''
relocatable_shields_space_invaders.py implements a altered version of SpaceInvaders,
in which the shields can be relocated based on a user specified offset.  
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

parser.add_argument("-pos", "--position", default=43, type=int,
                     help="Argument for setting the offset of the shield position." +
                     " The positional anchor is the left corner of the left shield with position 0."
                     +" The chosen number has to be between 0 and 225.")
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

SHIELD_POSITION_OFFSET = opts.position
if SHIELD_POSITION_OFFSET > 53 or SHIELD_POSITION_OFFSET < 35:
    print(colored('Illegal input for shield position offset. Shield position offset has to be' +
                   'between 35 and 53... Continuing with default position 43.', 'red'))
    SHIELD_POSITION_OFFSET = 43
"""
A Constant that determines the offset which is used to relocate the shields. A check is used to intercept illegal input values. If illegal values are used
a error message is displayed and the game is run using the default shield position as seen in the original game setup.
"""

class RelocatableShieldsSpaceInvaders(OCAtari):
    '''
    RelocatableShieldsSpaceInvaders: Modifies the Atari game "Space Invaders" such that
    the shields can be relocated. This class represents the ai agent mode.
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
        alter_ram: Manipulates the RAM cells at position 27 by setting them to the chosen offset 
        position if the corresponding variable is set accordingly. The shields are relocated 
        based on the position of the left shield. Possible values are between 35 and 53.
        '''
        shield_pos_new = SHIELD_POSITION_OFFSET
        if shield_pos_new < 53 and shield_pos_new >= 35:
            self.set_ram(27, shield_pos_new)

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

class RelocatableShieldsSpaceInvadersHuman(OCAtari):
    '''
    RelocatableShieldsSpaceInvadersHuman: Enables human play mode for the 
    RelocatableShieldsSpaceInvaders game.
    '''

    env: gym.Env

    def __init__(self, env_name: str):
        '''
        Initializes the RelocatableShieldsSpaceInvaders environment with the specified
        environment name.
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
        run: Runs the RelocatableShieldsSpaceInvadersHuman environment, allowing human interaction
        with the game.
        '''
        self.running = True
        while self.running:
            self._handle_user_input()
            if not self.paused:
                action = self._get_action()
                # ram changes for relocating shields
                # new shield position is based on the initially chosen offset value
                shield_pos_new = SHIELD_POSITION_OFFSET
                if shield_pos_new < 53 and shield_pos_new >= 35:
                    self.env.set_ram(27, shield_pos_new)
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
        _handle_user_input: Handles user input for the 
        RelocatableShieldsSpaceInvadersHuman environment.
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
    renderer = RelocatableShieldsSpaceInvadersHuman('SpaceInvaders')
    renderer.run()
else:
    env = RelocatableShieldsSpaceInvaders(render_mode="human")
    # The following path to the agent has to be modified according to individual user setup
    # and folder names
    dqn_agent = load_agent("../OC_Atari_master_HA_Testing/models/SpaceInvaders/dqn.gz",
                            env.action_space.n)
    env.reset()

    # Let the agent play the game for 10000 steps
    for i in range(10000):
        action = dqn_agent.draw_action(env.dqn_obs)
        _, _, done1, done2, _ = env.step(action)
        sleep(0.01)
        if done1 or done2:
            env.reset()
