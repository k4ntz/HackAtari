import random
import os
import numpy as np
import matplotlib.pyplot as plt
from hackatari import HackAtari
import ocatari_wrappers as ow

"""
Script to explore how RAM values change across different observation modes in HackAtari.
Runs the Kangaroo environment in different modes (DQN, Object, Original) and visualizes the results.
"""

# Configuration
ENV_ID = "FishingDerby"
SEED = 42
FRAMESKIP = 4
MODIFICATIONS = [""]
# Different observation modes to compare
OBSERVATION_MODES = ["ori"]
wrapper = ""
# Seeding for reproducibility
os.environ['PYTHONHASHSEED'] = str(SEED)
random.seed(SEED)
np.random.seed(SEED)


def run_environment(env_id, obs_mode, seed, frameskip, modifs):
    """Runs the HackAtari environment with the specified parameters and returns the final observation."""
    env = HackAtari(
        env_id, hud=False, modifs=modifs, render_mode="human", mode="ram",
        render_oc_overlay=True, obs_mode=obs_mode, frameskip=frameskip, create_buffer_stacks=["ori"]
    )

    env.action_space.seed(seed)
    env.reset(seed=seed)

    if wrapper == "binary":
        env = ow.BinaryMaskWrapper(env)
    elif wrapper == "pixels":
        env = ow.PixelMaskWrapper(env)
    elif wrapper == "classes":
        env = ow.ObjectTypeMaskWrapper(env)
    elif wrapper == "planes":
        env = ow.ObjectTypeMaskPlanesWrapper(env)
    elif wrapper == "binary+pixels":
        env = ow.BinaryMaskWrapper(env, include_pixels=True)
    elif wrapper == "pixels+pixels":
        env = ow.PixelMaskWrapper(env, include_pixels=True)
    elif wrapper == "classes+pixels":
        env = ow.ObjectTypeMaskWrapper(env, include_pixels=True)
    elif wrapper == "planes+pixels":
        env = ow.ObjectTypeMaskPlanesWrapper(env, include_pixels=True)

    # Simulate 100 steps with a fixed action
    for _ in range(90):
        action = 1  # Fixed action for consistency
        obs, _, _, _, _ = env.step(action)

    env.close()

    import ipdb
    ipdb.set_trace()
    if obs_mode == "dqn":
        obs = obs[0]
    return obs


def save_and_display_image(obs, filename):
    """Displays and saves an observation as an image."""
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(obs, cmap="gray")
    ax.set_title(filename[:-4])  # Remove extension for title
    ax.axis("off")
    plt.savefig(filename, format="svg", bbox_inches="tight", dpi=600)
    plt.show()


# Run environments for different observation modes and store results
observations = {mode: run_environment(
    ENV_ID, mode, SEED, FRAMESKIP, MODIFICATIONS) for mode in OBSERVATION_MODES}

# Save and display images for each observation mode
for mode, obs in observations.items():
    save_and_display_image(obs, f"{ENV_ID}_{mode}_{MODIFICATIONS[0]}.svg")
