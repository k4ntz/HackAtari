def load_color_swaps(file_path: str) -> dict:
    color_swaps = {}
    if file_path:
        with open(file_path) as f:
            for line in f.readlines():
                key, val = line.strip().split(":")
                color_swaps[eval(key)] = eval(val)
    return color_swaps
