# HackAtari

HackAtari is an object-centric extension of the Atari Learning Environment (ALE), built on top of [OCAtari](https://github.com/k4ntz/OC_Atari). It enables **custom environment modifications** and **dynamic reward functions** for Atari games in research and experimentation.

> **OCAtari** provides object-based observations for Atari 2600 games, supporting research in interpretable RL, object-centric RL, and environment hacking.

---

## Features
- **Plug-and-play Atari environments** with OpenAI Gym interface.
- **Object-centric observations** (RAM, pixel, or object states).
- **Easy-to-use modification system:** change rules, visuals, or add obstacles per game.
- **Custom reward function injection** (Python scripts, at runtime).
- **Dopamine-style frame pooling** for observation stability.
- **Fully human-playable:** interactive play mode (keyboard controls via Pygame).
- **Game mode and difficulty selection** (where supported by ALE).

---

## Installation

1. **Install OCAtari:**
   - Follow instructions in [OCAtari repository](https://github.com/k4ntz/OC_Atari),
     or install via pip:
     ```bash
     pip install ocatari
     ```

2. **Install HackAtari:**
   - Recommended: install from PyPI:
     ```bash
     pip install hackatari
     ```
   - Or, for development:
     ```bash
     git clone https://github.com/k4ntz/HackAtari
     cd HackAtari
     pip install -e .
     ```

---

## Usage

You can use HackAtari environments just like standard OpenAI Gym environments. The included `run.py` demonstrates launching both standard and modified games, with options for human or random agent play.

**Example usage:**

```bash
# Start normal Freeway (random agent)
python run.py -g Freeway

# Human mode, normal Freeway
python run.py -g Freeway -hu

# Cars of color Black
python run.py -g Freeway -m all_black_cars

# Freeway with stopping mode #3 (static cars)
python run.py -g Freeway -m stop_all_cars
```

## Evaluating Agents with HackAtari Modifications

HackAtari makes it easy to evaluate RL agents not only on standard Atari games, but also on custom or challenging **modified environments**. This enables robust evaluation of generalization, interpretability, and adaptability in RL research.

### Steps to Evaluate Agents using the eval script

0. **Install the needed additional packages**
```bash
pip install torch
pip install stable_baselines3
pip install rliable
```

1. **Choose Your Modification(s)**  
See [modification_list.md](modification_list.md) or print them in code:
```python
from hackatari.core import HackAtari
env = HackAtari('Pong')
print(env.available_modifications)
```

2. **Use the eval script**

```bash
# Start with the baseline performance 
python eval.py -g Freeway -a path_to_model

# Evaluate the same model on a modified version of the game
python eval.py -g Freeway -a path_to_model -m all_black_cars

# Save results in a json file
python eval.py -g Freeway -a path_to_model -m all_black_cars -out results.json
```

For more parameters, check the eval script.


## Game Modifications

* See: modification_list.md or the online docs.
* In code: Use `env.available_modifications` to print all modifications and their documentation for a given game.

**Example**
```python
from hackatari.core import HackAtari
env = HackAtari('Freeway')
print(env.available_modifications)
```

## Human Play Mode

Enable human-interactive play (keyboard) with the `-hu` flag in `run.py`, or directly instantiate `hackatari.core.HumanPlayable` in your code.

**Keyboard controls:**
- **P**: Pause/Resume
- **Q**: Quit
- **R**: Reset
- **Arrow keys / action keys**: Move or interact (varies per game)

---

## Custom Reward Functions

Override the environment's reward signal by providing your own reward function script (see `examples/` for a template). Pass the path via `-r` in `run.py` or as the `rewardfunc_path` argument:

```python
env = HackAtari('Pong', rewardfunc_path='path_to_my_custom_reward.py')
```

The reward function should be a Python function:

```python
def reward_function(env) -> float:
    # Your custom reward logic here
    return 0.0
``` 

## Documentation & Further Resources

- [Documentation](https://hackatari.readthedocs.io/en/latest/)
- [List of modifications](modification_list.md)
- [OCAtari documentation](https://oc-atari.readthedocs.io/en/latest/)

For in-depth API and modding reference, see the above links.

## Citation

If you use HackAtari in academic work, please cite the corresponding paper:

TBH

## License

HackAtari is open source under the MIT License (see [`LICENSE`](LICENSE)).
