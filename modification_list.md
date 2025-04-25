# Modified Atari Games

A complete list of all modifications and their corresponding arguments.

This is the list of games we have created new versions and modifications for during the "HackAtari" project. Each file, when started without additional parameters, starts the original game played by the DQN agent.
All modes/hacks/changes can be activated individually or in any combination via the command line.

Use `-hu` to start the game in Human Mode and play the game yourself.


Use `-m` to select the mode you want to play in. All modes/hacks/changes can be activated individually or in any combination by separating with whitespace between them.

**Example**: `python run.py -g Freeway -hu -m stop_all_cars` will run Freeway with all cars being red (`c3`) and stopped (`sm3`) in Human (playable) Mode (`-hu`).

The modes are:

## Amidar:
| Command | Effect                                                                               |
|---------|--------------------------------------------------------------------------------------|
| pig_enemies           | Changes enemies into pigs |
| paint_roller_player   | Changes player into paint roller |
| unlimited_lives       | The player never loses any lives |

## Asterix:
| Command | Effect                                                                               |
|---------|--------------------------------------------------------------------------------------|
| obelix                | Changes playmode to obelix (more difficult) |
| set_consumable_1      | Changes consumable into pink objects (100points) |
| set_consumable_2      | Changes consumable into shields (200points) |
| unlimited_lives       | Do not decrease lives |
| even_lines_free       | Even lines are free |
| odd_lines_free        | Odd lines are free |

## Atlantis:
| Command | Effect                                                                               |
|---------|--------------------------------------------------------------------------------------|
| no_last_line                | Remove enemies from the last (lowest) line |
| jets_only                   | Replace all enemies with Bandit Bombers |
| random_enemies              | Randomly assign enemy types |
| speed_mode_slow             | Set speed to 2 |
| speed_mode_medium           | Set speed to 4 |
| speed_mode_fast             | Set speed to 6 |
| speed_mode_ultrafast        | Set speed to 8 |

## Bankheist:
| Command | Effect                                                                               |
|---------|--------------------------------------------------------------------------------------|
| unlimited_gas           | Do not decrease the gas |
| no_police               | Do not spawn police |
| only_police             | Directly spawn police |
| random_city             | Start in a random city |
| revisit_city            | Allows player to revisit previous cities |

## Boxing:
| Command | Effect                                                                               |
|---------|--------------------------------------------------------------------------------------|
| gravity        | Enables Gravity pull on the player character |
| drunken_boxing | Enables drunken boxing mode where the player character staggers in a circular motion |
| one_armed      | Enables one armed mode where the player character only uses the right arm |
| color_player_black | Set player color to black (also works with white, red, blue and green) |
| color_enemy_black | Set enemy color to black (also works with white, red, blue and green) |
| switch_position | Set player position to the lower right corner |

## Breakout:
| Command | Effect                                        |
|---------|-----------------------------------------------|
| right_drift     | Set the drift direction "right" |
| left_drift      | Set the drift direction "right" |
| gravity         | Set drift direction downwards |
| inverse_gravity | Set drift dirtection upwards |
| color_player_and_ball_black | Set color of player and ball (also works with white, red, blue and green) |
| color_all_blocks_black | Set color of all blocks (also works with white, red, blue and green)  |

## Carnival:
| Command | Effect                                                                               |
|---------|--------------------------------------------------------------------------------------|
| no_flying_ducks                | Ducks in the last row disappear instead of turning into flying ducks. |
| unlimited_ammo                 | Ammunition doesn't decrease. |
| missile_speed_small_increase   | The projectiles fired from the players are faster (slow increase). |
| missile_speed_medium_increase  | The projectiles fired from the players are faster (medium increase). |
| missile_speed_large_increase   | The projectiles fired from the players are faster (large increase). |

## ChopperCommand:
### Untested due to the update of OCAtari to ns_representations

| Command | Effect                                                                               |
|---------|--------------------------------------------------------------------------------------|
| delay_shots           | Puts time delay between shots. |
| no_enemies            | Removes all enemies from the game. |
| no_radar              | Removes the radar content. |
| invisible_player      | Makes the player invisible. |
| color_black           | Changes the background and enemies' color to black. (also works with white, red, blue and green). |

## DonkeyKong:

| Command | Effect                                                                               |
|---------|--------------------------------------------------------------------------------------|
| no_barrel           | Removes barrels from the game. |
| unlimited_time      | Provides unlimited time for the player. |
| random_start        | Randomly choose between 10 possible starting positions. |

## DoubleDunk:

| Command | Effect                                                                               |
|---------|--------------------------------------------------------------------------------------|
| player_color_white | Set player teams color to white. (also works with green, red, yellow, purple and blue)
| enemy_color_white | Set enemy teams color to white. (also works with green, red, yellow, purple and blue)

## Fishing Derby:

| Command | Effect                                                                               |
|---------|--------------------------------------------------------------------------------------|
| shark_teleport        | Teleports the shark in the line |
| shark_speed_mode      | Makes the shark very very fast |
| fish_on_player_side   | All fish are on the player's side |
| fish_in_middle        | All fish are in the middle.|

## Freeway:

| Command | Effect                                                                               |
|---------|--------------------------------------------------------------------------------------|
| stop_random_car       | Stops a random car with a biased probability for a certain time. |
| stop_all_cars         | Stops all cars on the side of the board. |
| align_all_cars        | Align all cars so they move in a line. |
| all_black_cars        | All cars are black. (also works with white, red, blue and green)|


## Frostbite:
| Command | Effect                                                                               |
|---------|--------------------------------------------------------------------------------------|
| ui_color_black            | Sets ui color to black. (also works with red). |
| reposition_floes_easy     | Make ice shelves static (easy mode). |
| reposition_floes_medium   | Make ice shelves static (medium mode). |
| reposition_floes_hard     | Make ice shelves static (hard mode).|
| no_birds                  | Removes all birds (and fishes?) |
| few_enemies               | Increase enemies slightly |
| many_enemies              | Increase enemies to a maximum|


## Kangaroo:
| Command | Effect                                  |
|---------|-----------------------------------------|
| set_kangaroo_position_floor1  | Set the starting floor (0, 1, or 2)     |
| randomize_kangaroo_position   | Random starting floor |
| disable_monkeys               | Disable monkeys in the game             |
| disable_coconut               | Disable the falling coconut in the game |
| disable_thrown_coconut        | Disable the throwing coconut in the game |
| change_level_0                | Set starting level (0, 1, or 2) |

## MontezumaRevenge:
| Command | Effect                                  |
|---------|-----------------------------------------|
| random_position_start     | Sets a random starting position for the player. |
| set_level_0               | Sets the game to a specified level. (0, 1 or 2) |
| randomize_items           | Randomizes which items are found in which rooms. |
| full_inventory            | Adds all items to the player's inventory. |


## MsPacman
| Command                 | Effect                                                            |
|-------------------------|-------------------------------------------------------------------|
| caged_ghosts       | Caged ghosts, ghosts will not leave the middle |
| disable_orange     | Disable the orange ghost (also works with red, cyan, pink) |
| set_level_0        | Set level to 0. (0, 1 or 2) |
| end_game           | inverted mode, eating a power pill maked the ghos dangerous again |

## Pong
| Command                 | Effect                                                            |
|-------------------------|-------------------------------------------------------------------|
| lazy_enemy   | Enemy does not move after returning the shot. |
| up_drift     | Makes the ball drift upwards. (Also works with down, left and right) |
| hidden_enemy | Makes the enemy invisible for the player (does not work in dqn_default since it is a object detection modification)


## Seaquest
| Command | Effect                           |
|---------|----------------------------------|
| unlimited_oxygen     | Set the oxygen to unlimited mode |
| disable_enemies      | Disables all enemies             |
| random_color_enemies | The enemies have new random colors each time they go across the screen.|
| gravity              | Enable graxity mode.             |

### Note: If all enemies are disabled, stray projectiles can occure in certain situations which will still kill the player. We haven't found a fix for this.

## Skiing
| Command | Effect                           |
|---------|----------------------------------|
| invert_flags     | Change flag color to red (last flag will be blue) |

## SpaceInvaders:
| Command    | Effect                                                            |
|------------|-------------------------------------------------------------------|
| disable_shield_left          | Disables the left shield. (Also works with middle and right)  |
| relocate_shields_slight_left | Set the shields to a position left of their original  |
| relocate_shields_off_by_one  | Set shields off by one pixel  |
| relocate_shields_right       | Set shields to new position right of the original  |
| controlable_missile          | The missible trajectory follows the user control of the ship  |
| no_danger                    | Stops enemies from fireing missiles. Also removes the shields. 

## Tennis
| Command | Effect             |
|---------|--------------------|
| wind_effect               | Enables wind drift |
| always_upper_pitches      | The upper player always pitches |
| always_lower_pitches      | The lower player always pitches |
| always_upper_player       | The player is always the upper player |
| always_lower_player       | The player is always the lower player |

## Riverraid
| Command | Effect             |
|---------|--------------------|
| no_fuel                   | Disables Fuel |
| red_river                 | Makes River red |
| linear_river              | Makes the river straight, however objects still spwan at their normal position making them unreachable in the worst case                       | 
| game_color_change01       | Changes game color to color set 01 |
| game_color_change02       | Changes game color to color set 02 |
| game_color_change03       | Changes game color to color set 03 |
| object_color_change01     | Changes object color to color set 01 |
| object_color_change02     | Changes object color to color set 02 |
| object_color_change02     | Changes object color to color set 03 |
