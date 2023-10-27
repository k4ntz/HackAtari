import pygame
from ocatari.core import OCAtari, DEVICE
import numpy as np
import torch
import cv2

class ConstantBackgroundRiverraid(OCAtari):
    def __init__(self, env_name="RiverraidDeterministic-v0", mode="raw", hud=False, obs_mode="dqn", *args, **kwargs):
        self.render_mode = kwargs["render_mode"] if "render_mode" in kwargs else None
        super().__init__(env_name, mode, hud, obs_mode, *args, **kwargs)

    def _step_ram(self, *args, **kwargs):
        bgs = env.get_ram()[38:44]
        for i, bg in enumerate(bgs):
            if bg not in [65, 129]:
                env.set_ram(38+i, 35)
        toret = super()._step_ram(*args, **kwargs)
        bgs = env.get_ram()[38:44]
        for i, bg in enumerate(bgs):
            if bg not in [65, 129]:
                env.set_ram(38+i, 35)
        return toret

    def _fill_buffer_dqn(self):
        image = self._ale.getScreenGrayscale()
        state = cv2.resize(
            image, (84, 84), interpolation=cv2.INTER_AREA,
        )
        self._state_buffer.append(torch.tensor(state, dtype=torch.uint8,
                                               device=DEVICE))

import random
from time import sleep
env = ConstantBackgroundRiverraid(render_mode="human")
env.reset()
for i in range(10000):
    _, _, done1, done2, _ = env.step(random.randint(0,5))
    sleep(0.02)
    print(env.get_ram()[38:44])
    if done1 or done2:
        env.reset()