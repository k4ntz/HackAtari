def _calc_x(number):
    """
    takes the bitfield (4 bits) and extracts the x of the object
    way too complicated for no reason
    """
    anchor = number % 16
    offset = number >> 4
    if offset > 7:
        offset = 28 - offset  # 23 + 5 (5 being constant offset)
    else:
        offset = 12 - offset  # 7 + 5
    return anchor * 15 + offset

class GameModifications:
    """
    Encapsulates game modifications for managing active modifications and applying them.
    """
    
    def __init__(self, env):
        """
        Initializes the modification handler with the given environment.

        :param env: The game environment to modify.
        """
        self.env = env
        self.active_modifications = set()
        self._x_poses = [[0, 0], [0, 0], [0, 0]]
        self._ram20 = 0 # falling enemy x
    
    
    def static_enemies(self):
        """
        Makes the enemies horizontally static (i.e. constant x position).
        """
        ram = self.env.get_ram()
        for i in range(3):
            x_right = _calc_x(ram[13+i])
            x_left = _calc_x(ram[17+i])
            if ram[29+i] <= 3 and ram[33+i] <= 3 or abs(x_right - x_left) > 10:
                    
                self._x_poses[i] = [0, 0]
            else:
                if self._x_poses[i] == [0, 0]:
                    if not (x_right > 127 or x_left < 33):
                        self._x_poses[i] = [ram[13+i], ram[17+i]]
                else:
                    self.env.set_ram(13+i, self._x_poses[i][0])
                    self.env.set_ram(17+i, self._x_poses[i][1])
    
        if ram[51] and ram[50] >> 6:
            if self._ram20 == 0:
                self._ram20 = ram[20]
            self.env.set_ram(20, self._ram20)
        else:
            self._ram20 = 0

    def one_missile(self):
        changed = False
        for i in range(37, 47):
            if changed:
                self.env.set_ram(i, 0)
            if self.env.get_ram()[i] != 0:
                self.env.set_ram(i, 4)
                changed = True
                
    
    def _set_active_modifications(self, active_modifs):
        """
        Specifies which modifications are active.

        :param active_modifs: A list of active modification names.
        """
        self.active_modifications = set(active_modifs)

    def _fill_modif_lists(self):
        """
        Returns the step modification list with active modifications.

        :return: List of step modifications.
        """
        modif_mapping = {
            "static_enemies": self.static_enemies,
            "one_missile": self.one_missile,
        }

        step_modifs = [modif_mapping[name]
                       for name in self.active_modifications if name in modif_mapping]
        return step_modifs, [], []

def modif_funcs(env, active_modifs):
    modifications = GameModifications(env)
    modifications._set_active_modifications(active_modifs)
    return modifications._fill_modif_lists()
