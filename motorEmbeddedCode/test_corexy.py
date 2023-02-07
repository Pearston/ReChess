import corexyLib
import motorLib
from time import sleep
import RPi.GPIO as GPIO

SQUARE_SIDE = 57.3
resolution = 'Half'
corexy = corexyLib.CoreXY(20, resolution, motorLib.Motor(20, 21, 1, (14, 15, 18), 400, resolution), motorLib.Motor(19, 26, 1, (14, 15, 18), 400, resolution), 0, 0)
corexy.motorA.initial_set_up()
corexy.motorB.initial_set_up()
GPIO.setup(5, GPIO.OUT)

# Assume origin at the up left corner of square(1,1)
def cal_xy_coor(row, col):
    x_coor = ((row-1)+ (1/2)) * SQUARE_SIDE
    y_coor = ((col-1) + (1/2)) *SQUARE_SIDE

    return x_coor, y_coor

GPIO.output(5, GPIO.HIGH)
while(True):

    corexy.move_up(2500)
    corexy.move_down(2500)
    corexy.move_left(2500)
    corexy.move_right(2500)
    corexy.move_down(2500)
    corexy.move_up(2500)
    corexy.move_right(2500)
    corexy.move_left(2500)

GPIO.output(5, GPIO.LOW)
corexy.move_up(2500)
corexy.move_down(2500)
# corexy.move_left(5424)
# corexy.move_down(6630)

# corexy.motorA.motor_steps(5000)
# corexy.motorA.set_counter_clockwise()
# corexy.motorA.motor_steps(5000)

# while True:

#     row = int(input("Enter row: "))
#     col = int(input("Enter col: "))

#     new_x_coor, new_y_coor = cal_xy_coor(row, col)

#     corexy.move_to(new_x_coor, new_y_coor)






