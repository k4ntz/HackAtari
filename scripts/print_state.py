import time
import random
import ipdb
from matplotlib import pyplot as plt
import sys
import os
import numpy as np
# import pathlib
sys.path.insert(0, '../../')  # noqa

from hackatari import HackAtari
"""
set the ram and see whats changed
"""

env_id = "Boxing"
obs_mode = "dqn"
seed = 42
frameskip = 1
modifs = ["switch_p"]

# Seeding
os.environ['PYTHONHASHSEED'] = str(seed)
# torch.use_deterministic_algorithms(args.torch_deterministic)
# torch.backends.cudnn.deterministic = args.torch_deterministic
# torch.backends.cudnn.benchmark = False
# torch.cuda.manual_seed_all(args.seed)
random.seed(seed)
np.random.seed(seed)

env = HackAtari(env_id, hud=False, modifs=modifs, render_mode="rgb_array", mode="ram",
                render_oc_overlay=False, obs_mode=obs_mode, frameskip=1, create_buffer_stacks=["ori"])


env.action_space.seed(seed)

observation, info = env.reset(seed=seed)
observation, reward, terminated, truncated, info = env.step(0)


for _ in range(100):
    action = 1  # pick random action
    obs, reward, truncated, terminated, info = env.step(action)

obs1 = obs[0]
print("---")

obs_mode = "masked_dqn_pixels"

env = HackAtari(env_id, hud=False, modifs=modifs,  render_mode="rgb_array", mode="ram",
                render_oc_overlay=False, obs_mode=obs_mode, frameskip=1, create_buffer_stacks=["ori"])

env.action_space.seed(seed)

observation, info = env.reset(seed=seed)
observation, reward, terminated, truncated, info = env.step(0)


for _ in range(100):
    action = 1  # pick random action
    obs, reward, truncated, terminated, info = env.step(action)

obs2 = obs[0]

print("---")

obs_mode = "masked_dqn_bin"

env = HackAtari(env_id, hud=False,  modifs=modifs, render_mode="rgb_array", mode="ram",
                render_oc_overlay=False, obs_mode=obs_mode, frameskip=1, create_buffer_stacks=["ori"])

env.action_space.seed(seed)

observation, info = env.reset(seed=seed)
observation, reward, terminated, truncated, info = env.step(0)


for _ in range(100):
    action = 1  # pick random action
    obs, reward, truncated, terminated, info = env.step(action)

obs3 = obs[0]

print("---")

obs_mode = "obj"

env = HackAtari(env_id, hud=False,  modifs=modifs, render_mode="rgb_array", mode="ram",
                render_oc_overlay=False, obs_mode=obs_mode, frameskip=1, create_buffer_stacks=["ori"])

env.action_space.seed(seed)

observation, info = env.reset(seed=seed)
observation, reward, terminated, truncated, info = env.step(0)


for _ in range(100):
    action = 1  # pick random action
    obs, reward, truncated, terminated, info = env.step(action)

obs4 = obs

obs_mode = "ori"

env = HackAtari(env_id, hud=False,  modifs=modifs, render_mode="rgb_array", mode="ram",
                render_oc_overlay=False, obs_mode=obs_mode, frameskip=1, create_buffer_stacks=["ori"])

env.action_space.seed(seed)

observation, info = env.reset(seed=seed)
observation, reward, terminated, truncated, info = env.step(0)


for _ in range(100):
    action = 1  # pick random action
    obs, reward, truncated, terminated, info = env.step(action)

obs5 = obs


# Plot the difference as a grayscale image

fig, axes = plt.subplots(1, 1, figsize=(10, 10))

axes.imshow(obs1, cmap="gray")
axes.set_title("")

# axes[1].imshow(obs2, cmap="gray")
# axes[1].set_title("Masked")

# axes[2].imshow(obs3, cmap="gray")
# axes[2].set_title("Abstraction Visualization")

# axes[3].imshow(obs4, cmap="gray")
# axes[3].set_title("OBJ")

axes.axis("off")
plt.savefig("dqn.svg", format="svg", bbox_inches="tight")

fig, axes = plt.subplots(1, 1, figsize=(10, 10))

axes.imshow(obs2, cmap="gray")
axes.set_title("")

axes.axis("off")
plt.savefig("pixels.svg", format="svg", bbox_inches="tight")

fig, axes = plt.subplots(1, 1, figsize=(10, 10))

axes.imshow(obs3, cmap="gray")
axes.set_title("")

axes.axis("off")
plt.savefig("bins.svg", format="svg", bbox_inches="tight")

fig, axes = plt.subplots(1, 1, figsize=(10, 10))

axes.imshow(obs4, cmap="gray")
axes.set_title("")

axes.axis("off")
plt.savefig("obj.svg", format="svg", bbox_inches="tight")

fig, axes = plt.subplots(1, 1, figsize=(10, 10))

axes.imshow(obs5, cmap="gray")
axes.set_title("")

axes.axis("off")
plt.savefig("ori.svg", format="svg", bbox_inches="tight")


env.close()
