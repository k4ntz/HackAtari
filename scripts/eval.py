from hackatari import HackAtari, HumanPlayable
import numpy as np
import cv2
import pygame
import torch
import gymnasium as gym
from ocatari.utils import load_agent

# Set SDL to False (disable graphics window)
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"


def combine_means_and_stds(mu_list, sigma_list, n_list):
    """
    Combine multiple means and standard deviations using their sample sizes.

    Args:
        mu_list (list): List of means.
        sigma_list (list): List of standard deviations.
        n_list (list): List of sample sizes.

    Returns:
        tuple: Combined mean and combined standard deviation.
    """
    # Validate inputs
    if not (len(mu_list) == len(sigma_list) == len(n_list)):
        raise ValueError("All input lists must have the same length.")

    # Total sample size
    total_n = sum(n_list)

    # Combined mean
    combined_mean = sum(n * mu for mu, n in zip(mu_list, n_list)) / total_n

    # Combined variance
    combined_variance = sum(
        n * (sigma**2 + (mu - combined_mean)**2)
        for mu, sigma, n in zip(mu_list, sigma_list, n_list)
    ) / total_n

    # Combined standard deviation
    combined_std = np.sqrt(combined_variance)

    return combined_mean, combined_std


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="HackAtari run.py Argument Setter")

    parser.add_argument("-g", "--game", type=str,
                        default="Seaquest", help="Game to be run")
    parser.add_argument("-obs", "--obs_mode", type=str,
                        default="dqn", help="The observation mode (ori, dqn, obj)")
    parser.add_argument("-w", "--window", type=int, default=4,
                        help="The buffer window size (default = 4)")
    parser.add_argument("-f", "--frameskip", type=int, default=4,
                        help="The frames skipped after each action + 1 (default = 4)")
    parser.add_argument("-dp", "--dopamine_pooling", type=bool, default=False,
                        help="Use dopamine like frameskipping (default = False)")
    parser.add_argument("-m", "--modifs", nargs="+", default=[],
                        help="List of the modifications to be brought to the game")
    parser.add_argument("-sm", "--switch_modifs", nargs="+", default=[],
                        help="List of modifications after a certain frame")
    parser.add_argument("-sf", "--switch_frame", type=int, default=0,
                        help="Frame threshold for applying switch_modifs")
    parser.add_argument("-rf", "--reward_function", type=str, default="",
                        help="Replace default reward function with a custom one")
    # Add a parameter for a list of models
    parser.add_argument(
        "-a",
        '--agents',
        nargs='+',  # Accepts one or more arguments as a list
        required=True,
        help="List of model names to use (e.g., model1 model2 model3)"
    )

    parser.add_argument("-mo", "--game_mode", type=int,
                        default=0, help="Alternative ALE game mode")
    parser.add_argument("-d", "--difficulty", type=int,
                        default=0, help="Alternative ALE difficulty")
    parser.add_argument("-e", "--episodes", type=int,
                        default=10, help="Number of episodes to be played")

    args = parser.parse_args()

    # Initialize environment
    env = HackAtari(
        args.game,
        args.modifs,
        args.switch_modifs,
        args.switch_frame,
        args.reward_function,
        dopamine_pooling=args.dopamine_pooling,
        game_mode=args.game_mode,
        difficulty=args.difficulty,
        render_mode="None",
        obs_mode=args.obs_mode,
        mode="ram",
        hud=False,
        render_oc_overlay=True,
        buffer_window_size=args.window,
        frameskip=args.frameskip,
        repeat_action_probability=0.25,
        full_action_space=False,
    )

    avg_results = []
    std_results = []
    total_runs = []
    for pth in args.agents:
        # Load agent
        agent, policy = load_agent(pth, env, "cpu")
        print(f"Loaded agent from {pth}")

        rewards = []
        total_rewards = []
        env._env.sdl = False

        for episode in range(args.episodes):
            obs, _ = env.reset()
            done = False
            episode_reward = 0

            while not done:
                dqn_obs = torch.Tensor(obs).unsqueeze(0)
                action = policy(dqn_obs)[0]
                obs, reward, terminated, truncated, info = env.step(action)
                episode_reward += reward
                done = terminated or truncated

            rewards.append(episode_reward)
            print(f"Episode {episode + 1}: Reward = {episode_reward}")

        avg_reward = np.mean(rewards)
        std_reward = np.std(rewards)
        avg_results.append(avg_reward)
        std_results.append(std_reward)
        total_runs.append(args.episodes)
        min_reward = np.min(rewards)
        max_reward = np.max(rewards)

        print("\nSummary:")
        print(f"Total Episodes: {args.episodes}")
        print(f"Average Reward: {avg_reward:.2f}")
        print(f"Standard Deviation: {std_reward:.2f}")
        print(f"Min Reward: {min_reward}")
        print(f"Max Reward: {max_reward}")
        print("____________________________________")

    a, b = combine_means_and_stds(avg_results, std_results, total_runs)

    print("------------------------------------------------")
    print(f"Total Average Reward: {a:.2f}")
    print(f"Total Standard Deviation: {b:.2f}")
    print("------------------------------------------------")

    env.close()
