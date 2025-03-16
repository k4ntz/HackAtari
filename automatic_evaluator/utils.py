
from hackatari import HackAtari, HumanPlayable
import numpy as np
import cv2
import pygame
import torch
import gymnasium as gym
from ocatari.utils import load_agent
import os
from aim import Run


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

# Hyperparameters


def eval_withAimRun(game: str, agents: list, modifs: list = [], game_mode: int = 0, difficulty: int = 0, obs_mode: str = "dqn", window: int = 4, frameskip: int = 4, dopamine_pooling: bool = False, reward_function: str = "", episodes: int = 10):
    # Initialize environment
    env = HackAtari(
        game,
        modifs,
        reward_function,
        dopamine_pooling=dopamine_pooling,
        game_mode=game_mode,
        difficulty=difficulty,
        render_mode="None",
        obs_mode=obs_mode,
        mode="ram",
        hud=False,
        render_oc_overlay=True,
        buffer_window_size=window,
        frameskip=frameskip,
        repeat_action_probability=0.25,
        full_action_space=False,
    )

    # preapre run
    try: 
        if run: run.close()
    except NameError:
        pass
    
    
    hparams = {
            'game': game,
            'modifs': '+'.join(modifs), 
            'game_mode': game_mode,
            'difficulty': difficulty,
            'obs_mode': obs_mode,
            'window': window,
            'frameskip': frameskip,
            'dopamine_pooling': dopamine_pooling,
            'reward_function': reward_function,
            'episodes': episodes
    }
    
    avg_results = []
    std_results = []
    total_runs = []

    # Iterate through all agent models
    for agent_path in agents:
        _, policy = load_agent(agent_path, env, "cpu")
        print(f"Loaded agent from {agent_path}")
        
        run = Run(experiment=f"Eval: {game}")
        agent_name = "/".join(agent_path.split("/")[-2:])
        
        
        _context = {"agent": agent_name}
        hparams['agent'] = agent_name
        run['hparams'] = hparams
    
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

            run.track(name="Episode Reward", value=episode_reward, step=episode+1, context={"agent": agent_name})
            # print(f"Episode {episode + 1}: Reward = {episode_reward}")

        avg_reward = np.mean(rewards)
        std_reward = np.std(rewards)
        avg_results.append(avg_reward)
        std_results.append(std_reward)
        total_runs.append(episodes)

        # print("\nSummary:")
        # print(f"Agent: {agent_path}")
        # print(f"Total Episodes: {args.episodes}")
        # print(f"Average Reward: {avg_reward:.2f}")
        # print(f"Standard Deviation: {std_reward:.2f}")
        # print(f"Min Reward: {np.min(rewards)}")
        # print(f"Max Reward: {np.max(rewards)}")
        run.track(name="Total Episodes", value=episodes)
        run.track(name="Average Reward", value=avg_reward, context={"modifs": hparams['modifs']})
        run.track(name="Standard Reward", value=std_reward, context={"modifs": hparams['modifs']})
        run.track(name="Min Reward", value=np.min(rewards))
        run.track(name="Max Reward", value=np.max(rewards))
        # run.track(name="total_episodes", value=episodes)
        # run.track(name="agent", value=agent_path)
        
        print("--------------------------------------")
        run.close()

    # Compute overall statistics
    # total_avg, total_std = combine_means_and_stds(
    #     avg_results, std_results, total_runs)
    # print("------------------------------------------------")
    # print(f"Overall Average Reward: {total_avg:.2f}")
    # print(f"Overall Standard Deviation: {total_std:.2f}")
    # run.track(name="Overall Average Reward", value=total_avg)
    # run.track(name="Overall Standard Deviation", value=total_std)
    # print("------------------------------------------------")

    env.close()
    
    print("Done.")