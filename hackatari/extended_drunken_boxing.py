'''
drunkenboxing.py implements a further developed version of drunkenboxing
with the basis of Boxing, in which the boxer always staggers in a circle.
'''
from time import sleep
import time
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

class DrunkenBoxing(OCAtari):
    '''
    DrunkenBoxing: Modifies the Atari game "Boxing" to simulate that the boxer
    is always tumbling in circles. The pattern is forward, up, backward, down,
    forward, etc. (if possible)
    '''

    def __init__(self, env_name="Boxing", mode="raw", hud=False, obs_mode="dqn", *args, **kwargs):
        '''
        Initializes an OCAtari game environment with preset values for game name, mode, and
        observation mode. The Heads-Up Display (HUD) is disabled by default.
        '''
        self.render_mode = kwargs.get("render_mode", None)
        # Call __init__ to create the OCAtari environment
        super().__init__(env_name, mode, hud, obs_mode, *args, **kwargs)

        self.counter = 0
        self.last_reset_time = time.time()


    def set_ram_value(self, address, value):
        '''
        Sets the value in RAM at a specific address.
        '''
        ram = self.get_ram()
        ram[address] = value
        self.set_ram(address, ram[address])

    def alter_ram(self):
        '''
        Performs a sequence of operations (forward, up, backward, down) based
        on the value of the counter. Keeps track of the number of function
        calls using the counter variable.

        '''
        # Add a counter variable to keep track of the function calls
        self.counter = getattr(self, 'counter', 0)

        # Call functions in sequence based on the counter value
        if self.counter % 4 == 0:
            self.forward()
        elif self.counter % 4 == 1:
            self.move_up()
        elif self.counter % 4 == 2:
            self.backward()
        elif self.counter % 4 == 3:
            self.down()

        # Increment the counter for the next function call
        self.counter += 1

        # Introduce a sleep of 1 second (adjust the sleep duration as needed)
        #time.sleep(1)

    def forward(self):
        '''
        Moves the player character forward in the game environment.
        '''
        curr_player_pos_x = self.get_ram()[32]
        curr_player_pos_x_enemy = self.get_ram()[33]

        if 0 < curr_player_pos_x < 109 and curr_player_pos_x + 14 != curr_player_pos_x_enemy:
            curr_player_pos_x += 1
            self.set_ram_value(32, curr_player_pos_x)

    def move_up(self):
        '''
        Moves the player character up in the game environment.
        '''
        curr_player_pos_y = self.get_ram()[34]

        if 0 < curr_player_pos_y < 87:
            curr_player_pos_y -= 1
            self.set_ram_value(34, curr_player_pos_y)

    def backward(self):
        '''
        Moves the player character backward in the game environment.
        '''
        curr_player_pos_x = self.get_ram()[32]

        if 0 < curr_player_pos_x < 109:
            curr_player_pos_x -= 1
            self.set_ram_value(32, curr_player_pos_x)

    def down(self):
        '''
        Moves the player character down in the game environment.
        '''
        curr_player_pos_y = self.get_ram()[34]

        if 0 < curr_player_pos_y < 87:
            curr_player_pos_y += 1
            self.set_ram_value(34, curr_player_pos_y)

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

class DrunkenBoxingHuman(OCAtari):
    '''
    DrunkenBoxingHuman: Enables human play mode for the DrunkenBoxing game.
    '''

    env: gym.Env

    def __init__(self, env_name: str):
        '''
        Initializes the DrunkenBoxingHuman environment with the specified environment name.
        '''
        self.env = OCAtari(env_name, mode="revised", hud=True, render_mode="human",
                        render_oc_overlay=True, frameskip=1)
        self.env.reset()
        self.env.render()  # Initialize the pygame video system

        self.paused = False
        self.current_keys_down = set()
        self.keys2actions = self.env.unwrapped.get_keys_to_action()


    def _get_enemy_position(self):
        '''
        Retrieves the current position of the enemy from the game's RAM.
        '''
        curr_player_pos_x_enemy = self.env.get_ram()[33]
        curr_player_pos_y_enemy = self.env.get_ram()[35]
        return curr_player_pos_x_enemy, curr_player_pos_y_enemy

    def _step_and_render(self, action, change_x, change_y):
        '''
        Perform a step in the environment, updating the player's position and rendering the game.
        '''
        curr_player_pos_x = self.env.get_ram()[32]
        curr_player_pos_y = self.env.get_ram()[34]
        curr_player_pos_x += change_x
        curr_player_pos_y += change_y

        self.env.set_ram(32, curr_player_pos_x)
        self.env.set_ram(34, curr_player_pos_y)
        self.env.step(action)
        self.env.render()

        time.sleep(0.01)  # Delay, if desired

    def run(self):
        '''
        run: Runs the DrunkenBoxingHuman environment, allowing human interaction with the game.
        '''
        self.running = True
        while self.running:
            self._handle_user_input()
            if not self.paused:
                action = self._get_action()

                if 0 < self.env.get_ram()[32] < 109 and not \
                    (pygame.K_a in list(self.current_keys_down)) \
                    and not (self.env.get_ram()[33] - self.env.get_ram()[32]) < 16:
                    # move forward
                    self._step_and_render(action, 1, 0)

                if 1 < self.env.get_ram()[34] < 87 and not \
                    pygame.K_s in list(self.current_keys_down):
                    # move up
                    self._step_and_render(action, 0, -1)

                if 1 < self.env.get_ram()[32] < 109 and not \
                    pygame.K_d in list(self.current_keys_down):
                    # move backward
                    self._step_and_render(action, -1, 0)

                if 0 < self.env.get_ram()[34] < 87 and not \
                    pygame.K_w in list(self.current_keys_down):
                    # move down
                    self._step_and_render(action, 0, 1)

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
        _handle_user_input: Handles user input for the DrunkenBoxingHuman environment.
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
    renderer = DrunkenBoxingHuman('Boxing')
    renderer.run()
else:
    env = DrunkenBoxing(render_mode="human")
    # The following path to the agent has to be modified according to individual user setup
    # and folder names
    dqn_agent = load_agent("/home/m0chi/Schreibtisch/AI/OC_Atari-master/models/Boxing/dqn.gz",
                           env.action_space.n)
    env.reset()
    # Let the agent play the game for 10000 steps
    for i in range(10000):
        action = dqn_agent.draw_action(env.dqn_obs)
        _, _, done1, done2, _ = env.step(action)
        sleep(0.01)
        if done1 or done2:
            env.reset()
