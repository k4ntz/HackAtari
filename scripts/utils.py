import argparse
import sys
from hackatari.core import _available_modifications


class HackAtariArgumentParser(argparse.ArgumentParser):
    def parse_args(self, args=None, namespace=None):
        # Check if `-h` or `--help` is in the arguments
        if args is None:
            args = sys.argv[1:]
        if '-h' in args or '--help' in args:
            if not '-g' in args or '--game' in args:
                print("Call the script with a given game to get a list of available modifications.")
            else:
                print(_available_modifications(args[args.index('-g') + 1]))
                print("\n provide -h (or --help) without a game argument for the original help message.")
                exit(0)

        # Call the original `parse_args` method to display the default help
        return super().parse_args(args, namespace)
