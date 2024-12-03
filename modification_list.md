# Modified Atari Games

A complete list of all modifications and their corresponding arguments.

This is the list of games we have created new versions and modifications for during the "HackAtari" project. Each file, when started without additional parameters, starts the original game played by the DQN agent.
All modes/hacks/changes can be activated individually or in any combination via the command line.

Use `-hu` to start the game in Human Mode and play the game yourself.


Use `-m` to select the mode you want to play in. All modes/hacks/changes can be activated individually or in any combination by separating with whitespace between them.

**Example**: `python run.py -g Freeway -m c3 sm3 -hu` will run Freeway with all cars being red (`c3`) and stopped (`sm3`) in Human (playable) Mode (`-hu`).

The modes are:

## Boxing:
| Command | Effect                                                                               |
|---------|--------------------------------------------------------------------------------------|
| g       | Enables Gravity pull on the player character                                         |
| db      | Enables drunken boxing mode where the player character staggers in a circular motion |
| oa      | Enables one armed mode where the player character only uses the right arm            |

## Breakout:
| Command | Effect                                        |
|---------|-----------------------------------------------|
| d[r, l] | Set the drift direction "right" or "left"     |
| s[0-2]  | Sets the strenght of the drift, 0 is no drift |

### Note: In Breakout, the drift will not work if human mode is enabled due to issues with the rendering.


## Fishing Derby:
| Command | Effect                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|---------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| sm[0-4] | 0 = default behavior. 1 = x-position of the shark is fixed at 105, which is directly below the enemy player - 2 = x-position of the shark is fixed at 25, which is directly below the player - 3 = the shark teleports from the left to the right and the other way around when x-position 25 or 105 is reached - 4 = the shark moves from the left to the right with a very high velocity. When reaching x-position 120 the shark is set back to x-position 1 and starts to move again in the same speed up way as described. |
| fm[0-3] | = = default behavior. 1 = The x-position of the fish is changed. They are mainly on the player's side. 2 = The x-position of the fish is changed. They are mainly on the enemy's side. 3 = The x-position of the fish is changed. They are in the middle betwen  player and enemy.                                                                                                                                                                                                                                             |

## Freeway:
| Command | Effect                                                                                                                                                               |
|---------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| c[0-8]  | Change the colors of the cars. 0 = standard; 1 = black; 2 = grey; 3 = red; 4 = white; 5 = green; 6 = purple; 7 = blue; 8 = "invisible"                               |
| sm[0-3] | Change the behavior of the cars: 1 = cars stop randomly and drive off again; 2 = all cars stop simultaneously and drive off again simultaneously; 3 = all cars stop. |

## Frostbite:
| Command   | Effect                                                                                                                                                   |
|-----------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| c         | Argument for setting the color of line 1 of the ice floes. The chosen value has to be between 0 and 255. The default value is 12                         |
| l[1-4]    | Argument for choosing a line of ice floes for color changing.                                                                                            |
| c3        | This mode recolors 3 lines at once.                                                                                                                      |
| cui       | Argument for setting the color of the UI for temperature, life and points. The chosen value has to be between 6 and 254. The default value is 0 = white. |
| cfp       | Argument for enabling positional changes to the ice floes. Needs to be set for .fp to haven an effect.                                                   |
| fp[0-255] | Argument for setting the x-position of the ice floes. The input value has to be between 0 and 255.                                                       |
| en[0-3]   | Argument for changing the enemies number. The value has to be between 0 and 3. 0 is the unaltered version.                                               |

## Kangaroo:
| Command | Effect                                  |
|---------|-----------------------------------------|
| f       | Set the starting floor (0, 1, or 2)     |
| dm      | Disable monkeys in the game             |
| dc      | Disable the falling coconut in the game |
| e       | Enable easy mode                        |
| ra      | Rndom difficulty                        |

## MS Pacman
| Command                 | Effect                                                            |
|-------------------------|-------------------------------------------------------------------|
| cg                      | Caged ghosts, ghosts will not leave the middle                    |
| orange, cyan, pink, red | cages ghosts selectivly by color                                  |
| npp[0-4]                | number of available power pills                                   |
| eg                      | ghosts can always be eaten, power pills do nothing                |
| i                       | inverted mode, eating a power pill maked the ghos dangerous again |

## Seaquest
| Command | Effect                           |
|---------|----------------------------------|
| o       | Set the oxygen to unlimited mode |
| de      | disables all enemies             |
| gr      | Enable graxity mode.             |

### Note: If all enemies are disabled, stray projectiles can occure in certain situations which will still kill the player. We haven't found a fix for this.


## Space Invaders:
| Command    | Effect                                                            |
|------------|-------------------------------------------------------------------|
| pos[35-53] | Moves the shields side to side via an offset.                     |
| ds         | Disables all the shields.                                         |
| l, r, m    | disables the shields (left, right, middle) one by one selectively |
| c          | enabled curved shots                                              |

## Tennis
| Command | Effect             |
|---------|--------------------|
| w       | Enables wind drift |