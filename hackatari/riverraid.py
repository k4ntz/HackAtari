import pygame
from ocatari.core import OCAtari, DEVICE
import numpy as np
import torch
import cv2


class ConstantBackgroundRiverraid(OCAtari):
    def __init__(self, env_name="RiverraidDeterministic-v0", mode="raw", hud=False, obs_mode="dqn", *args, **kwargs):
        self.render_mode = kwargs["render_mode"] if "render_mode" in kwargs else None
        super().__init__(env_name, mode, hud, obs_mode, *args, **kwargs)
    
    def alter_ram(self):
        ram = self.get_ram()
        self.set_ram(55, 255) # avoid spending fuel
        for i in range(6):
            obj_type = ram[32 + i]
            anchor = ram[20 + i]
            if obj_type == 9 and (2 < anchor < 8): # house
                self.set_ram(20+i, random.choice([0, 1, 8, 9]))  # setting the grass
            elif obj_type not in [0, 1, 2, 3, 9, 4] and not (2 < anchor < 8): # other than house
                self.set_ram(20+i, random.randint(3, 6))  # setting the grass
            self.set_ram(14+i, 69)  # setting the grass
            self.set_ram(44+i, 0)
            self.set_ram(38+i, 35)
            if ram[32+i] == 8:
                self.set_ram(32+i, 0) # remove bridge

    def _step_ram(self, *args, **kwargs):
        self.alter_ram()
        toret = super()._step_ram(*args, **kwargs)
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
from ocatari.utils import load_agent, parser, make_deterministic
env = ConstantBackgroundRiverraid(render_mode="human")
dqn_agent = load_agent("../OC_Atari/models/Riverraid/dqn.gz", env.action_space.n)
env.reset()
for i in range(10000):
    # action = random.randint(0,5)
    action = dqn_agent.draw_action(env.dqn_obs)
    _, _, done1, done2, _ = env.step(action)
    sleep(0.01)
    # print(env.get_ram()[38:44])
    if done1 or done2:
        env.reset()