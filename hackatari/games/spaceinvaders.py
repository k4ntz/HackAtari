import numpy as np

NEW_POSITION = 0

PREV_X = 246

MATCH_X = 0


def disable_shield_left(self):
    '''
    disable_shield_left: Disables the left shield.
    '''
    shield_status_left = self.get_ram()[43:52]
    for i in range(len(shield_status_left)):
        shield_status_left[i] = 0
        self.set_ram(i+43,shield_status_left[i])


def disable_shield_middle(self):
    '''
    disable_shield_middle: Disables the middle shield.
    '''
    shield_status_middle = self.get_ram()[52:61]
    for i in range(len(shield_status_middle)):
        shield_status_middle[i] = 0
        self.set_ram(i+52, shield_status_middle[i])


def disable_shield_right(self):
    '''
    disable_shield_right: Disables the right shield.
    '''
    shield_status_right = self.get_ram()[61:71]
    for i in range(len(shield_status_right)):
        shield_status_right[i] = 0
        self.set_ram(i+61, shield_status_right[i])


def relocate_shields(self):
    '''
    relocate_shields: Allows for the relocation of the shields via an offset.
    '''
    shield_pos_new = NEW_POSITION
    if shield_pos_new < 53 and shield_pos_new >= 35:
        self.set_ram(27, shield_pos_new)


def curved_shots(self):
    '''
    curved_shots: Makes the shots travel on a curved path.
    '''
    curr_laser_pos = self.get_ram()[87]
    curr_laser_hight = self.get_ram()[85]

    
    # Manipulate the value in RAM cell 87 as long as the upper and the lower threshold
    # are not reached.
    if 40 < curr_laser_pos < 122:
        if 75 < curr_laser_hight < 150:
            global MATCH_X
            MATCH_X = self.get_ram()[28]
        laser_displacement = calculate_x_displacement(self, curr_laser_pos, curr_laser_hight)
        self.set_ram(87, laser_displacement)
    else:
        global PREV_X
        PREV_X = self.get_ram()[28]

# calculates the x coordinate displacement based on a parabolic function
def calculate_x_displacement(self, current_x, current_y):
    '''
    calculate_x_displacement: calculates the displacement value based on a parabolic function
    and the current x position.
    '''
    # 85
    global PREV_X
    global MATCH_X
    if MATCH_X < PREV_X:
        x_out = current_x - current_y/160
    elif MATCH_X > PREV_X:
        x_out = current_x + current_y/160
    else:
        x_out = current_x
    x_out = int(np.round(x_out))
    return int(x_out)

def controlable_missile(self):
    self.set_ram(87, self.get_ram()[28])


def _modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        if mod == "disable_shield_left":
            step_modifs.append(disable_shield_left)
        elif mod == "disable_shield_middle":
            step_modifs.append(disable_shield_middle)
        elif mod == "disable_shield_right":
            step_modifs.append(disable_shield_right)
        elif mod == "disable_shields":
            step_modifs.append(disable_shield_left)
            step_modifs.append(disable_shield_middle)
            step_modifs.append(disable_shield_right)
        elif mod == "curved":
            step_modifs.append(curved_shots) 
        elif mod == "controlable_missile":
            step_modifs.append(controlable_missile) 
        elif mod.startswith('relocate'):
            mod_n = int(mod[-2:])
            if mod_n < 35 or mod_n > 53:
                raise ValueError("Invalid position for shields, choose value 35-53")
            global NEW_POSITION
            NEW_POSITION = mod_n
            reset_modifs.append(relocate_shields)        
    return step_modifs, reset_modifs