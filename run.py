from hackatari import HackAtari, HumanPlayable


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

    args = parser.parse_args()

    if args.human:
        env = HumanPlayable(args.game, args.modifs)
        env.run()
    else:
        env = HackAtari(args.game, args.modifs, render_mode="human")
        env.reset()
        done = False
        env.render()
        while not done:
            action = env.action_space.sample()
            _, _, terminated, truncated, _ = env.step(action)
            if terminated or truncated:
                import ipdb; ipdb.set_trace()
                env.reset()
        env.close()