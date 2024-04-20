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

def modif_funcs(modifs):
    step_modifs, reset_modifs = [], []
    for mod in modifs:
        if mod == "wind":
            step_modifs.append(modify_ram_adding_wind)
    return step_modifs, reset_modifs