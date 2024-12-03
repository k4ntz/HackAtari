#!/usr/bin/env python
# coding: utf-8

import random

# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
from copy import deepcopy
from os import makedirs
import json
import pandas as pd
import numpy as np
import os
import torch
from datetime import datetime

# sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))) # noqa
from hackatari.core import HackAtari
from ocatari.utils import load_agent, parser

# from ocatari.vision.space_invaders import objects_colors
from tqdm import tqdm
from utils import get_dtypes, get_obj_props
import argparse

parser = argparse.ArgumentParser(description="HackAtari run.py Argument Setter")
parser.add_argument("-g", "--game", type=str, default="Seaquest", help="Game to be run")
parser.add_argument(
    "-m",
    "--modifs",
    nargs="+",
    default=[],
    help="List of the modifications to be brought to the game",
)
parser.add_argument(
    "-s", "--seed", type=int, default=0, help="Make the generation deterministic."
)
parser.add_argument(
    "-p",
    "--picture",
    type=int,
    default=0,
    help="Takes a picture after the number of steps provided.",
)
parser.add_argument(
    "-cs", "--color_swaps", default="", help="Colorswaps to be applied to the images."
)
parser.add_argument(
    "-rf",
    "--reward_function",
    type=str,
    default="",
    help="Replace the default reward fuction with new one in path rf",
)
parser.add_argument(
    "-a",
    "--agent",
    type=str,
    default="",
    help="Path to the cleanrl trained agent to be loaded.",
)
parser.add_argument(
    "-c", "--creator", type=str, default="", help="Name of the creator of this dataset"
)
parser.add_argument(
    "-f",
    "--frames",
    type=int,
    default=10000,
    help="How many frames should be generated.",
)
parser.add_argument(
    "-e",
    "--epsilon",
    type=float,
    default=0.1,
    help="The random probability of the state being added to the dataset.",
)

args = parser.parse_args()

# Init the environment
env = HackAtari(
    args.game,
    args.modifs,
    args.reward_function,
    args.color_swaps,
    render_mode="human",
    obs_mode="dqn",
    mode="vision",
)

# Set up an agent
if args.agent:
    agent = load_agent(args.agent, env.action_space.n)
    print(f"Loaded agents from {args.agent}")

# make environment deterministic
env.action_space.seed(args.seed)
np.random.seed(args.seed)
torch.manual_seed(args.seed)
os.environ["PYTHONHASHSEED"] = str(args.seed)
torch.use_deterministic_algorithms(True)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
random.seed(args.seed)
# set_random_seed(args.seed)
env.env.seed(args.seed)
env.env.action_space.seed(args.seed)
env.env.seed(args.seed)
# Init an empty dataset
game_nr = 0
turn_nr = 0
dataset = {
    "index": [],
    "obs": [],
    "action": [],
    "next_obs": [],
    "obs_dqn": [],
    "next_obs_dqn": [],
    "objects": [],
    "next_objects": [],
    "reward": [],
    "original_reward": [],
    "done": [],
}

obs, info = env.reset()

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")


# Generate 10,000 samples
counts = 0
with tqdm(total=args.frames) as pbar:
    while counts < args.frames:
        selected = (
            random.random() < args.epsilon
        )  # and same_object_list(env.objects, env.objects_v)
        if selected:
            state = deepcopy(torch.tensor(env.get_rgb_state))
            dqn_state = deepcopy(env.dqn_obs[0])
            objects = deepcopy(env.objects)

        if args.agent:
            action = agent.draw_action(env.dqn_obs)
        else:
            action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        step = f"{'%0.5d' % (game_nr)}_{'%0.5d' % (turn_nr)}"

        if selected:
            dataset["index"].append(step)
            dataset["obs"].append(state)
            dataset["obs_dqn"].append(dqn_state)
            dataset["action"].append(action.item())
            dataset["next_obs"].append(torch.tensor(env.get_rgb_state))
            dataset["next_obs_dqn"].append(env.dqn_obs[0])
            dataset["objects"].append(objects)
            dataset["next_objects"].append(env.objects)
            dataset["reward"].append(reward)
            dataset["original_reward"].append(env.org_reward)
            dataset["done"].append(terminated or truncated)
            pbar.update(1)
            counts += 1

        turn_nr = turn_nr + 1

        # if a game is terminated, restart with a new game and update turn and game counter
        if terminated or truncated:
            obs, info = env.reset()
            turn_nr = 0
            game_nr = game_nr + 1

env.close()


df = pd.DataFrame(
    dataset,
    columns=[
        "index",
        "obs",
        "next_obs",
        "obs_dqn",
        "next_obs_dqn",
        "objects",
        "next_objects",
        "action",
        "reward",
        "original_reward",
        "done",
    ],
)

df[["action", "reward", "original_reward", "done"]] = df[
    ["action", "reward", "original_reward", "done"]
].apply(pd.to_numeric, downcast="float")
# Metadata dictionary
metadata = {
    "dataset_name": "HackAtari-DS",
    "game": args.game,
    "modification": args.modifs,
    "reward_function": args.reward_function,
    "agent": args.agent,
    "agent_type": "If an agent is given (see above), this agent is used to play the game. Random if no agent was given.",
    "created_by": args.creator,
    "creation_date": dt_string,
    "seed": args.seed,
    "epsilon": "The random probability of the state being added to the dataset.",
    "epsilon_value": args.epsilon,
    "description": "This dataset was describes an agent playing a HackAtari game variant.",
    "source": "Generated manually by letting the agent play on the HackAtari game variant, described by the game name and modifications above. \
       An alternative reward_function (see above) can be given.",
    "num_rows": len(df),
    "num_columns": len(df.columns),
    "column_names": list(df.columns),
    "data_types": get_dtypes(df),
    "objects_props": get_obj_props(df["objects"]),
    "objects_props_description": "The objects properties are extracted from the objects list in the dataset. Not all properties are listed, the most useful ones only",
    "obs": "A 210x160x3 RGB image as a torch tensor of the current state",
    "obs_dqn": "A 4x84x84 grayscaled image (as torch tensor) of the last four states used by DQN agents to learn",
    "action": f"describes the action taken in this state. Actions are {env._env.env.env.get_action_meanings()}",
    "next_obs": "the resulting RGB state after taking the action in the state above",
    "next_obs_dqn": "the resulting Black and White DQN-style state after taking the action in the state above",
    "reward": "Describes the reward given for the action a in state s",
    "original_reward": "If an alternative reward function was given, original_reward describe the default reward, else it is 0",
    "done": "Is one if the action ended the game",
    "missing_values": df.isnull().sum().to_dict(),
    "transformations": "None",
    "license": "CC BY 4.0",
    "version": "1.0.0",
}

# Save metadata to a JSON file

basepath = "data/datasets"
makedirs(basepath, exist_ok=True)
makedirs(f"{basepath}/ALE", exist_ok=True)
prefix = f"{args.game}_dqn_agent" if args.agent else f"{args.game}_random_agent"
# df.to_csv(f"data/datasets/{prefix}.csv", index=False)
df_dqn_obs = deepcopy(df)
df.drop(columns=["obs_dqn", "next_obs_dqn"], inplace=True)
df_dqn_obs.drop(columns=["obs", "next_obs"], inplace=True)
df.to_pickle(f"{basepath}/{prefix}_rgb.pkl.gz", compression="gzip")
df_dqn_obs.to_pickle(f"{basepath}/{prefix}_dqn.pkl.gz", compression="gzip")
with open(f"{basepath}/{prefix}_metadata.json", "w") as f:
    json.dump(metadata, f, indent=4)


print(f"Finished {args.game}, stored in data/datesets/")
