from hackatari import HackAtari, HumanPlayable
import json


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Seaquest Game Argument Setter')

    # Argument to set the oxygen mode
    # Options:
    # - 0: easy mode: no oxygen usage
    # - 1: Default - standard game mode: with standard oxygen usage
    # - 2: hard mode: oxygen decreases twice as fast
    parser.add_argument('-g', '--game', type=str, default="Seaquest",
                        help='Game to be run')

    # Argument to enable gravity for the player.
    parser.add_argument('-m', '--modifs', nargs='+', default=[],
                        help='List of the modifications to be brought to the game')
    
    parser.add_argument('-hu', '--human', action='store_true',
                        help='Let user play the game.')
    parser.add_argument('-cs', '--color_swaps', default='',
                        help='Colorswaps to be applied to the images.')

    args = parser.parse_args()
    color_swaps = None
    if args.color_swaps:
        color_swaps = {}
        color_swaps_str = json.load(open(args.color_swaps))
        for key, val in color_swaps_str.items():
            color_swaps[eval(key)] = eval(val)
    
    if args.human:
        env = HumanPlayable(args.game, args.modifs, color_swaps)
        env.run()
    else:
        env = HackAtari(args.game, args.modifs, color_swaps, render_mode="human")
        env.reset()
        done = False
        env.render()
        while not done:
            action = env.action_space.sample()
            # import ipdb; ipdb.set_trace()
            obs, _, terminated, truncated, _ = env.step(action)
            if terminated or truncated:
                env.reset()
            # import matplotlib.pyplot as plt
            # plt.imshow(obs)
            # plt.show()
        env.close()