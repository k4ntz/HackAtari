from ocatari.core import OCAtari
import importlib
import pygame
import numpy as np
import random


GameList = ["BankHeist", "BattleZone", "Boxing", "Breakout", "Carnival", "ChopperCommand", "FishingDerby", 
            "Freeway", "Frostbite", "Kangaroo", "MontezumaRevenge",
            "MsPacman", "Pong", "Riverraid", "Seaquest", "Skiing", "SpaceInvaders", "Tennis"]


class ALEColorSwapProxy:
    def __init__(self, ale, colorswaps):
        self._ale = ale
        self._colorswaps = colorswaps

    def __getattr__(self, name):
        if name == "getScreenRGB" or name == "getScreen":
            return self.custom_getScreenRGB
        return getattr(self._ale, name)

    def custom_getScreenRGB(self, *args, **kwargs):
        # Your custom logic here
        ret = self._ale.getScreenRGB(*args, **kwargs)
        colorswappinng(ret, self._colorswaps)
        return ret


class HackAtari(OCAtari):
    """
    Modified environments from OCAtari
    """
    def __init__(self, game: str, modifs=[], colorswaps=None, *args, **kwargs):
        """
        Initialize the game environment.
        """
        if "frameskip" in kwargs:
            self._frameskip = kwargs["frameskip"]
        elif "NoFrameskip" or "v5" in game:
            self._frameskip = 1
        elif "Determinisitc" or "v5" in game:
            self._frameskip = 4
        else:
            self._frameskip = "0"  # correspond to random frameskip
        kwargs["frameskip"] = 1
        kwargs["render_oc_overlay"] = True
        super().__init__(game, *args, **kwargs)
        covered = False
        for cgame in GameList:
            if cgame in game:
                covered = True
                game = cgame
                break
        if not covered:
            raise ValueError(f"Game {game} is not covered in the HackAtari")
        modif_funcs = importlib.import_module(f"hackatari.games.{game.lower()}").modif_funcs
        self.alter_ram_steps, self.alter_ram_reset = modif_funcs(modifs)
        self._oc_step = self.step
        self._oc_reset = self.reset
        if colorswaps is not None:
            assert_colorswaps(colorswaps)
            self.colorswaps = colorswaps
            # self.step = self._colorswap_step
            # self.reset = self._colorswap_reset
            self.env.env.ale = ALEColorSwapProxy(self.env.env.ale, colorswaps)
        else:
            self.step = self._alter_step
            self.reset = self._alter_reset
    
    
    def _alter_step(self, action):
        """
        Take a step in the game environment after altering the ram.
        """
        frameskip = self._frameskip
        if not frameskip:
            frameskip = random.choice((2, 5))
        for _ in range(frameskip):
            for func in self.alter_ram_steps:
                func(self)
            ret = self._oc_step(action)
            for func in self.alter_ram_steps:
                func(self)
        return ret

    def _alter_reset(self, *args, **kwargs):
        ret = self._oc_reset(*args, **kwargs)
        for func in self.alter_ram_reset:
            func(self)
        return ret

    def _colorswap_step(self, *args, **kwargs):
        """
        Alter the color according to the colorswaps dictionary while also altering the steps.
        """
        ret = self._alter_step(*args, **kwargs)
        colorswappinng(ret[0], self.colorswaps)
        return ret

    def _colorswap_reset(self, *args, **kwargs):
        """
        Alter the color according to the colorswaps dictionary while also altering the steps.
        """
        ret = self._alter_reset(*args, **kwargs)
        colorswappinng(ret[0], self.colorswaps)
        return ret
    
    def _altered_screen_RGB(self, colorswaps):
        ret = self.getScreenRGB()
        colorswappinng(ret, colorswaps)
        return ret


class HumanPlayable(HackAtari):
    """
    HumanPlayable: Enables human play mode for the game.
    """

    def __init__(self, game, modifs=[], colorswaps={}, *args, **kwargs):
        """
        Initializes the HumanPlayable environment with the specified game and modifications.
        """
        kwargs["render_mode"] = "human"
        kwargs["render_oc_overlay"] = True
        super(HumanPlayable, self).__init__(game, modifs, colorswaps, *args, **kwargs)
        self.reset()
        self.render()  # Initialize the pygame video system

        self.paused = False
        self.current_keys_down = set()
        self.keys2actions = self.env.unwrapped.get_keys_to_action()



    def run(self):
        '''
        run: Runs the ExtendedHuman environment, allowing human interaction with the game.
        '''
        pygame.init()
        self.running = True
        while self.running:
            self._handle_user_input()
            if not self.paused:
                action = self._get_action()
                self.step(action)
                self.render()
        pygame.quit()

    def _get_action(self):
        '''
        _get_action: Gets the action corresponding to the current key press.
        '''
        pressed_keys = list(self.current_keys_down)
        pressed_keys.sort()
        pressed_keys = tuple(pressed_keys)
        if pressed_keys in self.keys2actions.keys():
            return self.keys2actions[pressed_keys]
        else:
            return 0  # NOOP

    def _handle_user_input(self):
        '''
        _handle_user_input: Handles user input for the BoxingExtendedHuman environment.
        '''
        self.current_mouse_pos = np.asarray(pygame.mouse.get_pos())

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:  # Window close button clicked
                self.running = False

            elif event.type == pygame.KEYDOWN:  # Keyboard key pressed
                if event.key == pygame.K_p:  # 'P': Pause/Resume
                    self.paused = not self.paused

                if event.key == pygame.K_r:  # 'R': Reset
                    self.env.reset()

                elif (event.key,) in self.keys2actions.keys():  # Env action
                    self.current_keys_down.add(event.key)

            elif event.type == pygame.KEYUP:  # Keyboard key released
                if (event.key,) in self.keys2actions.keys():
                    self.current_keys_down.remove(event.key)

def assert_colorswaps(colorswaps):
    msg = "Invalid colorswaps dictionary, needs to be e.g.: {(0, 0, 0): (255, 255, 255), ...}"
    for ecol, rcol in colorswaps.items():
        assert len(ecol) == 3 and len(rcol) == 3, msg
        assert all(0 <= c <= 255 for c in ecol) and all(0 <= c <= 255 for c in rcol), msg


def colorswappinng(image, colorswaps):
    for (r1, g1, b1), (r2, g2, b2) in colorswaps.items():
        red, green, blue = image[:,:,0], image[:,:,1], image[:,:,2]
        mask1 = (red == r1) & (green == g1) & (blue == b1)
        mask2 = (red == r2) & (green == g2) & (blue == b2)
        image[:,:,:3][mask1] = [r2, g2, b2]
        image[:,:,:3][mask2] = [r1, g1, b1]