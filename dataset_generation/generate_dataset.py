#!/usr/bin/env python
# coding: utf-8

import random
# appends parent path to syspath to make ocatari importable
# like it would have been installed as a package
import sys
from copy import deepcopy
from os import path, makedirs

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import torch
# sys.path.append(path.dirname(path.dirname(path.abspath(__file__)))) # noqa
from hackatari.core import HackAtari
from ocatari.utils import load_agent, parser, make_deterministic
# from ocatari.vision.space_invaders import objects_colors
import pickle
from tqdm import tqdm

import argparse
parser = argparse.ArgumentParser(description='HackAtari run.py Argument Setter')
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
#s, _ = env.reset(args.seed)
#env.env.envs[0].action_space.seed(args.seed)
#env.env.envs[0].ocatari_env.seed(args.seed)
# Init an empty dataset
game_nr = 0
turn_nr = 0
dataset = {"INDEX": [], "OBS": [], 
           "RAM": [], "HUD": [], "REW": [], "ACT": []}
frames = []
r_objs = []
rewards = []
actions = []

obs, info = env.reset()


# Generate 10,000 samples
for i in tqdm(range(10000)):
    state = env.get_rgb_state
    frames.append(state)
    r_objs.append(deepcopy(env.objects))
    
    if args.agent:
        action = agent.draw_action(obs)
    else:    
        action = env.action_space.sample()
    obs, reward, terminated, truncated, info = env.step(action)
    # make a short print every 1000 steps
    # if i % 1000 == 0:
    #    print(f"{i} done")

    step = f"{'%0.5d' % (game_nr)}_{'%0.5d' % (turn_nr)}"
    dataset["INDEX"].append(step)
    dataset["OBS"].append(state.flatten().tolist())
    dataset["RAM"].append([x for x in sorted(env.objects, key=lambda o: str(o)) if x.hud == False])
    dataset["HUD"].append([x for x in sorted(env.objects, key=lambda o: str(o)) if x.hud == True])
    dataset["ACT"].append(action)
    dataset["REW"].append(reward)
    turn_nr = turn_nr + 1

    # if a game is terminated, restart with a new game and update turn and game counter
    if terminated or truncated:
        obs, info = env.reset()
        turn_nr = 0
        game_nr = game_nr + 1

    if i % 1 == 0:
        env.render()
    # The interval defines how often images are saved as png files in addition to the dataset
    # if i % opts.interval == 0:
        """
        print("-"*50)
        print(f"Frame {i}")
        print("-"*50)
        fig, axes = plt.subplots(1, 2)
        for obs, objects_list, title, ax in zip([obs,obs2], [env.objects, env.objects_v], ["ram", "vis"], axes):
            print(f"{title}: ", sorted(objects_list, key=lambda o: str(o)))
            for obj in objects_list:
                opos = obj.xywh
                ocol = obj.rgb
                sur_col = make_darker(ocol, 0.2)
                mark_bb(obs, opos, color=sur_col)
                # mark_point(obs, *opos[:2], color=(255, 255, 0))
            ax.set_xticks([])
            ax.set_yticks([])
            ax.imshow(obs)
            ax.set_title(title)
        plt.suptitle(f"frame {i}", fontsize=20)
        plt.show()
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(1, 1, 1)
        for obj in env.objects:
            opos = obj.xywh
            ocol = obj.rgb
            sur_col = make_darker(ocol, 0.8)
            mark_bb(obs3, opos, color=sur_col)
        ax2.imshow(obs3)
        ax2.set_xticks([])
        ax2.set_yticks([])
        plt.show()
        fig3 = plt.figure()
        ax3 = fig3.add_subplot(1, 1, 1)
        for obj in env.objects_v:
            opos = obj.xywh
            ocol = obj.rgb
            sur_col = make_darker(ocol, 0.8)
            mark_bb(obs4, opos, color=sur_col)
        ax3.imshow(obs4)
        ax3.set_xticks([])
        ax3.set_yticks([])
        plt.show()
        """
env.close()

df = pd.DataFrame(dataset, columns=['INDEX', 'RAM', 'HUD', 'OBS'])
makedirs("data/datasets/", exist_ok=True)
prefix = f"{args.game}_dqn" if args.agent else f"{args.game}_random" 
df.to_csv(f"data/datasets/{prefix}.csv", index=False)
pickle.dump(rewards, open(f"data/datasets/{prefix}_rewards.pkl", "wb"))
pickle.dump(actions, open(f"data/datasets/{prefix}_actions.pkl", "wb"))
pickle.dump(r_objs, open(f"data/datasets/{prefix}_objects_r.pkl", "wb"))
pickle.dump(frames, open(f"data/datasets/{prefix}_frames.pkl", "wb"))
print(f"Finished {args.game}")
