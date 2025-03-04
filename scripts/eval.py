from hackatari import HackAtari, HumanPlayable
import numpy as np
import cv2
import pygame
import torch
import gymnasium as gym
from ocatari.utils import load_agent
import os
import argparse
import json
from utils import HackAtariArgumentParser
from ocatari_wrappers import BinaryMaskWrapper, PixelMaskWrapper, ObjectTypeMaskWrapper, ObjectTypeMaskPlanesWrapper, PixelMaskPlanesWrapper
from stable_baselines3.common.atari_wrappers import (
    EpisodicLifeEnv,
    FireResetEnv,
    NoopResetEnv,
)
import rliable.metrics as rlm

# Disable graphics window (SDL) for headless execution
os.environ["SDL_VIDEODRIVER"] = "dummy"

# Define human and random scores
human_scores = {
    'Boxing': 12.1, 'Breakout': 30.5, 'Freeway': 29.6, 'Frostbite': 4334.7, 'MsPacman': 6951.6, "Pong": 14.6, "Skiing": -4336.9,
}
random_scores = {
    'Boxing': 0.1, 'Breakout': 1.7, 'Freeway': 0.0, 'Frostbite': 65.2, 'MsPacman': 307.3, "Pong": -20.7, "Skiing": -17098.1
}


def calculate_hns(score, game):
    human_score = human_scores[game]
    random_score = random_scores[game]
    return (score - random_score) / (human_score - random_score)


def main():
    parser = HackAtariArgumentParser(description="HackAtari Experiment Runner")
    parser.add_argument("-g", "--game", type=str,
                        default="Seaquest", help="Game to be run")
    parser.add_argument("-obs", "--obs_mode", type=str,
                        default="dqn", help="Observation mode (ori, dqn, obj)")
    parser.add_argument("-w", "--window", type=int,
                        default=4, help="Buffer window size")
    parser.add_argument("-f", "--frameskip", type=int,
                        default=4, help="Frames skipped after each action")
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
                        default=10, help="Number of episodes per agent")
    parser.add_argument("-wr", "--wrapper", type=str,
                        default="", help="Use a masking wrapper")
    parser.add_argument("-out", "--output", type=str,
                        default="results.json", help="Output file for results")

    args = parser.parse_args()

    env = HackAtari(
        args.game, args.modifs, args.reward_function,
        dopamine_pooling=args.dopamine_pooling, game_mode=args.game_mode,
        difficulty=args.difficulty, render_mode="None", obs_mode=args.obs_mode,
        mode="ram", hud=False, render_oc_overlay=True,
        buffer_window_size=args.window, frameskip=args.frameskip,
        repeat_action_probability=0.25, full_action_space=False,
    )

    if "FIRE" in env.unwrapped.get_action_meanings():
        env = FireResetEnv(env)

    wrapper_mapping = {
        "binary": BinaryMaskWrapper,
        "pixels": PixelMaskWrapper,
        "classes": ObjectTypeMaskWrapper,
        "planes": ObjectTypeMaskPlanesWrapper,
        "pixelplanes": PixelMaskPlanesWrapper,
    }

    if args.wrapper in wrapper_mapping:
        env = wrapper_mapping[args.wrapper](env)
    elif args.wrapper.endswith("+pixels"):
        base_wrapper = args.wrapper.split("+")[0]
        if base_wrapper in wrapper_mapping:
            env = wrapper_mapping[base_wrapper](env, include_pixels=True)

    results = {}

    for agent_path in args.agents:
        agent, policy = load_agent(agent_path, env, "cpu")
        print(f"Loaded agent from {agent_path}")

        rewards = []
        for episode in range(args.episodes):
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
        median_reward = np.median(rewards)
        hns_reward = calculate_hns(avg_reward, args.game)
        iqm_reward = rlm.aggregate_iqm(np.array(rewards))
        hns_iqm = calculate_hns(iqm_reward, args.game)

        results[agent_path] = {
            "obs_mode": args.obs_mode,
            "wrapper": args.wrapper,
            "modifs": args.modifs,
            "episode_rewards": rewards,
            "average_reward": avg_reward,
            "hns_reward": hns_reward,
            "median_reward": median_reward,
            "iqm_reward": iqm_reward,
            "hns_iqm": hns_iqm,
            "std_reward": std_reward,
            "min_reward": np.min(rewards),
            "max_reward": np.max(rewards),
            "total_episodes": args.episodes
        }

        print(f"\nSummary for {agent_path}:")
        print(f"Average Reward: {avg_reward:.2f}")
        print(f"HNS: {hns_reward:.2f}")
        print(f"IQM Reward: {iqm_reward:.2f}")
        print(f"HNS (IQM): {hns_iqm:.2f}")
        print("--------------------------------------")

    with open(args.output, "w") as f:
        json.dump(results, f, indent=4)

    env.close()


if __name__ == "__main__":
    main()
