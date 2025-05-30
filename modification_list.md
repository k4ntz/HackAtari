# Modified Atari Games

A complete list of all modifications and their corresponding arguments.

This is the list of games we have created new versions and modifications for during the "HackAtari" project. Each file, when started without additional parameters, starts the original game played by the DQN agent.
All modes/hacks/changes can be activated individually or in any combination via the command line.

Use `-hu` to start the game in Human Mode and play the game yourself.


Use `-m` to select the mode you want to play in. All modes/hacks/changes can be activated individually or in any combination by separating with whitespace between them.

**Example**: `python run.py -g Freeway -hu -m stop_all_cars` will run Freeway with all cars being red (`c3`) and stopped (`sm3`) in Human (playable) Mode (`-hu`).

The modes are:

## Alien:
| Command | Effect                                                                               |
|---------|--------------------------------------------------------------------------------------|
| last_egg           | Removes all eggs but one |
| aliens_0           | Removes all three alien enemies from the maze (also works with 1 and 2). |
| no_enemies         | Removes the three alien enemies from the maze, and freezes all aliens in the second faze. |
| unlimited_fuel     | Always keeps the flamethrowers fuel at max. |

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
| two_police_cars         | Replaces 2 banks with police cars, robbed banks give 50 points |
| random_city             | Start in a random city |
| revisit_city            | Allows player to revisit previous cities |

## Bowling:
| Command | Effect                                                                               |
|---------|--------------------------------------------------------------------------------------|
| shift_player           | Shifts the player to the left |
| horizontal_pins        | Draws the pins horizontally instead of vertically |
| small_pins             | Decreases pin size to 1 pixel |
| moving_pins            | Moves all pins up and down |
| top_pins               | Removes all but the top two pins |
| middle_pins            | Removes all but the two middle pins |
| bottom_pins            | Removes all but the bottom two pins |
| top_bottom_pins        | Removes all but the top and bottom two pins |

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

## DemonAtack:

| Command | Effect                                                                               |
|---------|--------------------------------------------------------------------------------------|
| static_enemies         | Makes the enemies horizontally static (i.e. constant x position) |
| one_missile            | Enemies only shoot one missile |

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
| shark_no_movement_easy    | The shark will not move and stay on the opponents side |
| shark_no_movement_middle  | The shark will not move and is placed in the middle |
| shark_teleport            | Teleports the shark in the line |
| shark_speed_mode          | Makes the shark very very fast |
| fish_on_player_side       | All fish are on the player's side |
| fish_in_middle            | All fish are in the middle.|

## Freeway:

| Command | Effect                                                                               |
|---------|--------------------------------------------------------------------------------------|
| stop_random_car           | Stops a random car with a biased probability for a certain time. |
| stop_all_cars_edge        | Stops all cars on the side of the board. |
| stop_all_cars_tunnel      | Stops all cars on the street, building a tunnel for the player. |
| align_all_cars            | Align all cars so they move in a line. |
| invisible_mode            | Makes the cars invisible. |
| strobo_mode               | Each car changes color randomly every timestep. |
| phantom_mode              | Each car changes color from black to invisible approximately every second. |
| blinking_mode             | Each car changes color randomly approximately every second. |
| speed_mode                | Increases the speed of all cars. |
| reverse_car_speed_bottom  | Reverses the speed order of the cars on the bottom road (the fastest becomes the slowest and vice versa). |
| reverse_car_speed_top     | Reverses the speed order of the cars on the top road (the fastest becomes the slowest and vice versa). |
| all_black_cars            | All cars are black. (also works with white, red, blue and green)|


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


## Jamesbond:
| Command | Effect                                                                               |
|---------|--------------------------------------------------------------------------------------|
| constant_jump     | Makes the player character jump constantly. |
| straight_shots    | The player shots go straight up, instead of diagonal. |
| fast_backward     | Increases the reversing speed. |
| mobile_player     | Makes the player character jump constantly and increases the reversing speed. |
| unlimited_lives   | Player has an unlimited amounts of lives. |


## Kangaroo:
| Command | Effect                                  |
|---------|-----------------------------------------|
| set_kangaroo_position_floor1  | Set the starting floor (1, or 2) |
| randomize_kangaroo_position   | Random starting floor |
| disable_monkeys               | Disable monkeys in the game |
| disable_coconut               | Disable the falling coconut in the game |
| disable_thrown_coconut        | Disable the throwing coconut in the game |
| no_danger                     | Combines the three modifications above, disabling all hazards in the game |
| change_level_0                | Set starting level (0, 1, or 2) |
| unlimited_time                | Provides unlimited time to clear the level |

## KungFuMaster:
| Command | Effect                                  |
|---------|-----------------------------------------|
| no_damage         | Player does not take damage. |
| unlimited_time    | Provides unlimited time to clear the level. |
| unlimited_lives   | Player has an unlimited amounts of lives. |

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
| end_game           | Simulates an almost done game, with 15 pills remaining in the level. |
| maze_man           | Changes the game to a maze solving task. Only one pill will spawn at a time. After the player collects it, a new pill will spawn. The game is won when the player has collected 20 pills. |


## NameThisGame
| Command                 | Effect                                                            |
|-------------------------|-------------------------------------------------------------------|
| unlimited_oxygen   | Provides the player with an unlimited supply of oxygen. |
| unlimited_lives    | Player has an unlimited amounts of lives. |
| double_wave_length | Doubles the amount of time it takes to get into the next phase. |
| quick_start        | Skips the intro. |


## Pong
| Command                 | Effect                                                            |
|-------------------------|-------------------------------------------------------------------|
| lazy_enemy   | Enemy does not move after returning the shot. |
| up_drift     | Makes the ball drift upwards. (Also works with down, left and right) |
| hidden_enemy | Makes the enemy invisible for the player (does not work in dqn_default since it is a object detection modification) |


## RiverRaid
| Command                 | Effect                                                            |
|-------------------------|-------------------------------------------------------------------|
| no_fuel               | Removes the fuel deposits from the game. |
| red_river             | Turns the river red. |
| linear_river          | Makes the river straight, however objects still spwan at their normal position making them unreachable in the worst case. |
| game_color_change01   | Turns all elements of the game to another colorset (also works with 02, 03). |
| object_color_change01 | Turns all objects in the game to another colorset (also works with 02, 03). |
| exploding_fuels       | Shooting the fuel deposits will now provides -80 points (instead of 20). |
| restricted_firing     | The player is only able to shoot in critical situation, facing a bridge or in a corridor. |
| unlimited_lives       | Player has an unlimited amounts of lives. |


## RoboTank
| Command                 | Effect                                                            |
|-------------------------|-------------------------------------------------------------------|
| fog           | Weather condition is always set to fog. |
| snow          | Weather condition is always set to snow. |
| rain          | Weather condition is always set to rain. |
| no_radar      | Disables the radar. |
| tread_damage  | Tread sensor is damaged. |
| canon_damage  | Canon is damaged. |
| vision_damage | Vision sensor is damaged. |


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
| invert_flags     | Change flag color to red (last flag will be blue). |
| moguls_to_trees  | Replaces all moguls with trees. |
| moving_flags     | Flags move to the left and right. |
| random_flags     | Randomizes the horizontal position of the flags. |
| flag_flurry      | Flags appear in quick succession. The number of flags per run doubles. |


## SpaceInvaders:
| Command    | Effect                                                            |
|------------|-------------------------------------------------------------------|
| disable_shield_left          | Disables the left shield. (Also works with middle and right)  |
| relocate_shields_slight_left | Set the shields to a position left of their original  |
| relocate_shields_off_by_one  | Set shields off by one pixel  |
| relocate_shields_right       | Set shields to new position right of the original  |
| controlable_missile          | The missible trajectory follows the user control of the ship  |
| no_danger                    | Stops enemies from fireing missiles. Also removes the shields. |


## StarGunner:
| Command    | Effect                                                            |
|------------|-------------------------------------------------------------------|
| static_bomber     | Stops the bomber at the top from moving.  |
| static_flyers     | Stops the flying enemies in place.  |
| remove_mountains  | Removes the mountains from the game. |
| static_mountains  | The mountains stay the same, even if the player moves. |


## Tennis
| Command | Effect             |
|---------|--------------------|
| wind_effect               | Enables wind drift |
| always_upper_pitches      | The upper player always pitches |
| always_lower_pitches      | The lower player always pitches |
| always_upper_player       | The player is always the upper player |
| always_lower_player       | The player is always the lower player |


## TimePilot
| Command | Effect             |
|---------|--------------------|
| level_1               | Changes the level to level 1 (also works with 2, 3, 4, 5). |
| random_orientation    | Randomizes orientation of enemies. They are no longer aligned. |


## Venture
| Command | Effect             |
|---------|--------------------|
| random_enemy_colors   | Changes the color of all enemies to a random color. |
| enemy_color_black     | Randomizes orientation of enemies. They are no longer aligned (also works with white, red, blue, green). |


## YarsRevenge
| Command | Effect             |
|---------|--------------------|
| disable_enemy_movement    | Disables enemy movement. |
| disable_block_movement    | Stops blocks in place. |
| static                    | Disables enemy movement and stops blocks in place. |
