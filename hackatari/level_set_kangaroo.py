"""
This module provides an enhanced gaming experience for the Atari game "Kangaroo" by introducing
customizable difficulty levels trough modified starting positions.

Key Features:
- TOGGLE_HUMAN_MODE: A switch to alternate between human play and agent mode, allowing for 
  both manual and AI-driven game interaction.
- FLOOR: Players can set the starting floor to adjust the game's difficulty,
  making it easier to complete the game by skipping initial floors.
"""


from time import sleep
import gymnasium as gym
import pygame
import torch
import cv2
import numpy as np
from ocatari.core import OCAtari, DEVICE
from ocatari.utils import load_agent



TOGGLE_HUMAN_MODE = 'True'
"""
A constant that toggles the state of the agent mode.

This constant is used to toggle between the human mode and the agent mode. 
The value 'True' indicates that the human mode is active, while the value
'False' indicates that the agent mode is active.
"""


FLOOR = 1
'''
This constant can be changed to numbers between 0 and 2.
FLOOR = 0 is the normal mode, meaning the start position isn't changed.
FLOOR = 1 the starting position is changed and also moved up one floor,
          so that the game is easier to finish.
FLOOR = 2 the starting position is changed and also moved up two floors,
          so that the game is even easier to finish.
'''



# Constants for clarity and maintainability
KANGAROO_POS_X_INDEX = 17   # RAM index for kangaroo's X position
KANGAROO_POS_Y_INDEX = 16   # RAM index for kangaroo's Y position
LEVEL_2 = 2

# Starting positions based on different conditions
FLOOR_1_LEVEL2_POS = (25, 10)
FLOOR_2_LEVEL2_POS = (100, 6)
FLOOR_1_START_POS = (65, 12)
FLOOR_2_START_POS = (65, 6)
ANY_FLOOR_INSTANT_WIN = (110, 0)

def set_kangaroo_position(self, pos_x, pos_y):
    """
    Set the kangaroo's position.
    Args:
    pos_x (int): The x-coordinate for the kangaroo's position.
    pos_y (int): The y-coordinate for the kangaroo's position.
    """
    self.set_ram(KANGAROO_POS_X_INDEX, pos_x)
    self.set_ram(KANGAROO_POS_Y_INDEX, pos_y)


def is_at_start(pos):
    """
    checks wether the given x and y coordinates are in the starting range of the kangaroo.
    Args:
    pos_x (int): The x-coordinate.
    pos_y (int): The y-coordinate.
    """
    return (5 < pos[0] < 11 and 16 < pos[1] < 21)

class LevelSetKangaroo(OCAtari):
    ''' 
    LevelSetKangaroo: Modifies the Atari game "Kangaroo" to enable the player
    to choose the difficulty of the game, by choosing how many floors should be skipped
    and also changing the starting position.
    Making it easier for humans but not necessarily for agents.
    '''

    # initializing the game from the original game of Kangaroo
    def __init__(self, env_name="Kangaroo", mode="revised", hud=False,
        obs_mode="dqn", *args, **kwargs):
        '''
        __init__: Initializes a OCAtari game environment. The game environment name, the mode 
            and the observation mode are preset. The HUD is disabled.
        '''
        self.render_mode = kwargs["render_mode"] if "render_mode" in kwargs else None
        super().__init__(env_name, mode, hud, obs_mode, *args, **kwargs)
        self.position_set = False  # Flag to track if the position has been set
        self.last_level = self.get_ram()[36]
        self.last_lives = self.get_ram()[45]


    def alter_ram(self):
        '''
        alter_ram: sets the starting position depending on the difficulty,
        which is chosen with the FLOOR constant.
        '''

        #get the current ram state
        ram = self.get_ram()

        current_level = ram[36]
        kangaroo_pos = (ram[KANGAROO_POS_X_INDEX], ram[KANGAROO_POS_Y_INDEX])

        current_lives = ram[45]


        # checks wether the palyer has finished a level or has lost a live
        # to re-enable the teleportation to the new starting position
        if current_lives != self.last_lives or current_level != self.last_level:
            self.position_set = False
            self.last_lives = current_lives
            self.last_level = current_level





        if is_at_start(kangaroo_pos) and not self.position_set:
            if FLOOR == 1:
                # For floor 1, position depends on whether the current level is 2
                new_pos = FLOOR_1_LEVEL2_POS if current_level == LEVEL_2 else FLOOR_1_START_POS
                set_kangaroo_position(self, *new_pos)
            elif FLOOR == 2:
                # For floor 2, position is set to a different location
                # but also depends on the current level
                new_pos = FLOOR_2_LEVEL2_POS if current_level == LEVEL_2 else FLOOR_2_START_POS
                set_kangaroo_position(self, *new_pos)
            self.position_set = True







    def _step_ram(self, *args, **kwargs):
        '''
        step_ram: Updates the environment by one ram step
        '''
        self.alter_ram()
        ram_step = super()._step_ram(*args, **kwargs)
        return ram_step

    def _fill_buffer_dqn(self):
        '''
        _fill_buffer_dqn: Fills the buffer for usage by the dqn agent
        '''
        image = self._ale.getScreenGrayscale()
        state = cv2.resize(
            image, (84, 84), interpolation=cv2.INTER_AREA,
        )
        self._state_buffer.append(torch.tensor(state, dtype=torch.uint8,
                                               device=DEVICE))



class LevelSetKangarooHuman(OCAtari):
    '''
    LevelSetKangarooHuman: Enables human play mode for the level_set_kangaroo game.
    '''

    env: gym.Env

    def __init__(self, env_name: str):
        '''
        Initializes the LevelSetKangarooHuman environment with the specified environment name.
        '''
        self.env = OCAtari(env_name, mode="revised", hud=True, render_mode="human",
                        render_oc_overlay=True, frameskip=1)
        self.env.reset()
        self.env.render()  # Initialize the pygame video system
        self.position_set = False  # Flag to track if the position has been set
        self.last_level = self.env.get_ram()[36]
        self.last_lives = self.env.get_ram()[45]
        self.paused = False
        self.current_keys_down = set()
        self.keys2actions = self.env.unwrapped.get_keys_to_action()


    def run(self):
        '''
        run: Runs the LevelSetKangarooHuman environment, allowing human interaction with the game.
        '''
        self.running = True
        while self.running:
            self._handle_user_input()
            if not self.paused:
                action = self._get_action()

                #gets the current ram state
                ram = self.env.get_ram()
                current_lives = ram[45]
                current_level = ram[36]
                kangaroo_pos = (ram[KANGAROO_POS_X_INDEX], ram[KANGAROO_POS_Y_INDEX])


                # checks wether the palyer has finished a level or has lost a live
                # to re-enable the teleportation to the new starting position
                if current_lives != self.last_lives or current_level != self.last_level:
                    self.position_set = False
                    self.last_lives = current_lives
                    self.last_level = current_level


                if is_at_start(kangaroo_pos) and not self.position_set:
                    if FLOOR == 1:
                        # For floor 1, position depends on whether the current level is 2
                        new_pos = FLOOR_1_LEVEL2_POS if current_level == 2 else FLOOR_1_START_POS
                        set_kangaroo_position(self.env, *new_pos)
                    elif FLOOR == 2:
                        # For floor 2, position is set to a different location,
                        # but also depends on the current level
                        new_pos = FLOOR_2_LEVEL2_POS if current_level == 2 else FLOOR_2_START_POS
                        set_kangaroo_position(self.env, *new_pos)
                    self.position_set = True



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
        _handle_user_input: Handles user input for the LevelSetKangarooHuman environment.
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




# code for having an agent play the modified game

if TOGGLE_HUMAN_MODE == 'True':
    renderer = LevelSetKangarooHuman('Kangaroo')
    renderer.run()
else:
    env = LevelSetKangaroo(render_mode="human")
    # The following path to the agent has to be modified according to individual user setup
    # and folder names
    dqn_agent = load_agent("../OC_Atari/models/Kangaroo/dqn.gz", env.action_space.n)
    env.reset()
    # Let the agent play the game for 10000 steps
    for i in range(10000):
        action = dqn_agent.draw_action(env.dqn_obs)
        _, _, done1, done2, _ = env.step(action)
        sleep(0.01)
        if done1 or done2:
            env.reset()
