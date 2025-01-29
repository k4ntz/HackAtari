import random
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

        :param env_name: Name of the Atari game environment
        :param modifs: List of modifications applied to the environment
        :param rewardfunc_path: Path to a custom reward function
        :param dopamine_pooling: Whether to use Dopamine-style frame pooling
        :param game_mode: Specific mode setting for the ALE
        :param difficulty: Difficulty level for the ALE
        """
        self._frameskip = kwargs.get("frameskip", 4)  # Default frameskip to 4
        # Override frameskip to 1 for custom step handling
        kwargs["frameskip"] = 1

        super().__init__(env_name, *args, **kwargs)

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
            print(colored(f"Error: {e}. No modifications available for {self.game_name}.", "yellow"))

        self.dopamine_pooling = dopamine_pooling and self._frameskip > 1

        # Track original rewards for external reward adjustments
        self.org_return = 0
        self.org_reward = 0

        # Load custom reward function if provided
        if rewardfunc_path:
            print(f"Changed reward function to {rewardfunc_path}")
            spec = importlib.util.spec_from_file_location(
                "reward_function", rewardfunc_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules["reward_function"] = module
            spec.loader.exec_module(module)
            self.new_reward_func = module.reward_function
            self._step = self.step  # Override step function
            self.step = self.step_with_lm_reward  # Override step function

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
        obs, reward, terminated, truncated, info = super().step(
            *args, **kwargs)
        total_reward += float(reward)
        for func in self.post_detection_modifs:
            func()

        if self.dopamine_pooling:
            last_two_obs.append(cv2.resize(cv2.cvtColor(self.getScreenRGB(
            ), cv2.COLOR_RGB2GRAY), (84, 84), interpolation=cv2.INTER_AREA))
            last_two_org.append(self.getScreenRGB())

        if self.dopamine_pooling:
            merged_obs = np.maximum.reduce(last_two_obs)
            merged_org = np.maximum.reduce(last_two_org)

            if self.create_dqn_stack:
                self._state_buffer_dqn[-1] = merged_obs
            if self.create_rgb_stack:
                self._state_buffer_rgb[-1] = merged_org

            if self.obs_mode == "dqn":
                obs[-1] = merged_obs
            else:
                # dopamine pooling works with either "dqn" or "ori" obs_mode.
                obs = merged_org

        return obs, total_reward, terminated, truncated, info

    def step_with_lm_reward(self, action):
        """
        Perform a step in the environment while applying a custom reward function.
        """
        obs, game_reward, truncated, terminated, info = self._step(action)
        self.org_reward = game_reward
        self.org_return += game_reward
        try:
            reward = self.new_reward_func(self)
        except Exception as e:
            print("Error in new_reward_func: ", e)
            reward = 0
        info["org_return"] = self.org_return
        return obs, reward, truncated, terminated, info

    def reset(self, *args, **kwargs):
        """
        Reset the environment and apply reset modifications.
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
        return _available_modifications(self.game_name)
        

class HumanPlayable(HackAtari):
    """
    Enables human play mode for the Atari game by handling user input and rendering.
    """

    def __init__(self, game, modifs=[], rewardfunc_path="", game_mode=None, difficulty=None, *args, **kwargs):
        """
        Initialize a human-playable Atari game instance.
        """
        kwargs["render_mode"] = "human"
        kwargs["render_oc_overlay"] = True
        kwargs["frameskip"] = 1
        kwargs["full_action_space"] = True

        super().__init__(game, modifs, rewardfunc_path, dopamine_pooling=True,
                         game_mode=game_mode, difficulty=difficulty, *args, **kwargs)

        self.reset()
        self.render(self._state_buffer_rgb[-1])
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
                self.render(self._state_buffer_rgb[-1])

        pygame.quit()

    def _get_action(self):
        """
        _get_action: Gets the action corresponding to the current key press.
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
        _handle_user_input: Handles user input for the BoxingExtendedHuman environment.
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
    modif_module = importlib.import_module(
            f"hackatari.games.{game_name.lower()}")
    modifs_list = [mod for mod in dir(modif_module.GameModifications) if not mod.startswith("_")]
    retstr = f"Available modifications for {game_name}:\n"
    for mod in modifs_list:
        retstr += f"  * {mod}:\n\t"
        retstr += getattr(modif_module.GameModifications, mod).__doc__.strip() + "\n"
    return retstr