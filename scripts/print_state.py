import random
import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
import cv2
from ocatari.utils import load_agent
from hackatari import HackAtari

"""
Script to visualize how RAM (or other) observations change across different modes in HackAtari.
Allows command-line configuration for environment, observation mode, modifications, steps, etc.
"""


def parse_args():
    parser = argparse.ArgumentParser(
        description="Visualize RAM/obs changes across HackAtari modes."
    )
    parser.add_argument('-g', '--game', type=str,
                        default='Pong', help='Atari environment/game name')
    parser.add_argument('-m', '--modification', type=str,
                        default='', help='Environment modification (or empty)')
    parser.add_argument('-o', '--obs_mode', type=str, default='ori',
                        help='Observation mode (e.g. dqn, obj, ori, ram)')
    parser.add_argument('-f', '--frameskip', type=int,
                        default=4, help='Frameskip (default: 4)')
    parser.add_argument('-s', '--seed', type=int, default=42,
                        help='Random seed (default: 42)')
    parser.add_argument('--steps', type=int, default=90,
                        help='Number of steps (default: 90)')
    parser.add_argument('--action', type=int, default=0,
                        help='Action to repeat (default: 0/NOOP)')
    parser.add_argument('--save_dir', type=str, default='.',
                        help='Directory to save images')
    return parser.parse_args()


def run_environment(env_id, obs_mode, seed, frameskip, modifs, steps, action):
    """Runs the HackAtari environment and returns the final merged observation."""
    env = HackAtari(
        env_id, hud=False, modifs=modifs, render_mode="human", mode="ram",
        render_oc_overlay=True, obs_mode=obs_mode, frameskip=frameskip, create_buffer_stacks=["ori"]
    )
    env.action_space.seed(seed)
    obs = env.reset(seed=seed)

    # Print available actions
    for i, act in enumerate(env.unwrapped.get_action_meanings()):
        print(f"Action {i}: {act}")
    obss = []
    for f in range(steps):
        action = env.action_space.sample()
        obs, _, _, _, _ = env.step(action)
        if f % frameskip == 0:
            obss.append(obs)
    env.close()
    return merge_last_observations(obss)


def merge_last_observations(obss):
    """
    Merges the last 3 observations with transparency to create a single image showing recent movement.
    """
    merged_obs = np.zeros_like(obss[0], dtype=np.float32)
    alphas = [0.2, 0.3, 0.5]  # Transparency values
    for alpha, obs in zip(alphas, obss[-3:]):
        merged_obs = cv2.addWeighted(
            merged_obs, 1 - alpha, obs.astype(np.float32), alpha, 0)
    merged_obs = np.clip(merged_obs, 0, 255).astype(np.uint8)
    return merged_obs


def save_image(obs, filename):
    """
    Save an observation as an image file (PNG).
    """
    # Optionally upscale for visibility
    obs_up = np.repeat(np.repeat(obs, 3, axis=0), 3, axis=1)
    cv2.imwrite(filename, cv2.cvtColor(obs_up, cv2.COLOR_BGR2RGB),
                [cv2.IMWRITE_PNG_COMPRESSION, 0])
    print(f"Image saved as {filename}")


def main():
    args = parse_args()
    # Handle multiple modifications, comma-separated
    modifs = [m for m in args.modification.split(',') if m]
    os.makedirs(args.save_dir, exist_ok=True)
    os.environ['PYTHONHASHSEED'] = str(args.seed)
    random.seed(args.seed)
    np.random.seed(args.seed)
    # Run environment

    merged_obs = run_environment(
        args.game, args.obs_mode, args.seed, args.frameskip, modifs, args.steps, args.action
    )
    filename = os.path.join(
        args.save_dir, f"{args.game}_{args.obs_mode}_{'_'.join(modifs) or 'nomod'}.png"
    )
    save_image(merged_obs, filename)


if __name__ == "__main__":
    main()
