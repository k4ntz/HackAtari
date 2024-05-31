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
    parser.add_argument('-cs', '--color_swaps', default='',
                        help='Colorswaps to be applied to the images.')
    parser.add_argument('-t', '--track', default=False, action="store_true",
                        help='track scores')
    parser.add_argument('-n', '--name', required=True,
                    help='your name')

    args = parser.parse_args()
    
   
    import csv
    import time
  
    gamecnt = 0
    crew = 0
    start_time = time.time()
    print("start_time:", start_time)

    modstring = ""
    for mod in args.modifs:
        modstring += mod+"+"
    data = [[args.game, modstring]]

    color_swaps = None
    if args.color_swaps:
        color_swaps = {}
        color_swaps_str = json.load(open(args.color_swaps))
        for key, val in color_swaps_str.items():
            color_swaps[eval(key)] = eval(val)
    
    duration = 0
    while duration < 5*60:
        print("Elapsed time", duration)
        env = HumanPlayable(args.game, args.modifs, color_swaps)
        crew = env.run()
        duration = time.time() - start_time
        data.append([gamecnt,  crew, int(duration)])
        env.reset()
        gamecnt += 1
    import os
    if not os.path.isfile(f"results_{args.name}.csv"):
        with open(f"results_{args.name}", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
    else:
        with open(f"results_{args.name}.csv", 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
    env.close()
