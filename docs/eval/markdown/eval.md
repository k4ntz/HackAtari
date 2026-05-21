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
