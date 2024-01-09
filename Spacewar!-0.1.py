import math
from tkinter import *

toggle = 0  #   toggle is pause

W = 0
A = 0
S = 0
D = 0
SPACE = 0

UP = 0
DOWN = 0
LEFT = 0
RIGHT = 0
ZERO = 0

R1 = 10
R2 = math.sqrt(10**2 + 5**2)

orange_angle = 0
orange_x_speed = 0
orange_y_speed = 0
orange_shoot_cd = 0
orange_rotation_coords = [-5, -10, 5, -10, 0, 10]
orange_draw_coords = [0, 0, 0, 0, 0, 0]
orange_coords = [90, 630]
orange_live_status = 1

green_angle = 180
green_x_speed = 0
green_y_speed = 0
green_shoot_cd = 0
green_rotation_coords = [-5, -10, 5, -10, 0, 10]
green_draw_coords = [0, 0, 0, 0, 0, 0]
green_coords = [630, 90]
green_live_status = 1

move_speed = 0.03
turn_speed = 3
torpedo_speed = 6
torpedo_cd = 160
torpedo_size = 2

gravity_well_size = 15

respawn_time = 256
orange_respawn = respawn_time
green_respawn = respawn_time

orange_score = 0
green_score = 0

root = Tk()
c = Canvas (root, width = 720, height = 720, bg = 'black')
c.pack()

gravity_well_coords = [360, 360]
delta_gw_orange_x = 0
delta_gw_orange_y = 0 
orange_to_gravity_well_dist = 0
delta_gw_green_x = 0
delta_gw_green_y = 0
green_to_gravity_well_dist = 0
gravity_circle = c.create_oval(gravity_well_coords[0] - gravity_well_size, gravity_well_coords[1] + gravity_well_size,
                               gravity_well_coords[0] + gravity_well_size, gravity_well_coords[1] - gravity_well_size,
                               fill = 'gray', outline = 'black')

orange = c.create_polygon (orange_rotation_coords, fill = 'orange', outline = 'orange')

orange_hitbox_top = 0
orange_hitbox_bot = 0
orange_hitbox_right = 0
orange_hitbox_left = 0

ot1 = c.create_rectangle (-100, -100, -100, -100, fill = 'red', outline = 'red')
ot1_launched = 0
ot1_cooldown = torpedo_cd
ot1_angle = 0
delta_orange_x_t1 = 0
delta_orange_y_t1 = 0

ot2 = c.create_rectangle (-100, -100, -100, -100, fill = 'red', outline = 'red')
ot2_launched = 0
ot2_cooldown = torpedo_cd
ot2_angle = 0
delta_orange_x_t2 = 0
delta_orange_y_t2 = 0

ot12_cooldown = torpedo_cd / 2

green = c.create_polygon (green_rotation_coords, fill = 'green', outline = 'green')

green_hitbox_top = 0
green_hitbox_bot = 0
green_hitbox_right = 0
green_hitbox_left = 0

gt1 = c.create_rectangle (-100, -100, -100, -100, fill = 'yellow', outline = 'yellow')
gt1_launched = 0
gt1_cooldown = torpedo_cd
gt1_angle = 0
delta_green_x_t1 = 0
delta_green_y_t1 = 0

gt2 = c.create_rectangle (-100, -100, -100, -100, fill = 'yellow', outline = 'yellow')
gt2_launched = 0
gt2_cooldown = torpedo_cd
gt2_angle = 0
delta_green_x_t2 = 0
delta_green_y_t2 = 0

gt12_cooldown = torpedo_cd / 2

orange_text = c.create_text(180, 50, font = ('Consolas', 20), fill = 'orange')
green_text = c.create_text(540, 50, font = ('Consolas', 20), fill = 'green')

c.focus_set()

def key_status(event):
    global toggle, W, A, S, D, SPACE, UP, DOWN, LEFT, RIGHT, ZERO
    if event.keysym == 'w':
        W = 1
    elif event.keysym == 'a':
        A = 1
    elif event.keysym == 's':
        S = 1
    elif event.keysym == 'd':
        D = 1
    elif event.keysym == 'space':
        SPACE = 1
    elif event.keysym == 'Up':
        UP = 1
    elif event.keysym == 'Down':
        DOWN = 1
    elif event.keysym == 'Left':
        LEFT = 1
    elif event.keysym == 'Right':
        RIGHT = 1
    elif event.keysym == '0':
        ZERO = 1
    elif event.keysym == 'p':
        if toggle == 1:
            toggle = 0
        else:
            toggle = 1

c.bind('<KeyPress>', key_status)

def key_status_negative(event):
    global W, S, A, D, SPACE, UP, DOWN, LEFT, RIGHT, ZERO
    if event.keysym in 'w':
        W = 0
    elif event.keysym in 'a':
        A = 0
    elif event.keysym in 's':
        S = 0
    elif event.keysym in 'd':
        D = 0
    elif event.keysym in 'space':
        SPACE = 0
    elif event.keysym in 'Up':
        UP = 0
    elif event.keysym in 'Down':
        DOWN = 0
    elif event.keysym in 'Left':
        LEFT = 0
    elif event.keysym in 'Right':
        RIGHT = 0
    elif event.keysym in '0':
        ZERO = 0

c.bind('<KeyRelease>', key_status_negative)

def gravity_well_orange():
    global orange_x_speed, orange_y_speed, delta_gw_orange_x, delta_gw_orange_y
    global orange_to_gravity_well_dist
    delta_gw_orange_x = orange_coords[0] - gravity_well_coords[0]
    delta_gw_orange_y = orange_coords[1] - gravity_well_coords[1]
    orange_to_gravity_well_dist = math.sqrt(delta_gw_orange_x**2 + delta_gw_orange_y**2)
    orange_x_speed += - (delta_gw_orange_x / 1500000000000) * ((720 - orange_to_gravity_well_dist)**3)
    orange_y_speed += (delta_gw_orange_y / 1500000000000) * ((720 - orange_to_gravity_well_dist)**3)

def orange_move():
    orange_coords[0] += orange_x_speed
    orange_coords[1] += -orange_y_speed

def orange_hitboxes():
    global orange_hitbox_top, orange_hitbox_bot, orange_hitbox_right, orange_hitbox_left
    orange_hitbox_top = orange_coords[1] - R1 - 5
    orange_hitbox_bot = orange_coords[1] + R1 + 5
    orange_hitbox_right = orange_coords[0] + R1 + 5
    orange_hitbox_left = orange_coords[0] - R1 - 5

def orange_destroy():
    global orange_live_status, orange_coords, green_live_status, green_coords
    global orange_score, green_score
    if (gravity_well_coords[0] > orange_hitbox_left) and (gravity_well_coords[0] < orange_hitbox_right):
        if (gravity_well_coords[1] > orange_hitbox_top) and (gravity_well_coords[1] < orange_hitbox_bot):
            orange_coords = [-337, -100]
            orange_live_status = 0
            green_score += 1
    if ((c.coords(gt1)[0] + torpedo_size) > orange_hitbox_left) and ((c.coords(gt1)[0] + torpedo_size) < orange_hitbox_right):
        if ((c.coords(gt1)[1] + torpedo_size) > orange_hitbox_top) and ((c.coords(gt1)[1] + torpedo_size) < orange_hitbox_bot):
            orange_coords = [-337, -100]
            orange_live_status = 0
            green_score += 1
    if ((c.coords(gt2)[0] + torpedo_size) > orange_hitbox_left) and ((c.coords(gt2)[0] + torpedo_size) < orange_hitbox_right):
        if ((c.coords(gt2)[1] + torpedo_size) > orange_hitbox_top) and ((c.coords(gt2)[1] + torpedo_size) < orange_hitbox_bot):
            orange_coords = [-337, -100]
            orange_live_status = 0
            green_score += 1
    if (green_coords[0] > orange_hitbox_left) and (green_coords[0] < orange_hitbox_right):
        if (green_coords[1] > orange_hitbox_top) and (green_coords[1] < orange_hitbox_bot):
            orange_coords = [-337, -100]
            orange_live_status = 0
            green_score += 1
            green_coords = [-100, -337]
            green_live_status = 0
            orange_score += 1
    #крч, так как у меня оранжевый проверяется раньше чем зелёный, я решил что лучше это запихнуть сюда:
"""
    if (orange_coords[0] > green_hitbox_left) and (orange_coords[0] < green_hitbox_right):
        if (orange_coords[1] > green_hitbox_top) and (orange_coords[1] < green_hitbox_bot):
            green_coords = [-100, -337]
            green_live_status = 0
            orange_score += 1
            orange_coords = [-337, -100]
            orange_live_status = 0
            green_score += 1
"""
    #крч, я походу ошибся ))

def orange_screen():
    global orange_coords
    if orange_coords[0] > 724:
        orange_coords[0] = -2
    elif orange_coords[0] < -4:
        orange_coords[0] = 722
    if orange_coords[1] > 724:
        orange_coords[1] = -2
    elif orange_coords[1] < -4:
        orange_coords[1] = 722

def orange_move_binds():
    global orange_x_speed, orange_y_speed
    if W == 1:
        orange_x_speed += move_speed * math.cos ((90 - orange_angle) * 0.0175)
        orange_y_speed += move_speed * math.cos (orange_angle * 0.0175)

def orange_rotate_binds():
    global orange_angle
    if A == 1:
        orange_angle += -turn_speed
    elif D == 1:
        orange_angle += turn_speed

def orange_12_cooldown():
    global ot12_cooldown
    if ot1_launched == 1:
        if ot12_cooldown > 0:
            ot12_cooldown += -1 

def orange_torpedos():
    global ot1_launched, ot1_cooldown, ot1_angle, delta_orange_x_t1, delta_orange_y_t1, ot12_cooldown
    global ot2_launched, ot2_cooldown, ot2_angle, delta_orange_x_t2, delta_orange_y_t2
    orange_x_t = (R1 + 10) * math.cos ((90 - orange_angle) * 0.0175)
    orange_y_t = (R1 + 10) * math.cos (orange_angle * 0.0175)   
    if (SPACE == 1) or (S == 1):
        if ot1_launched == 0:
            ot1_launched = 1
            c.coords(ot1, orange_coords[0] + orange_x_t - torpedo_size, orange_coords[1] - orange_y_t - torpedo_size,
                     orange_coords[0] + orange_x_t + torpedo_size, orange_coords[1] - orange_y_t + torpedo_size)
            delta_orange_x_t1 = orange_x_speed
            delta_orange_y_t1 = -orange_y_speed
            ot1_angle = orange_angle
            ot1_cooldown = torpedo_cd
            ot12_cooldown = torpedo_cd / 2
        elif ot1_launched == 1:
            if ot2_launched == 0:
                if ot12_cooldown == 0:
                    ot2_launched = 1
                    c.coords(ot2, orange_coords[0] + orange_x_t - torpedo_size, orange_coords[1] - orange_y_t - torpedo_size,
                     orange_coords[0] + orange_x_t + torpedo_size, orange_coords[1] - orange_y_t + torpedo_size)
                    delta_orange_y_t2 = -orange_y_speed
                    ot2_angle = orange_angle
                    ot2_cooldown = torpedo_cd

def orange_torpedos_launch():
    global ot1_launched, ot1_cooldown, ot1_angle, delta_orange_x_t1, delta_orange_y_t1  
    if ot1_launched == 1:
        c.move(ot1, delta_orange_x_t1 + math.cos((90 - ot1_angle) * 0.0175) * torpedo_speed,
               delta_orange_y_t1 - math.cos(ot1_angle * 0.0175) * torpedo_speed)
        if ot1_cooldown > 0:
            ot1_cooldown += -1
        elif ot1_cooldown == 0:
            ot1_launched = 0
            c.coords(ot1, -100, -100, -100, -100)

def orange_torpedos_launch_2():
    global ot2_launched, ot2_cooldown, ot2_angle, delta_orange_x_t2, delta_orange_y_t2
    if ot2_launched == 1:
        c.move(ot2, delta_orange_x_t2 + math.cos((90 - ot2_angle) * 0.0175) * torpedo_speed,
               delta_orange_y_t2 - math.cos(ot2_angle * 0.0175) * torpedo_speed)
        if ot2_cooldown > 0:
            ot2_cooldown += -1
        elif ot2_cooldown == 0:
            ot2_launched = 0
            c.coords(ot2, -100, -100, -100, -100)

def orange_draw():
    orange_rotation_coords[0] = - (math.sin (orange_angle * 0.0175 + (math.atan (2/4))) * R2)
    orange_rotation_coords[1] = - (math.cos (orange_angle * 0.0175 + (math.atan (2/4))) * R2)
    orange_rotation_coords[2] = - (math.sin (orange_angle * 0.0175 - (math.atan (2/4))) * R2)
    orange_rotation_coords[3] = - (math.cos (orange_angle * 0.0175 - (math.atan (2/4))) * R2)
    orange_rotation_coords[4] = math.sin (orange_angle * 0.0175) * R1
    orange_rotation_coords[5] = math.cos (orange_angle * 0.0175) * R1
    orange_draw_coords[0] = orange_rotation_coords[0] + orange_coords[0]
    orange_draw_coords[1] = - (orange_rotation_coords[1] - orange_coords[1])
    orange_draw_coords[2] = orange_rotation_coords[2] + orange_coords[0]
    orange_draw_coords[3] = - (orange_rotation_coords[3] - orange_coords[1])
    orange_draw_coords[4] = orange_rotation_coords[4] + orange_coords[0]
    orange_draw_coords[5] = - (orange_rotation_coords[5] - orange_coords[1])
    c.coords (orange, orange_draw_coords[0], orange_draw_coords[1], orange_draw_coords[2],
             orange_draw_coords[3], orange_draw_coords[4], orange_draw_coords[5])



def gravity_well_green():
    global green_x_speed, green_y_speed, delta_gw_green_x, delta_gw_green_y
    global green_to_gravity_well_dist
    delta_gw_green_x = green_coords[0] - gravity_well_coords[0]
    delta_gw_green_y = green_coords[1] - gravity_well_coords[1]
    green_to_gravity_well_dist = math.sqrt(delta_gw_green_x**2 + delta_gw_green_y**2)
    green_x_speed += - (delta_gw_green_x / 1500000000000) * ((720 - green_to_gravity_well_dist)**3)
    green_y_speed += (delta_gw_green_y / 1500000000000) * ((720 - green_to_gravity_well_dist)**3)    

def green_hitboxes():
    global green_hitbox_top, green_hitbox_bot, green_hitbox_right, green_hitbox_left
    green_hitbox_top = green_coords[1] - R1 - 5
    green_hitbox_bot = green_coords[1] + R1 + 5
    green_hitbox_right = green_coords[0] + R1 + 5
    green_hitbox_left = green_coords[0] - R1 - 5

def green_destroy():
    global green_live_status, green_coords, orange_score, orange_live_status, green_score, orange_coords
    if (gravity_well_coords[0] > green_hitbox_left) and (gravity_well_coords[0] < green_hitbox_right):
        if (gravity_well_coords[1] > green_hitbox_top) and (gravity_well_coords[1] < green_hitbox_bot):
            green_coords = [-100, -337]
            green_live_status = 0
            orange_score += 1
    if ((c.coords(ot1)[0] + torpedo_size) > green_hitbox_left) and ((c.coords(ot1)[0] + torpedo_size) < green_hitbox_right):
        if ((c.coords(ot1)[1] + torpedo_size) > green_hitbox_top) and ((c.coords(ot1)[1] + torpedo_size) < green_hitbox_bot):
            green_coords = [-100, -337]
            green_live_status = 0
            orange_score += 1
    if ((c.coords(ot2)[0] + torpedo_size) > green_hitbox_left) and ((c.coords(ot2)[0] + torpedo_size) < green_hitbox_right):
        if ((c.coords(ot2)[1] + torpedo_size) > green_hitbox_top) and ((c.coords(ot2)[1] + torpedo_size) < green_hitbox_bot):
            green_coords = [-100, -337]
            green_live_status = 0
            orange_score += 1
    if (orange_coords[0] > green_hitbox_left) and (orange_coords[0] < green_hitbox_right):
        if (orange_coords[1] > green_hitbox_top) and (orange_coords[1] < green_hitbox_bot):
            green_coords = [-100, -337]
            green_live_status = 0
            orange_score += 1
            orange_coords = [-337, -100]
            orange_live_status = 0
            green_score += 1

def green_screen():
    global green_coords
    if green_coords[0] > 724:
        green_coords[0] = -2
    elif green_coords[0] < -4:
        green_coords[0] = 722
    if green_coords[1] > 724:
        green_coords[1] = -2
    elif green_coords[1] < -4:
        green_coords[1] = 722

def green_move():
    green_coords[0] += green_x_speed
    green_coords[1] += -green_y_speed

def green_move_binds():
    global green_x_speed, green_y_speed
    if UP == 1:
        green_x_speed += move_speed * math.cos ((90 - green_angle) * 0.0175)
        green_y_speed += move_speed * math.cos (green_angle * 0.0175)

def green_rotate_binds():
    global green_angle
    if LEFT == 1:
        green_angle += -turn_speed
    elif RIGHT == 1:
        green_angle += turn_speed

def green_12_cooldown():
    global gt12_cooldown
    if gt1_launched == 1:
        if gt12_cooldown > 0:
            gt12_cooldown += -1 

def green_torpedos():
    global gt1_launched, gt1_cooldown, gt1_angle, delta_green_x_t1, delta_green_y_t1, gt12_cooldown
    global gt2_launched, gt2_cooldown, gt2_angle, delta_green_x_t2, delta_green_y_t2
    green_x_t = (R1 + 10) * math.cos ((90 - green_angle) * 0.0175)
    green_y_t = (R1 + 10) * math.cos (green_angle * 0.0175)   
    if (ZERO == 1) or (DOWN == 1):
        if gt1_launched == 0:
            gt1_launched = 1
            c.coords(gt1, green_coords[0] + green_x_t - torpedo_size, green_coords[1] - green_y_t - torpedo_size,
                     green_coords[0] + green_x_t + torpedo_size, green_coords[1] - green_y_t + torpedo_size)
            delta_green_x_t1 = green_x_speed
            delta_green_y_t1 = -green_y_speed
            gt1_angle = green_angle
            gt1_cooldown = torpedo_cd
            gt12_cooldown = torpedo_cd / 2
        elif gt1_launched == 1:
            if gt2_launched == 0:
                if gt12_cooldown == 0:
                    gt2_launched = 1
                    c.coords(gt2, green_coords[0] + green_x_t - torpedo_size, green_coords[1] - green_y_t - torpedo_size,
                     green_coords[0] + green_x_t + torpedo_size, green_coords[1] - green_y_t + torpedo_size)
                    delta_green_y_t2 = -green_y_speed
                    gt2_angle = green_angle
                    gt2_cooldown = torpedo_cd

def green_torpedos_launch():
    global gt1_launched, gt1_cooldown, gt1_angle, delta_green_x_t1, delta_green_y_t1  
    if gt1_launched == 1:
        c.move(gt1, delta_green_x_t1 + math.cos((90 - gt1_angle) * 0.0175) * torpedo_speed,
               delta_green_y_t1 - math.cos(gt1_angle * 0.0175) * torpedo_speed)
        if gt1_cooldown > 0:
            gt1_cooldown += -1
        elif gt1_cooldown == 0:
            gt1_launched = 0
            c.coords(gt1, -100, -100, -100, -100)

def green_torpedos_launch_2():
    global gt2_launched, gt2_cooldown, gt2_angle, delta_green_x_t2, delta_green_y_t2
    if gt2_launched == 1:
        c.move(gt2, delta_green_x_t2 + math.cos((90 - gt2_angle) * 0.0175) * torpedo_speed,
               delta_green_y_t2 - math.cos(gt2_angle * 0.0175) * torpedo_speed)
        if gt2_cooldown > 0:
            gt2_cooldown += -1
        elif gt2_cooldown == 0:
            gt2_launched = 0
            c.coords(gt2, -100, -100, -100, -100)

def green_draw():
    green_rotation_coords[0] = - (math.sin (green_angle * 0.0175 + (math.atan (2/4))) * R2)
    green_rotation_coords[1] = - (math.cos (green_angle * 0.0175 + (math.atan (2/4))) * R2)
    green_rotation_coords[2] = - (math.sin (green_angle * 0.0175 - (math.atan (2/4))) * R2)
    green_rotation_coords[3] = - (math.cos (green_angle * 0.0175 - (math.atan (2/4))) * R2)
    green_rotation_coords[4] = math.sin (green_angle * 0.0175) * R1
    green_rotation_coords[5] = math.cos (green_angle * 0.0175) * R1
    green_draw_coords[0] = green_rotation_coords[0] + green_coords[0]
    green_draw_coords[1] = - (green_rotation_coords[1] - green_coords[1])
    green_draw_coords[2] = green_rotation_coords[2] + green_coords[0]
    green_draw_coords[3] = - (green_rotation_coords[3] - green_coords[1])
    green_draw_coords[4] = green_rotation_coords[4] + green_coords[0]
    green_draw_coords[5] = - (green_rotation_coords[5] - green_coords[1])
    c.coords (green, green_draw_coords[0], green_draw_coords[1], green_draw_coords[2],
             green_draw_coords[3], green_draw_coords[4], green_draw_coords[5])


def respawn():
    global orange_live_status, orange_respawn, orange_coords, orange_angle, orange_x_speed, orange_y_speed
    global green_live_status, green_respawn, green_coords, green_angle, green_x_speed, green_y_speed
    if orange_live_status == 0:
        orange_respawn += -1
        if orange_respawn == 0:
            orange_coords = [25, 695]
            orange_angle = 0
            orange_live_status = 1
            orange_x_speed = 0
            orange_y_speed = 0
            orange_respawn = respawn_time
    if green_live_status == 0:
        green_respawn += -1
        if green_respawn == 0:
            green_coords = [695, 25]
            green_angle = 180
            green_live_status = 1
            green_x_speed = 0
            green_y_speed = 0
            green_respawn = respawn_time

def text_update():
    c.itemconfig(orange_text, text = orange_score)
    c.itemconfig(green_text, text = green_score)

def main():
    if toggle == 0:
        orange_draw()
        green_draw()
        if orange_live_status == 1:
            orange_destroy()
            orange_move_binds()
            orange_rotate_binds()
            gravity_well_orange()
            orange_move()
            orange_hitboxes()
            orange_screen()
            orange_12_cooldown()
            orange_torpedos()
            orange_torpedos_launch()
            orange_torpedos_launch_2()
        if green_live_status == 1:
            green_destroy()
            green_move_binds()
            green_rotate_binds()
            gravity_well_green()
            green_move()
            green_hitboxes()
            green_screen()
            green_12_cooldown()
            green_torpedos()
            green_torpedos_launch()
            green_torpedos_launch_2()
        respawn()
        text_update()
    root.after(16,main)

main()
root.mainloop()