from random import random

def modify_ram_adding_wind(self):
    '''
    wind: Sets the ball in the up and right direction by 3 pixles every single ram step
    to simulate the effect of wind
    '''
    ram = self.get_ram()
    ball_x = ram[16]
    # ball_y isn't always stable, as the ball bounces in some situations
    ball_y = 189 - ram[54]
    # shadow x is always the same as ball_x
    # this ankers the ball when bouncing
    shadow_anker = ram[15]
    shadow_y = 189 - ram[55]


    #movement up and right - noth-east wind direction stays the same so no indication is needed
    new_ball_x = ball_x # moves the ball to the right one position every ram step
    new_ball_y = ball_y # moves the ball up one position every ram step
    new_shadow_y  = shadow_y
    if random() < 0.5:
        new_ball_x += 1 # moves the ball to the right one position every ram step
        new_ball_y += 1 # moves the ball up one position every ram step
        new_shadow_y += 1 
    #first part makes sure ball only moves in the air, not if bouncing on the line
    #as ram manipualtion fails when bouncing
    #second part makes sure the ball stops moving when it exits the visible field
    #in the x position to not loop the ram around
    if (ball_y < 140 and ball_y > 10) and (shadow_anker < 140 and shadow_anker > 10) and (ball_x > 2 and ball_x < 155):
        self.set_ram(16, new_ball_x)
        self.set_ram(54, new_ball_y)
        self.set_ram(55, new_shadow_y)

def upper_pitches(self):
    """
    Changes the ram so that it is always the upper persons turn to pitch.
    """
    ram = self.get_ram()
    if ram[15] == 7:
        self.set_ram(15, 142) # makes the ball start from the top
        self.set_ram(74, 0) # makes it the upper persons turn to pitch


def lower_pitches(self):
    """
    Changes the ram so that it is always the lower persons turn to pitch.
    """
    ram = self.get_ram()
    if ram[15] == 142:
        self.set_ram(15, 7) # makes the ball start from the bottom
        self.set_ram(74, 1) # makes it the lower persons turn to pitch

def upper_player(self):
    """
    Changes the ram so that the player is always in the upper field
    """      
    self.set_ram(80, 0)

def lower_player(self):
    """
    Changes the ram so that the player is always in the lower field
    """      
    self.set_ram(80, 1)

def _modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        if mod == "wind":
            step_modifs.append(modify_ram_adding_wind)
        if mod == "upper_pitches":
            step_modifs.append(upper_pitches)
        if mod == "lower_pitches":
            step_modifs.append(lower_pitches)
        if mod == "upper_player":
            step_modifs.append(upper_player)
        if mod == "lower_player":
            step_modifs.append(lower_player)
    return step_modifs, reset_modifs