# Readme

## Instructions
1. First install everything by running 
`bash start.sh`
* Should you want to try it on Windows, then look into the bash script and follow the steps to clone and install HackAtari.

2. Next go into the folder, activate the environment

`cd HackAtari;source env/bin/activate`

3. Choose a game from the following
* Boxing
* Freeway
* Pong
* Kangaroo
* SpaceInvaders
* MsPacman

4. Train as long as you want
`python run.py -g [gamename] -hu`

5. Start the game by running
`python run_study.py -g [gamename] -n [yourname]`

When finishing a game, you have to manually close the game window, not the console, to restart the game!

6. Start the same game, now in its new variation
* `python run_study.py -g Boxing -n [yourname] -m one_armed`
* `python run_study.py -g Freeway -n [yourname] -m s2`
* `python run_study.py -g Pong -n [yourname] -m lazy_enemy`
* `python run_study.py -g Kangaroo -n [yourname] -m disable_coconut disable_monkeys`
* `python run_study.py -g SpaceInvaders -n [yourname] -m disable_shields`
* `python run_study.py -g MsPacman -n [yourname] -m change_level3`

7. Send us the result files



