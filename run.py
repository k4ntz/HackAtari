from hackatari import HackAtari, HumanPlayable
import random
import numpy as np
import cv2
import sys

import matplotlib.pyplot as plt
from hackatari.utils import load_color_swaps
from ocatari.utils import load_agent


def save_upsampled(rgb_arrays, k=4, l=4):
    augs = []
    for rgb_array in rgb_arrays:
        aug = np.repeat(np.repeat(rgb_array, k, axis=0), l, axis=1)[:,:,[2,1,0]]
        augs.append(aug)
    aug = np.average(augs, 0).astype(int)
    # plt.imshow(aug)
    # plt.show()
    cv2.imwrite("screenshot.png", aug, [cv2.IMWRITE_PNG_COMPRESSION, 0])
    print("Screenshot saved as screenshot.png")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='HackAtari run.py Argument Setter')

    parser.add_argument('-g', '--game', type=str, default="Seaquest",
                        help='Game to be run')

    # Argument to enable gravity for the player.
    parser.add_argument('-m', '--modifs', nargs='+', default=[],
                        help='List of the modifications to be brought to the game')
    
    parser.add_argument('-hu', '--human', action='store_true',
                        help='Let user play the game.')
    
    parser.add_argument('-p', '--picture', type=int, default=0,
                        help='Takes a picture after the number of steps provided.')
    parser.add_argument('-cs', '--color_swaps', default='',
                        help='Colorswaps to be applied to the images.')
    parser.add_argument('-rf','--reward_function', type=str, default='', 
                        help="Replace the default reward fuction with new one in path rf")
    parser.add_argument('-a','--agent', type=str, default='', 
                        help="Path to the cleanrl trained agent to be loaded.")

    args = parser.parse_args()
    obss = []

    color_swaps = load_color_swaps(args.color_swaps)
    
    if args.human:
        env = HumanPlayable(args.game, args.modifs, args.reward_function, color_swaps)
        env.run()
    else:        
        env = HackAtari(args.game, args.modifs, args.reward_function, color_swaps, render_mode="human", obs_mode="dqn")
        if args.agent:
            agent = load_agent(args.agent, env.action_space.n)
            print(f"Loaded agents from {args.agent}")
        obs, _ = env.reset()
        done = False
        nstep = 1
        while not done:
            if args.agent:
                action = agent.draw_action(env.dqn_obs)
            else:    
                action = env.action_space.sample()
            obs, reward, terminated, truncated, _ = env.step(action)
            if reward and args.reward_function:
                print(reward)
            if terminated or truncated:
                env.reset()
            if nstep == args.picture:
                obss.append(obs)
                save_upsampled(obss)
                exit()
            elif args.picture - nstep < 4:
                obss.append(obs)
            # if nstep % 100 == 0:
            #     print(".", end="", flush=True)
            nstep += 1
            env.render()
        env.close()