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
    parser.add_argument("-a", "--agent", type=str, default="",
                        help="Path to the trained agent to be loaded.")
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

    pygame.init()

    # Load agent
    agent, policy = load_agent(args.agent, env, "cpu")
    print(f"Loaded agent from {args.agent}")

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
    min_reward = np.min(rewards)
    max_reward = np.max(rewards)

    print("\nSummary:")
    print(f"Total Episodes: {args.episodes}")
    print(f"Average Reward: {avg_reward:.2f}")
    print(f"Standard Deviation: {std_reward:.2f}")
    print(f"Min Reward: {min_reward}")
    print(f"Max Reward: {max_reward}")

    env.close()
