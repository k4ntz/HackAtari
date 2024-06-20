# HackAtari

This repository relies on OCAtari, a fork of the OpenAI Gym Atari environment. 
The OCAtari repository can be found [here](https://github.com/k4ntz/OC_Atari).


## Installation
To install the OCAtari environment, please follow the instructions in the OCAtari repository,
or simply run the following command:
```bash
pip install ocatari
```
To install the hackatari environment, run 
```bash
pip install hackatari
```

or clone this repository and run the following command:
```bash
git clone https://github.com/k4ntz/HackAtari
cd HackAtari
pip install -e .
```

## Usage
To use the HackAtari environment, simply import it as you would any other OpenAI Gym environment:
You can run the `run.py` file to start the original game or any of the modified versions.
E.g.:
```python
python run.py -g Freeway # Starts normal Freeway (random agent)
python run.py -g Freeway -hu # Starts Freeway with the cars being invisible (interactive/human playing mode)
python run.py -g Freeway -m color8 # Starts Freeway with the cars of color #8 being (i.e. invisible) (random agent)
python run.py -g Freeway -m stop3 # Starts Freeway with stopping mode #3 (i.e. static cars) (random agent)
python run.py -g Seaquest -m oxygen disable_enemies gravity # Starts Seaquest with infinite oxygen, no enemy, gravity (random agent)
python run.py -g Kangaroo -m random_init disable_monkeys # Starts Kangaroo with random initial floor and no monkeys (random agent)
```

See [the documentation](https://hackatari.readthedocs.io/en/latest/)
or [this markdown file](modification_list.md) for more information on the available modifications.

## Cite our work
```bibtex
@article{delfosse2024hackatari,
  title={HackAtari: Atari Learning Environments for Robust and Continual Reinforcement Learning},
  author={Delfosse, Quentin and Bl{\"u}ml, Jannis and Gregori, Bjarne and Kersting, Kristian},
  journal={arXiv preprint arXiv:2406.03997},
  year={2024}
}
```