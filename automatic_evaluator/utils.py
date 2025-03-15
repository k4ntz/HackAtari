
from hackatari import HackAtari, HumanPlayable
import numpy as np
import cv2
import pygame
import torch
import gymnasium as gym
from ocatari.utils import load_agent
import os
import aim

# Hyperparameters


def eval_withRun(game:str, agents:list, modifs:list=[], game_mode:int=0, difficulty:int=0, obs_mode:str="dqn", window:int=4, frameskip:int = 4, dopamine_pooling:bool=False, reward_function:str="", episodes:int=10):
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
    
    # Initialize Aim
    run = aim.Run(experiment=game)

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
            
            run.track(name="reward", value=episode_reward, step=episode+1)
            #print(f"Episode {episode + 1}: Reward = {episode_reward}")

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
        run.track(name="avg_reward", value=avg_reward)
        run.track(name="std_reward", value=std_reward)
        run.track(name="min_reward", value=np.min(rewards))
        run.track(name="max_reward", value=np.max(rewards))
        #run.track(name="total_episodes", value=episodes)
        #run.track(name="agent", value=agent_path)
        print("--------------------------------------")

    # # Compute overall statistics
    # total_avg, total_std = combine_means_and_stds(
    #     avg_results, std_results, total_runs)
    # print("------------------------------------------------")
    # print(f"Overall Average Reward: {total_avg:.2f}")
    # print(f"Overall Standard Deviation: {total_std:.2f}")
    # print("------------------------------------------------")

    env.close()