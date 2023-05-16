# importing modules
from controller import Robot, Motor, Camera, TouchSensor
import math


# Constants
TIME_STEP = 64 #timestep for the robot
MAX_SPEED = 6.67 # maximum speed attainable by the robot
RED_THRESHOLD = 1.5
GREEN_THRESHOLD = 1.5
BLUE_THRESHOLD = 1.5
MIN_OBJECT_SIZE = 50000 # minimum size for the object to be detected
left_speed = 0 #initilaising speeds
right_speed = 0


# Initialize the robot
robot = Robot()
#Initialise wheels
left_wheel = robot.getDevice('left wheel motor')
right_wheel = robot.getDevice('right wheel motor')
left_wheel.setPosition(float('inf')) # setting wheels to rotate indefinitely
right_wheel.setPosition(float('inf'))
left_wheel.setVelocity(0.0) # initial speed
right_wheel.setVelocity(0.0)

# Initialise camera
camera = robot.getDevice('camera')
camera.enable(TIME_STEP)  # enabling the camera with the time step

# Initialise and enable the touch sensors
front_touch_sensor = robot.getDevice('front touch sensor')
left_touch_sensor = robot.getDevice('left touch sensor')
right_touch_sensor = robot.getDevice('right touch sensor')
front_touch_sensor.enable(TIME_STEP)
left_touch_sensor.enable(TIME_STEP)
right_touch_sensor.enable(TIME_STEP)

# Set up wheels
left_wheel.setPosition(float('inf'))
right_wheel.setPosition(float('inf'))
left_wheel.setVelocity(0.0)
right_wheel.setVelocity(0.0)

# Functions to determine what color the pixel is
def is_red_pixel(r, g, b):
    return r > RED_THRESHOLD * g and r > RED_THRESHOLD * b

def is_green_pixel(r, g, b):
    return g > GREEN_THRESHOLD * r and g > GREEN_THRESHOLD * b

def is_blue_pixel(r, g, b):
    return b > BLUE_THRESHOLD * r and b > BLUE_THRESHOLD * g

# Function to detect colored objects in the camera image
def detect_colored_objects(camera_image, min_object_size):
    height = camera.getHeight() # height of image
    width = camera.getWidth()   # width of image

    detected_colors = {'red': False, 'green': False, 'blue': False}
    color_areas = {'red': 0, 'green': 0, 'blue': 0}

# iterate over each pixel
    for y in range(height):
        for x in range(width):
            r, g, b = camera_image[y][x] # get the color values of the pixel
            # incrementing the area of the color if the pixel is that color
            if is_red_pixel(r, g, b):
                color_areas['red'] += 1
            if is_green_pixel(r, g, b):
                color_areas['green'] += 1
            if is_blue_pixel(r, g, b):
                color_areas['blue'] += 1
#  if the color area is above the minimum size, consider it detected
    for color, area in color_areas.items():
        if area > min_object_size:
            detected_colors[color] = True

    return detected_colors


def turn_degrees(degrees, left_wheel, right_wheel):
    # adjusting speed of turn
    speed_ratio = 1.0
    # time needed for the robot to turn
    turn_time = abs(degrees) * 6.67 / (360 * speed_ratio)
    # if degrees is positive, the robot should turn right by setting the left wheel to move forward and the right wheel backward.
    if degrees > 0:
        left_speed = MAX_SPEED
        right_speed = -MAX_SPEED
    # if degrees is negative, the robot should turn left
    else:
        left_speed = -MAX_SPEED
        right_speed = MAX_SPEED

    left_wheel.setVelocity(left_speed)
    right_wheel.setVelocity(right_speed)
    # robot then steps for the calculated amount of time
    robot.step(int(turn_time * 1000))
    robot.step(TIME_STEP)

# main loop
while robot.step(TIME_STEP) != -1:
    # get the camera image
    camera_image = camera.getImageArray()

    # detect colored objects in the camera image
    detected_colors = detect_colored_objects(camera_image, MIN_OBJECT_SIZE)


    # get the touch sensor values
    is_front_touching = front_touch_sensor.getValue() > 0.0
    is_left_touching = left_touch_sensor.getValue() > 0.0
    is_right_touching = right_touch_sensor.getValue() > 0.0

    # change behavior based on touch sensors and detected colors
    if is_front_touching:
    # Reverse a little bit and then turn slightly right
        left_speed, right_speed, msg = -0.5 * MAX_SPEED, -MAX_SPEED, "Front obstacle detected, backing up and turning"
        left_wheel.setVelocity(left_speed)
        right_wheel.setVelocity(right_speed)
        robot.step(1000) # back up for one second
        left_speed, right_speed = 0.5 * MAX_SPEED, MAX_SPEED,  # now take a turn slighly
    elif is_left_touching:
    # take a slight turn towards right
        left_speed, right_speed, msg = 0.75 * MAX_SPEED, 0.5 * MAX_SPEED, "Left obstacle detected, veering right"
    elif is_right_touching:
    # take a slight turn towards left
        left_speed, right_speed, msg = 0.5 * MAX_SPEED, 0.75 * MAX_SPEED, "Right obstacle detected, veering left"

    elif detected_colors['green']:
        turn_degrees(30, left_wheel, right_wheel)
        left_speed, right_speed, msg = 0, 0, "Green object detected, turning right"
    elif detected_colors['blue']:
        turn_degrees(-30, left_wheel, right_wheel)
        left_speed, right_speed, msg = 0, 0, "Blue object detected, turning left"
    elif detected_colors['red']:
         left_speed, right_speed, msg = 0,0, "Red detected, stopping"
    else:
        left_speed, right_speed = MAX_SPEED, MAX_SPEED

    left_wheel.setVelocity(left_speed), right_wheel.setVelocity(right_speed)
    #print statements
    if 'msg' in locals():
        print(msg)