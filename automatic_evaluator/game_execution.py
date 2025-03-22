from hackatari import HackAtari
import numpy as np
import torch
from ocatari.utils import load_agent
import os

import time

import eval

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
        log_file = 'logs.json',
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

    if log_file.endswith(".json"):
        log_file = log_file[:-5]
    else:
        print(f"log_file should be in the 'path/to/file.json' format. Exiting the evaluation!")
        return

    if len(log_file) == 0:
        print(f"log_file should be in the 'path/to/file.json' format. Exiting the evaluation!")
        return


    compressed_file = log_file + "_comp.gz"
    log_file = log_file + ".json"
    # Iterate through all agent models
    for agent_path in agents:
        agent, policy = load_agent(agent_path, env, "cpu")
        
        print(f"Runing for episodes: {episodes}")
        for episode in range(episodes):
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

            episode_data = {
                "agent_path": agent_path,
                "current_episodes_rewards": current_episodes_rewards,
                "current_episodes_times": current_episodes_times,
                "current_episodes_actions": current_episodes_actions
            }
            eval.log_episode_data(log_file, episode_data)

    env.close()

    episode_data = eval.read_log_data(log_file)
    eval.print_metrics(episode_data, episodes)
    eval.compress_log_data(log_file, compressed_file)
    os.remove(log_file)
