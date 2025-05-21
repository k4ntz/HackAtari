"""
core.py

This module extends the OCAtari framework to provide HackAtari, an object-centric
Atari Learning Environment with support for custom modifications, reward functions,
and human playability. It includes:

- HackAtari: Main environment class with modifiable step/reset logic and reward functions.
- HumanPlayable: Subclass for human-interactive play using pygame.
- _available_modifications: Utility to list available modifications for a game.

Dependencies:
- numpy, pygame, importlib, sys, warnings, cv2, termcolor (optional), ocatari.core
"""

import numpy as np
import pygame
import importlib
import sys
from ocatari.core import OCAtari
import warnings
import cv2
try:
    from termcolor import colored
except ImportError:
    def colored(text, color):
        return text
    print("Warning: termcolor not installed. Colored output will not be available.")

# Suppress unnecessary warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=UserWarning)


class HackAtari(OCAtari):
    """
    HackAtari extends the Atari Learning Environment (ALE) by enabling object-centric observations
    and providing various environment modifications.

    Features:
    - Dynamic loading of game-specific modifications.
    - Support for custom reward functions.
    - Dopamine-style frame pooling.
    - Game mode and difficulty configuration.
    """

    def __init__(
        self,
        env_name: str,
        modifs=[],
        rewardfunc_path=None,
        dopamine_pooling=False,
        game_mode=None,
        difficulty=None,
        *args,
        **kwargs,
    ):
        """
        Initialize the Atari environment with optional modifications.

        :param env_name: Name of the Atari game environment.
        :param modifs: List of modifications applied to the environment.
        :param rewardfunc_path: Path to a custom reward function (or list of paths).
        :param dopamine_pooling: Whether to use Dopamine-style frame pooling.
        :param game_mode: Specific mode setting for the ALE.
        :param difficulty: Difficulty level for the ALE.
        :param args: Additional positional arguments for OCAtari.
        :param kwargs: Additional keyword arguments for OCAtari.
        """
        self._frameskip = kwargs.get("frameskip", 4)  # Default frameskip to 4
        # Override frameskip to 1 for custom step handling
        kwargs["frameskip"] = 1

        super().__init__(env_name, *args, **kwargs)

        self.ale = self.env.unwrapped.ale
        # Initialize modifications and environment settings
        self.step_modifs, self.reset_modifs, self.post_detection_modifs = [], [], []

        # Load modification functions dynamically
        try:
            modif_module = importlib.import_module(
                f"hackatari.games.{self.game_name.lower()}")
            step_modifs, reset_modifs, post_detection_modifs = modif_module.modif_funcs(
                self, modifs)
            self.step_modifs.extend(step_modifs)
            self.reset_modifs.extend(reset_modifs)
            self.post_detection_modifs.extend(post_detection_modifs)

        except ModuleNotFoundError as e:
            print(colored(
                f"Error: {e}. No modifications available for {self.game_name}.", "yellow"))

        self.dopamine_pooling = dopamine_pooling and self._frameskip > 1

        # Track original rewards for external reward adjustments
        self.org_return = 0
        self.org_reward = 0

        # Load custom reward function(s) if provided
        if rewardfunc_path:
            if type(rewardfunc_path) is list:
                # multiple reward functions (return tuple)
                print(f"Using multiple rewards: {rewardfunc_path}")
                self.new_reward_func = []
                for path in rewardfunc_path:
                    spec = importlib.util.spec_from_file_location(
                        "reward_function", path
                    )
                    if spec is None:
                        raise ImportError(f"Cannot load spec from {path}")
                    module = importlib.util.module_from_spec(spec)
                    sys.modules["reward_function"] = module
                    spec.loader.exec_module(module)
                    self.new_reward_func.append(module.reward_function)
            else:
                spec = importlib.util.spec_from_file_location(
                    "reward_function", rewardfunc_path
                )
                if spec is None:
                    raise ImportError(
                        f"Cannot load spec from {rewardfunc_path}")
                module = importlib.util.module_from_spec(spec)
                sys.modules["reward_function"] = module
                spec.loader.exec_module(module)
                self.new_reward_func = [module.reward_function]
            self._step = self.step
            self.step = self.step_with_lm_reward

        if game_mode is not None:
            # Apply game mode and difficulty settings
            try:
                self.env.env.ale.setMode(game_mode)
                print("Game mode set to: ", game_mode)
            except RuntimeError:
                print(f"Invalid mode. Available modes: \
                    {self.env.env.ale.getAvailableModes()}")
                exit()
        if difficulty is not None:
            try:
                self.env.env.ale.setDifficulty(difficulty)
                print("Difficulty set to: ", difficulty)
            except RuntimeError:
                print(f"Invalid difficulty. Available difficulties: \
                    {self.env.env.ale.getAvailableDifficulties()}")
                exit()

    def step(self, *args, **kwargs):
        """
        Take a step in the game environment after altering the ram.

        Args:
            action (int): Action to take in the environment.
        Returns:
            tuple: (obs, reward, truncated, terminated, info)
                - obs: Environment observation
                - reward: Sum of all custom rewards (for this one step)
                - truncated: Boolean if truncated
                - terminated: Boolean if terminated
                - info: dict with 'all_rewards' (list of rewards) and 'org_return' (cumulative ALE reward)
        """
        frameskip = self._frameskip
        total_reward = 0.0
        terminated = truncated = False
        if self.dopamine_pooling:
            last_two_obs = []
            last_two_org = []

        for i in range(frameskip-1):
            for func in self.step_modifs:
                func()
            obs, reward, terminated, truncated, info = self._env.step(
                *args, **kwargs)
            total_reward += float(reward)
            if terminated or truncated:
                break

        if self.dopamine_pooling:
            last_two_obs.append(cv2.resize(cv2.cvtColor(self.getScreenRGB(
            ), cv2.COLOR_RGB2GRAY), (84, 84), interpolation=cv2.INTER_AREA))
            last_two_org.append(self.getScreenRGB())

        for func in self.step_modifs:
            func()
        obs, reward, terminated, truncated, info = self._env.step(
            *args, **kwargs)
        for func in self.step_modifs:
            func()
        total_reward += float(reward)
        self.detect_objects()
        for func in self.post_detection_modifs:
            func()
        self._fill_buffer()

        if self.obs_mode == "dqn":
            obs = np.array(self._state_buffer_dqn)
        elif self.obs_mode == "obj":
            obs = np.array(self._state_buffer_ns)

        if self.dopamine_pooling:
            last_two_obs.append(cv2.resize(cv2.cvtColor(self.getScreenRGB(
            ), cv2.COLOR_RGB2GRAY), (84, 84), interpolation=cv2.INTER_AREA))
            last_two_org.append(self.getScreenRGB())
            merged_obs = np.maximum.reduce(last_two_obs)
            merged_org = np.maximum.reduce(last_two_org)

            if self.create_dqn_stack:
                self._state_buffer_dqn[-1] = merged_obs
            if self.create_rgb_stack:
                self._state_buffer_rgb[-1] = merged_org

            if self.obs_mode == "dqn":
                obs[-1] = merged_obs
            else:
                obs = merged_org

        return obs, total_reward, terminated, truncated, info

    def step_with_lm_reward(self, action):
        """
        Step using a custom (external) reward function, combining all rewards as the environment reward.

        Args:
            action (int): Action to take in the environment.
        Returns:
            tuple: (obs, reward, truncated, terminated, info)
                - obs: Environment observation
                - reward: Sum of all custom rewards (for this one step)
                - truncated: Boolean if truncated
                - terminated: Boolean if terminated
                - info: dict with 'all_rewards' (list of rewards) and 'org_return' (cumulative ALE reward)
        """
        obs, game_reward, truncated, terminated, info = self._step(action)
        self.org_reward = game_reward
        self.org_return += game_reward
        try:
            rewards = [reward_func(self)
                       for reward_func in self.new_reward_func]
        except Exception as e:
            print("Error in new_reward_func:", e)
            rewards = [0]
        info["all_rewards"] = rewards
        reward = sum(rewards)
        info["org_return"] = self.org_return
        return obs, reward, truncated, terminated, info

    def reset(self, *args, **kwargs):
        """
        Reset the environment and apply reset modifications.

        :return: (obs, info)
        """
        obs, info = super().reset(*args, **kwargs)
        self.org_reward = 0
        self.org_return = 0

        for func in self.reset_modifs:
            func()
        for func in self.post_detection_modifs:
            func()

        return obs, info

    @property
    def available_modifications(self):
        """
        List available modifications for the current game.

        :return: String listing available modifications.
        """
        return _available_modifications(self.game_name)


class HumanPlayable(HackAtari):
    """
    Enables human play mode for the Atari game by handling user input and rendering.

    Features:
    - Keyboard-based action mapping.
    - Pause, reset, and quit controls.
    - Real-time rendering with overlays.
    """

    def __init__(self, game, modifs=[], rewardfunc_path="", game_mode=None, difficulty=None, *args, **kwargs):
        """
        Initialize a human-playable Atari game instance.

        :param game: Name of the Atari game.
        :param modifs: List of modifications.
        :param rewardfunc_path: Path to custom reward function.
        :param game_mode: Game mode for ALE.
        :param difficulty: Difficulty for ALE.
        :param args: Additional positional arguments.
        :param kwargs: Additional keyword arguments.
        """
        kwargs["render_mode"] = "human"
        kwargs["render_oc_overlay"] = True
        kwargs["frameskip"] = 1
        kwargs["full_action_space"] = True

        super().__init__(game, modifs, rewardfunc_path, dopamine_pooling=True,
                         game_mode=game_mode, difficulty=difficulty, *args, **kwargs)

        self.reset()
        self.render(self._state_buffer_rgb[-1])  # type: ignore
        self.print_reward = bool(rewardfunc_path)
        self.paused = False
        self.current_keys_down = set()
        self.keys2actions = self.env.unwrapped.get_keys_to_action()
        print("Keys to actions: ", self.keys2actions)

    def run(self):
        """
        Start the game loop, allowing human interaction.
        """
        pygame.init()
        self.running = True

        while self.running:
            self._handle_user_input()

            if not self.paused:
                action = self._get_action()
                _, reward, _, _, _ = self.step(action)
                if self.print_reward and reward:
                    print(reward)
                self.render(self._state_buffer_rgb[-1])  # type: ignore

        pygame.quit()

    def _get_action(self):
        """
        Get the action corresponding to the current key press.

        :return: Action integer for the environment.
        """
        pressed_keys = list(self.current_keys_down)
        pressed_keys.sort()
        pressed_keys = tuple(pressed_keys)
        print("Pressed keys: ", pressed_keys)
        if pressed_keys in self.keys2actions.keys():
            print("Action: ", self.keys2actions[pressed_keys])
            return self.keys2actions[pressed_keys]
        else:
            return 0  # NOOP

    def _handle_user_input(self):
        """
        Handles user input for the environment, including pause, reset, and quit.
        """
        self.current_mouse_pos = np.asarray(pygame.mouse.get_pos())

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:  # Window close button clicked
                self.running = False

            elif event.type == pygame.KEYDOWN:  # Keyboard key pressed
                if event.key == pygame.K_p:  # 'P': Pause/Resume
                    self.paused = not self.paused

                if event.key == pygame.K_q:  # 'Q': Quit
                    self.running = False

                if event.key == pygame.K_r:  # 'R': Reset
                    self.reset()

                elif (event.key,) in self.keys2actions.keys():  # Env action
                    self.current_keys_down.add(event.key)

            elif event.type == pygame.KEYUP:  # Keyboard key released
                if (event.key,) in self.keys2actions.keys():
                    self.current_keys_down.remove(event.key)


def _available_modifications(game_name):
    """
    List available modifications for a given game.

    :param game_name: Name of the Atari game.
    :return: String listing available modifications and their docstrings.
    """
    modif_module = importlib.import_module(
        f"hackatari.games.{game_name.lower()}")
    modifs_list = [mod for mod in dir(
        modif_module.GameModifications) if not mod.startswith("_")]
    retstr = f"Available modifications for {game_name}:\n"
    for mod in modifs_list:
        retstr += f"  * {mod}:\n\t"
        retstr += getattr(modif_module.GameModifications,
                          mod).__doc__.strip() + "\n"
    return retstr
