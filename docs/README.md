# HackAtari Documentation Compiler
Short guide on how to compile the documentation


## Install dependencies
from within the docs folder:
```sh
pip install -r requirements.txt
```

## Generate the docs
To compile the games, run:

```sh
sphinx-apidoc -o hackatari/games ../hackatari/games
```

To create the html files:
```sh
make html
```