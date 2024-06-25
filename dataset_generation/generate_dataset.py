#!/usr/bin/env python
# coding: utf-8

import random
# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
from copy import deepcopy
from os import path, makedirs
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import torch
from datetime import datetime
# sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))) # noqa
from hackatari.core import HackAtari
from ocatari.utils import load_agent, parser
# from ocatari.vision.space_invaders import objects_colors
import pickle
from tqdm import tqdm
import argparse


parser = argparse.ArgumentParser(description='HackAtari generate_dataset.py Argument Setter')
parser.add_argument('-g', '--game', type=str, default="Seaquest",
                    help='Game to be run')
# Argument to enable gravity for the player.
parser.add_argument('-m', '--modifs', nargs='+', default=[],
                    help='List of the modifications to be brought to the game')

#parser.add_argument('-hu', '--human', action='store_true',
#                    help='Let user play the game.')
parser.add_argument('-s', '--seed', type=int, default=0,
                    help='Make the generation deterministic.')
parser.add_argument('-p', '--picture', type=int, default=0,
                    help='Takes a picture after the number of steps provided.')
parser.add_argument('-cs', '--color_swaps', default='',
                    help='Colorswaps to be applied to the images.')
parser.add_argument('-rf','--reward_function', type=str, default='', 
                    help="Replace the default reward fuction with new one in path rf")
parser.add_argument('-a','--agent', type=str, default='', 
                    help="Path to the cleanrl trained agent to be loaded.")
parser.add_argument('-c','--creator', type=str, default='', 
                    help="Name of the creator of this dataset")
args = parser.parse_args()

# Init the environment
env = HackAtari(args.game, args.modifs, args.reward_function, args.color_swaps, render_mode="human", obs_mode="dqn")

# Set up an agent
if args.agent:
    agent = load_agent(args.agent, env.action_space.n)
    print(f"Loaded agents from {args.agent}")

# make environment deterministic
env.action_space.seed(args.seed)
np.random.seed(args.seed)
torch.manual_seed(args.seed)
os.environ['PYTHONHASHSEED'] = str(args.seed)
torch.use_deterministic_algorithms(True)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False
random.seed(args.seed)
#set_random_seed(args.seed)
env.env.seed(args.seed)
env.env.action_space.seed(args.seed)
env.env.seed(args.seed)
# Init an empty dataset
game_nr = 0
turn_nr = 0
dataset = {"index": [], "obs": [], "action": [], "obs_after_action": [], "reward": [], "original_reward": [], "done" : []}

obs, info = env.reset()

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")



# Generate 10,000 samples
for i in tqdm(range(10000)):
    state = env.get_rgb_state
    # frames.append(state)
    
    if args.agent:
        action = agent.draw_action(env.dqn_obs)
    else:    
        action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)

    state2 = env.get_rgb_state

    step = f"{'%0.5d' % (game_nr)}_{'%0.5d' % (turn_nr)}"
    dataset["index"].append(step)
    dataset["obs"].append(state.flatten().tolist())
    dataset["action"].append(action)
    dataset["obs_after_action"].append(state2.flatten().tolist())
    dataset["reward"].append(reward)
    import ipdb; ipdb.set_trace()
    dataset["original_reward"].append(env.org_reward_step)
    dataset["done"].append(terminated or truncated)
    turn_nr = turn_nr + 1

    # if a game is terminated, restart with a new game and update turn and game counter
    if terminated or truncated:
        obs, info = env.reset()
        turn_nr = 0
        game_nr = game_nr + 1

    ## The interval defines how often images are saved as png files in addition to the dataset
    ## if i % opts.interval == 0:
        # print("-"*50)
        # print(f"Frame {i}")
        # print("-"*50)
        # fig, axes = plt.subplots(1, 2)
        # for obs, objects_list, title, ax in zip([obs,obs2], [env.objects, env.objects_v], ["ram", "vis"], axes):
        #     print(f"{title}: ", sorted(objects_list, key=lambda o: str(o)))
        #     for obj in objects_list:
        #         opos = obj.xywh
        #         ocol = obj.rgb
        #         sur_col = make_darker(ocol, 0.2)
        #         mark_bb(obs, opos, color=sur_col)
        #         # mark_point(obs, *opos[:2], color=(255, 255, 0))
        #     ax.set_xticks([])
        #     ax.set_yticks([])
        #     ax.imshow(obs)
        #     ax.set_title(title)
        # plt.suptitle(f"frame {i}", fontsize=20)
        # plt.show()
        # fig2 = plt.figure()
        # ax2 = fig2.add_subplot(1, 1, 1)
        # for obj in env.objects:
        #     opos = obj.xywh
        #     ocol = obj.rgb
        #     sur_col = make_darker(ocol, 0.8)
        #     mark_bb(obs3, opos, color=sur_col)
        # ax2.imshow(obs3)
        # ax2.set_xticks([])
        # ax2.set_yticks([])
        # plt.show()
        # fig3 = plt.figure()
        # ax3 = fig3.add_subplot(1, 1, 1)
        # for obj in env.objects_v:
        #     opos = obj.xywh
        #     ocol = obj.rgb
        #     sur_col = make_darker(ocol, 0.8)
        #     mark_bb(obs4, opos, color=sur_col)
        # ax3.imshow(obs4)
        # ax3.set_xticks([])
        # ax3.set_yticks([])
        # plt.show()
env.close()

df = pd.DataFrame(dataset, columns=['index', 'obs', 'action', 'obs_after_action', "reward", "original_reward", "done"])

# Metadata dictionary
metadata = {
    'dataset_name': f"HackAtari-DS",
    'game': args.game,
    'modification': args.modifs,
    'reward_function': args.reward_function,
    'agent': args.agent,
    'agent_type': "If an agent is given (see above), this agent is used to play the game. Random if no agent was given.",
    'created_by': args.creator,
    'creation_date': dt_string,
    'seed': args.seed,
    'description': 'This dataset was describes an agent playing a HackAtari game variant.',
    'source': 'Generated manually by letting the agent play on the HackAtari game variant, described by the game name and modifications above. \
       An alternative reward_function (see above) can be given.',
    'num_rows': len(df),
    'num_columns': len(df.columns),
    'column_names': list(df.columns),
    'data_types': df.dtypes.astype(str).to_dict(),
    'obs': "A 210x160x3 RGB image as a flatten list",
    'action': f"describes the action taken in this state. Actions are {env._env.env.env.get_action_meanings()}",
    'obs_after_action': "describes the resulting state after taking the action in the state above",
    'reward': "Describes the reward given for the action a in state s",
    'original_reward': "If an alternative reward function was given, original_reward describe the default reward, else it is 0",
    'done': "Is one if the action ended the game",
    'missing_values': df.isnull().sum().to_dict(),
    'transformations': 'None',
    'license': 'CC BY 4.0',
    'version': '1.0.0'
}

# Save metadata to a JSON file


makedirs("data/datasets/", exist_ok=True)
makedirs("data/datasets/ALE", exist_ok=True)
prefix = f"{args.game}_dqn" if args.agent else f"{args.game}_random" 
df.to_csv(f"data/datasets/{prefix}.csv", index=False)
df.to_pickle(f"data/datasets/{prefix}.pkl")
with open(f'data/datasets/{prefix}_metadata.json', 'w') as f:
    json.dump(metadata, f, indent=4)


print(f"Finished {args.game}")
