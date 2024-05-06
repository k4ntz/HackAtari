from hackatari import HackAtari, HumanPlayable
import random
import numpy as np
import cv2


def save_upsampled(rgb_array, k=4, l=4):
    aug = np.repeat(np.repeat(rgb_array, k, axis=0), l, axis=1)[:,:,[2,1,0]]
    cv2.imwrite("screenshot.png", aug, [cv2.IMWRITE_PNG_COMPRESSION, 0])
    print("Screenshot saved as screenshot.png")

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
    
    parser.add_argument('-p', '--picture', type=int, default=0,
                        help='Takes a picture after the number of steps provided.')

    args = parser.parse_args()

    if args.human:
        env = HumanPlayable(args.game, args.modifs)
        env.run()
    else:
        env = HackAtari(args.game, args.modifs, render_mode="human")
        env.reset()
        done = False
        env.render()
        nstep = 1
        while not done:
            action = env.action_space.sample()
            obs, _, terminated, truncated, _ = env.step(action)
            if terminated or truncated:
                env.reset()
            if nstep == args.picture:
                save_upsampled(obs)
                exit()
            nstep += 1
        env.close()