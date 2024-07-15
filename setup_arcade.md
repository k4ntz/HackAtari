# Setup Guide for the Arcade

## Setup checked on
    - OS: Ubuntu
    - Python 11
    - numpy 1.26.3

## Installation

### install packages:
```
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11
sudo apt install python3.11-venv
sudo apt install git
sudo apt install dialog
```

### create folder and activate venv:
```
cd ~
mkdir arcade
cd arcade
mkdir venv
python3.11 -m venv ~/arcade/venv/
source ~/arcade/venv/bin/activate
pip install numpy==1.26.3
pip install --upgrade pip
```

### install torchvision 
cpu:
```
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
```
gpu:
```
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### install OC Atari:
```
cd ~/arcade
git clone https://github.com/k4ntz/OC_Atari
cd OC_Atari
python setup.py install
```

### install Hackatari:
```
cd ~/arcade
git clone https://github.com/k4ntz/HackAtari
cd HackAtari
# ~~python setup.py install~~
pip3 install -e .
cd ~/arcade
```

### rebuild:
```
cd ~/arcade/OC_Atari
python setup.py install
cd ~/arcade/HackAtari
pip3 install -e .
```

### install/accept gymnasium:
```
pip install "gymnasium[atari, accept-rom-license]"
```

### start testrun:
```
cd ~/arcade/HackAtari
python run.py -g Freeway
```

## Configure Controller

### install antimicrox
```
sudo apt install flatpak
sudo apt install gnome-software-plugin-flatpak
flatpak remote-add --if-not-exists flathub https://dl.flathub.org/repo/flathub.flatpakrepo
flatpak install flathub io.github.antimicrox.antimicrox
flatpak run io.github.antimicrox.antimicrox
```

### change selected profiles

add profiles of the Git Repo to the corresponding Controllers.

### check config
open config file: (TODO: check correct config path)
```
TBD /home/hackatari/.var/app/io.github.antimicrox.antimicrox/config
```
check the config file, that the configs are correctly saved (TODO: insert right config lines!)
```
TBD
```
Optional:
change config file to read only

## Autostart

### configure autostart:
add following startscript to system startup:
```
home/hackatari/arcade/HackAtari/start_terminal.sh
```
add following antimicrox run command to system startup:
```
flatpak run io.github.antimicrox.antimicrox
```

Options: 
- Startup Applications Preferences
- systemd

### Change Settings
- change the "Screen Blank"/"Turn off Screen" Setting to "Never"
- activate "Automatic Login" for User

### Add key shortcut
- Strg + M with script: ```home/hackatari/arcade/HackAtari/start_terminal.sh```

## Models

### Add Models:
Modells have to be added at:
```
models/_Gamename_/
```

Warning! The folder names for the games are truncated to delete spaces.
So "Space Invaders" has the Foldername "SpaceInvaders".