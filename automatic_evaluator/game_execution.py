from hackatari import HackAtari
import numpy as np
import torch
import gymnasium as gym
from ocatari.utils import load_agent
import os

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


def eval_run(game='pong',
        agents = [],
        modifications = [],
        rewardfunc_path = None,
        dopamine_pooling = False,
        game_mode = 0,
        difficulty = 0,
        render_mode = "None",
        obs_mode = "dqn",
        mode = "ram",
        hud = False,
        renderc_oc_overlay = True,
        buffer_window_size = 4,
        frameskip = 4,
        repeat_action_probability = 0.25,
        full_action_space = False,
        episodes = 1,
    ):
    """Main function to run HackAtari experiments with different agents."""
    # Initialize environment
    env = HackAtari(
        game,
        modifications,
        rewardfunc_path,
        dopamine_pooling=dopamine_pooling,
        game_mode=game_mode,
        difficulty=difficulty,
        render_mode=render_mode,
        obs_mode=obs_mode,
        mode=mode,
        hud=hud,
        render_oc_overlay=renderc_oc_overlay,
        buffer_window_size=buffer_window_size,
        frameskip=frameskip,
        repeat_action_probability=repeat_action_probability,
        full_action_space=full_action_space,
    )

    avg_results = []
    std_results = []
    total_runs = []

    # Iterate through all agent models
    for agent_path in agents:
        agent, policy = load_agent(agent_path, env, "cpu")
        print(f"Loaded agent from {agent_path}")

        rewards = []
        for episode in range(episodes):
            obs, _ = env.reset()
            done = False
            episode_reward = 0

            while not done:
                action = policy(torch.Tensor(obs).unsqueeze(0))[0]
                obs, reward, terminated, truncated, _ = env.step(action)
                episode_reward += reward
                done = terminated or truncated

            rewards.append(episode_reward)
            print(f"Episode {episode + 1}: Reward = {episode_reward}")

        avg_reward = np.mean(rewards)
        std_reward = np.std(rewards)
        avg_results.append(avg_reward)
        std_results.append(std_reward)
        total_runs.append(episodes)

        print("\nSummary:")
        print(f"Agent: {agent_path}")
        print(f"Total Episodes: {episodes}")
        print(f"Average Reward: {avg_reward:.2f}")
        print(f"Standard Deviation: {std_reward:.2f}")
        print(f"Min Reward: {np.min(rewards)}")
        print(f"Max Reward: {np.max(rewards)}")
        print("--------------------------------------")

    # Compute overall statistics
    total_avg, total_std = combine_means_and_stds(
        avg_results, std_results, total_runs)
    print("------------------------------------------------")
    print(f"Overall Average Reward: {total_avg:.2f}")
    print(f"Overall Standard Deviation: {total_std:.2f}")
    print("------------------------------------------------")

    env.close()
