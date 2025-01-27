from hackatari import HackAtari, HumanPlayable
import numpy as np
import cv2
import pygame
import torch
import gymnasium as gym
from ocatari.utils import load_agent
import os
import time
import argparse
from utils import HackAtariArgumentParser

# Disable graphics window (SDL) for headless execution
os.environ["SDL_VIDEODRIVER"] = "dummy"


def combine_means_and_stds(mu_list, sigma_list, n_list):
    """
    Combine multiple means and standard deviations using their respective sample sizes.

    Args:
        mu_list (list): List of means.
        sigma_list (list): List of standard deviations.
        n_list (list): List of sample sizes.

    Returns:
        tuple: Combined mean and combined standard deviation.
    """
    if not (len(mu_list) == len(sigma_list) == len(n_list)):
        raise ValueError("All input lists must have the same length.")

    total_n = sum(n_list)
    combined_mean = sum(n * mu for mu, n in zip(mu_list, n_list)) / total_n
    combined_variance = sum(
        n * (sigma**2 + (mu - combined_mean)**2)
        for mu, sigma, n in zip(mu_list, sigma_list, n_list)
    ) / total_n
    combined_std = np.sqrt(combined_variance)

    return combined_mean, combined_std


def main():
    """Main function to run HackAtari experiments with different agents."""
    parser = HackAtariArgumentParser(description="HackAtari Experiment Runner")

    # Game and environment parameters
    parser.add_argument("-g", "--game", type=str,
                        default="Seaquest", help="Game to be run")
    parser.add_argument("-obs", "--obs_mode", type=str,
                        default="dqn", help="Observation mode (ori, dqn, obj)")
    parser.add_argument("-w", "--window", type=int, default=4,
                        help="Buffer window size (default = 4)")
    parser.add_argument("-f", "--frameskip", type=int, default=4,
                        help="Frames skipped after each action (default = 4)")
    parser.add_argument("-dp", "--dopamine_pooling", action='store_true',
                        help="Enable dopamine-like frameskipping")
    parser.add_argument("-m", "--modifs", nargs="+",
                        default=[], help="List of modifications to apply")
    parser.add_argument("-rf", "--reward_function", type=str,
                        default="", help="Custom reward function path")
    parser.add_argument("-a", "--agents", nargs='+',
                        required=True, help="List of trained agent model paths")
    parser.add_argument("-mo", "--game_mode", type=int,
                        default=0, help="Alternative ALE game mode")
    parser.add_argument("-d", "--difficulty", type=int,
                        default=0, help="Alternative ALE difficulty")
    parser.add_argument("-e", "--episodes", type=int,
                        default=10, help="Number of episodes to run per agent")

    args = parser.parse_args()


    # Initialize environment
    env = HackAtari(
        args.game,
        args.modifs,
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

    all_episodes_avg_results = []
    all_episodes_std_results = []
    all_episodes_avg_times = []
    all_episodes_std_times = []
    all_episodes_avg_steps = []
    all_episodes_std_steps = []
    total_runs = []

    # Iterate through all agent models
    for agent_path in args.agents:
        agent, policy = load_agent(agent_path, env, "cpu")
        print(f"Loaded agent from {agent_path}")

        all_episodes_cumulative_rewards = []
        all_episodes_cumulative_times = []
        all_episodes_cumulative_actions = []
        all_episodes_cumulative_steps = []
        for episode in range(args.episodes):
            obs, _ = env.reset()
            done = False
            current_episodes_rewards = []
            current_episodes_times = []
            current_episodes_actions = []
            
            while not done:
                step_start_time = time.time()

                action = policy(torch.Tensor(obs).unsqueeze(0))[0]
                obs, reward, terminated, truncated, _ = env.step(action)
                current_episodes_rewards.append(reward)
                done = terminated or truncated

                step_end_time = time.time()
                current_episodes_times.append(step_end_time - step_start_time)
                
                current_episodes_actions.append(action)

            episodes_cumulative_reward = sum(current_episodes_rewards)            
            all_episodes_cumulative_rewards.append(episodes_cumulative_reward)
            
            episodes_cumulative_time = sum(current_episodes_times)
            all_episodes_cumulative_times.append(episodes_cumulative_time)

            episodes_cumulative_action = {ac:current_episodes_actions.count(ac) for ac in current_episodes_actions}
            episodes_cumulative_action = dict(sorted(episodes_cumulative_action.items()))
            all_episodes_cumulative_actions.append(episodes_cumulative_action)

            episodes_cumulative_step = len(current_episodes_times)
            all_episodes_cumulative_steps.append(episodes_cumulative_step)

            print(f"Episode {episode + 1}: Reward = {episodes_cumulative_reward}, Time = {episodes_cumulative_time:.2f} seconds with {episodes_cumulative_step} steps and actions: {episodes_cumulative_action}")

        all_episodes_avg_reward = np.mean(all_episodes_cumulative_rewards)
        all_episodes_std_reward = np.std(all_episodes_cumulative_rewards)
        all_episodes_avg_results.append(all_episodes_avg_reward)
        all_episodes_std_results.append(all_episodes_std_reward)
        
        all_episodes_avg_time = np.mean(all_episodes_cumulative_times)
        all_episodes_std_time = np.std(all_episodes_cumulative_times)
        all_episodes_avg_times.append(all_episodes_avg_time)
        all_episodes_std_times.append(all_episodes_std_time)

        all_episodes_avg_step = np.mean(all_episodes_cumulative_steps)
        all_episodes_std_step = np.std(all_episodes_cumulative_steps)
        all_episodes_avg_steps.append(all_episodes_avg_step)
        all_episodes_std_steps.append(all_episodes_std_step)

        total_runs.append(args.episodes)

        print("\nSummary:")
        print(f"Agent: {agent_path}")
        print(f"Total Episodes: {args.episodes}")
        print(f"Average Reward: {all_episodes_avg_reward:.2f}")
        print(f"Reward Standard Deviation: {all_episodes_std_reward:.2f}")
        print(f"Min Reward: {np.min(all_episodes_cumulative_rewards)}")
        print(f"Max Reward: {np.max(all_episodes_cumulative_rewards)}")
        print(f"Average Time: {all_episodes_avg_time:.2f} seconds")
        print(f"Time Standard Deviation: {all_episodes_std_time:.2f} seconds")
        print(f"Min Time: {np.min(all_episodes_cumulative_times):.2f} seconds")
        print(f"Max Step: {np.max(all_episodes_cumulative_times):.2f} seconds")
        print(f"Average Step: {all_episodes_avg_step:.2f} steps")
        print(f"Step Standard Deviation: {all_episodes_std_step:.2f} steps")
        print(f"Min Step: {np.min(all_episodes_cumulative_steps)} steps")
        print(f"Max Step: {np.max(all_episodes_cumulative_steps)} steps")
        print("--------------------------------------")

    # Compute overall statistics
    total_avg, total_std = combine_means_and_stds(all_episodes_avg_results, all_episodes_std_results, total_runs)
    total_avg_time, total_std_time = combine_means_and_stds(all_episodes_avg_times, all_episodes_std_times, total_runs)
    total_avg_step, total_std_step = combine_means_and_stds(all_episodes_avg_steps, all_episodes_std_steps, total_runs)
    print("------------------------------------------------")
    print(f"Overall Average Reward: {total_avg:.2f}, Time: {total_avg_time:.2f} seconds and {total_avg_step:.2f} steps")
    print(f"Overall Reward Standard Deviation: {total_std:.2f}, Time Standard Deviation: {total_std_time:.2f} seconds, Step Standard Deviation: {total_std_step:.2f}")
    print("------------------------------------------------")

    env.close()

""" metric ideas:
TODO CSV/JSON Logs: Save rewards, actions, and episode data to files for offline analysis.
"""

if __name__ == "__main__":
    main()

