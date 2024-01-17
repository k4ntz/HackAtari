'''
CarColorFreeway.py implements a modified version of Freeway in which all cars are assigned a color.
'''
from time import sleep
import torch
import cv2
import pygame
import numpy as np
import gymnasium as gym
from ocatari.core import OCAtari, DEVICE
from ocatari.utils import load_agent



TOGGLE_HUMAN_MODE = 'False'
'''
A constant that toggles the state of the agent mode.

This constant is used to toggle between the human mode and the agent mode.
The value 'True' indicates that the human mode is active, while the value
'False' indicates that the agent mode is active.
'''

CAR_COLOR = 0
'''
The constant changes the colors of the cars as follows:
0 = standard; 1 = black; 2 = grey; 3 = red; 4 = white; 5 = green;
6 = purple; 7 = blue; 8 = "invisible"
'''

class CarColorFreeway(OCAtari):
    '''
    CarColorFreeway: The class has been adapted to modify the Atari game "Freeway"
    by assigning the same color to all cars. A total of six colors are available,
    as well as the special "invisible" mode.
    '''

    def __init__(self, env_name="Freeway", mode="raw", hud=False, obs_mode="dqn", *args, **kwargs):
        '''
        Initializes an OCAtari game environment with preset values for game name, mode, and
        observation mode. The Heads-Up Display (HUD) is disabled by default.
        '''
        self.render_mode = kwargs.get("render_mode", None)
        # Call __init__ to create the OCAtari environment
        super().__init__(env_name, mode, hud, obs_mode, *args, **kwargs)
        #self.counter = 10

    def set_ram_value(self, address, value):
        '''
        Sets the value in RAM at a specific address.
        '''
        ram = self.get_ram()
        ram[address] = value
        self.set_ram(address, ram[address])

    def car_color(self):
        '''
        This function assigns certain color values to the cars in the game "Freeway".
        '''
        color = 0
        if CAR_COLOR == 0 or CAR_COLOR > 8:
            color = 256
        elif CAR_COLOR == 1:
            color = 0
        elif CAR_COLOR == 2:
            color = 2
        elif CAR_COLOR == 3:
            color = 66
        elif CAR_COLOR == 4:
            color = 15
        elif CAR_COLOR == 5:
            color = 210
        elif CAR_COLOR == 6:
            color = 120
        elif CAR_COLOR == 7:
            color = 145
        elif CAR_COLOR == 8:
            color = 6
        return color

    def alter_ram(self):
        '''
        This function modifies the RAM memory based on the specified color values.
        '''
        color = self.car_color()

        if color != 256:
            for car in range(77, 87):
                self.set_ram(car, color)
        else:
            self.set_ram(77, 26)
            self.set_ram(78, 216)
            self.set_ram(79, 68)
            self.set_ram(80, 136)
            self.set_ram(81, 36)
            self.set_ram(82, 130)
            self.set_ram(83, 74)
            self.set_ram(84, 18)
            self.set_ram(85, 220)
            self.set_ram(86, 66)
            self.set_ram(87, 189)
            
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

class CarColorFreewayHuman(OCAtari):
    '''
    CarColorFreewayHuman: Enables human play mode for the CarColorFreeway game.
    '''

    env: gym.Env

    def __init__(self, env_name: str):
        '''
        Initializes the CarColorFreewayHuman environment with the specified environment name.
        '''
        self.env = OCAtari(env_name, mode="revised", hud=True, render_mode="human",
                        render_oc_overlay=True, frameskip=1)
        self.env.reset()
        self.env.render()  # Initialize the pygame video system

        self.paused = False
        self.current_keys_down = set()
        self.keys2actions = self.env.unwrapped.get_keys_to_action()

    def car_color(self):
        '''
        This function assigns certain color values to the cars in the game "Freeway".
        '''
        color = 0
        if CAR_COLOR == 0 or CAR_COLOR > 8:
            color = 256
        elif CAR_COLOR == 1:
            color = 0
        elif CAR_COLOR == 2:
            color = 2
        elif CAR_COLOR == 3:
            color = 66
        elif CAR_COLOR == 4:
            color = 15
        elif CAR_COLOR == 5:
            color = 210
        elif CAR_COLOR == 6:
            color = 120
        elif CAR_COLOR == 7:
            color = 145
        elif CAR_COLOR == 8:
            color = 6
        return color

    def run(self):
        '''
        run: Runs the CarColorFreewayHuman environment, allowing human interaction with the game.
        '''
        self.running = True
        while self.running:
            self._handle_user_input()
            if not self.paused:
                action = self._get_action()

                color = self.car_color()

                if color != 256:
                    for car in range(77, 87):  # Änderung des Bereichs von 77 bis 87 (exklusiv)
                        self.env.set_ram(car, color)
                else:
                    self.env.set_ram(77, 26)
                    self.env.set_ram(78, 216)
                    self.env.set_ram(79, 68)
                    self.env.set_ram(80, 136)
                    self.env.set_ram(81, 36)
                    self.env.set_ram(82, 130)
                    self.env.set_ram(83, 74)
                    self.env.set_ram(84, 18)
                    self.env.set_ram(85, 220)
                    self.env.set_ram(86, 66)
                    self.env.set_ram(87, 189)

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
        _handle_user_input: Handles user input for the CarColorFreewayHuman environment.
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
if TOGGLE_HUMAN_MODE == 'True':
    renderer = CarColorFreewayHuman('Freeway')
    renderer.run()
else:
    env = CarColorFreeway(render_mode="human")
    # The following path to the agent has to be modified according to individual user setup
    # and folder names
    dqn_agent = load_agent("/home/m0chi/Schreibtisch/AI/OC_Atari-master/models/Freeway/dqn.gz", 
                           env.action_space.n)
    env.reset()
    # Let the agent play the game for 10000 steps
    for i in range(10000):
        action = dqn_agent.draw_action(env.dqn_obs)
        _, _, done1, done2, _ = env.step(action)
        sleep(0.01)
        if done1 or done2:
            env.reset()
