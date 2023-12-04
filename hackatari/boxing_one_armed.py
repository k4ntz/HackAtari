import pygame
import torch
import cv2
import numpy as np
from time import sleep
from ocatari.core import OCAtari, DEVICE
from ocatari.utils import load_agent 
import gymnasium as gym


TOGGLE_HUMAN_MODE = 'True'
"""
A constant that toggles the state of the agent mode.

This constant is used to toggle between the human mode and the agent mode. 
The value 'True' indicates that the human mode is active, while the value
'False' indicates that the agent mode is active.
"""





class BoxingOneArmed(OCAtari):
    ''' 
    BoxingOneArmed: Modifies the Atari game "Boxing" such that the player or agent
    can't use the right arm to box.
    '''

    # initializing the game from the original game of boxing
    def __init__(self, env_name="Boxing", mode="revised", hud=False,
    obs_mode="dqn", *args, **kwargs):
        '''
        __init__: Initializes a OCAtari game environment. The game environment name, the mode 
            and the observation mode are preset. The HUD is disabled.
        '''
        self.render_mode = kwargs["render_mode"] if "render_mode" in kwargs else None
        super().__init__(env_name, mode, hud, obs_mode, *args, **kwargs)

    def alter_ram(self):
        '''
        alter_ram: Manipulates the RAM cell at position 101
        to facilitate that the right arm is not useable.
        The value in the aforementioned cell is continually set to 128.
        '''
        self.set_ram(101, 128) # disables the "hitting motion" with the right arm permanently




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



class BoxingOneArmedHuman(OCAtari): 
    '''
    BoxingOneArmedHuman: Enables human play mode for the BoxingOneArmed game.
    '''

    env: gym.Env

    def __init__(self, env_name: str):
        '''
        Initializes the BoxingOneArmedHuman environment with the specified environment name.
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
        run: Runs the BoxingOneArmedHuman environment, allowing human interaction with the game.
        '''
        self.running = True
        while self.running:
            self._handle_user_input()
            if not self.paused:
                action = self._get_action()
                # Change RAM value
                self.env.set_ram(101, 128) # disables the "hitting motion" with the right arm permanently
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
        _handle_user_input: Handles user input for the BoxingOneArmedHuman environment.
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
    renderer = BoxingOneArmedHuman('Boxing')
    renderer.run()
else:
    env = BoxingOneArmed(render_mode="human")
    # The following path to the agent has to be modified according to individual user setup
    # and folder names
    dqn_agent = load_agent("../OC_Atari/models/Boxing/dqn.gz", env.action_space.n)
    env.reset()
    # Let the agent play the game for 10000 steps
    for i in range(10000):
        action = dqn_agent.draw_action(env.dqn_obs)
        _, _, done1, done2, _ = env.step(action)
        sleep(0.01)
        if done1 or done2:
            env.reset()


