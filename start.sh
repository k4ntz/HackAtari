# git clone

git clone git@github.com:k4ntz/HackAtari.git

cd HackAtari/
git checkout study

python -m venv env

source env/bin/activate
pip install ocatari
pip install "gymnasium[atari, accept-rom-license]"
