import pygame
from ocatari.core import OCAtari, DEVICE
import numpy as np
import torch
import cv2

class HideEnemyPong(OCAtari):
    def __init__(self, env_name="PongDeterministic-v0", mode="raw", hud=False, obs_mode="dqn", *args, **kwargs):
        self.render_mode = kwargs["render_mode"] if "render_mode" in kwargs else None
        if self.render_mode == "human":
            kwargs["render_mode"] = None
            self.screen = pygame.display.set_mode((160, 210), flags=pygame.SCALED)
            pygame.init()
        super().__init__(env_name, mode, hud, obs_mode, *args, **kwargs)

    def _step_ram(self, *args, **kwargs):
        # if self.render_mode == "human":
        self._make_rendering()
        return super()._step_ram(*args, **kwargs)
    
    def _make_rendering(self):
        rgb_array = self._ale.getScreenRGB()
        rgb_array[34:194, 4:20] = [144, 72, 17]

        # Render RGB image
        rgb_array = np.transpose(rgb_array, (1, 0, 2))
        pygame.pixelcopy.array_to_surface(self.screen, rgb_array)

        pygame.display.flip()
        pygame.event.pump()
    
    def _fill_buffer_dqn(self):
        image = self._ale.getScreenGrayscale()
        image[34:194, 8:24] = 87
        state = cv2.resize(
            image, (84, 84), interpolation=cv2.INTER_AREA,
        )
        self._state_buffer.append(torch.tensor(state, dtype=torch.uint8,
                                               device=DEVICE))

import random
from time import sleep
env = HideEnemyPong(render_mode="human")
env.reset()
for i in range(10000):
    _, _, done1, done2, _ = env.step(random.randint(0, 3))
    sleep(0.02)
    if done1 or done2:
        env.reset()