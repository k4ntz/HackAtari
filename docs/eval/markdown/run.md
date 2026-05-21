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
