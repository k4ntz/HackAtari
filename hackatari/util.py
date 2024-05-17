import json


def load_color_swaps(file_path: str) -> dict:
    if file_path:
        color_swaps = {}
        color_swaps_str = json.load(open(file_path))
        for key, val in color_swaps_str.items():
            color_swaps[eval(key)] = eval(val)
    else:
        return {}
