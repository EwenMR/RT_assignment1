rom __future__ import print_function

import time
from sr.robot import *


rgrping_point = None
rgrping_offset = None

a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

silver = True
""" boolean: variable for letting the robot know if it has to look for a silver or for a golden marker"""

R = Robot()
""" instance of the class Robot"""
def go_home():

    if check_grab():
        if -rgrp_rot <= rot_y <= rgrp_rot:  # if the robot is well aligned with the home token, we go forward
            print("Ah, that'll do.")
            drive(10, 0.5)
            if dist < token.info.size/2
                R.release()
        elif rot_y < -rgrp_rot:  # if the robot is not well aligned with the token, we move it on the left or on the right
            print("Left a bit...")
            turn(-2, 0.5)
        elif rot_y > rgrp_rot:
            print("Right a bit...")
            turn(+2, 0.5)

def set_rgrping_point():

    min_dist = 100
    if token.info.marker_type == MARKER_TOKEN_GOLDEN:
        if token.centre.dist<min_dist:
            min_dist = token.centre.dist
            rgrping_point = token.centre
            rgrping_offset = token.info.offset
            rgrp_rot = token.rot_y

            return rgrp_rot
            return rgrping_point
            return rgrping_offset

def check_grab():

    ind = 0
    count = 0

    while count < 5:
        token_in_view = R.see()
        if ind < len(token_in_view):
            token = token_in_view[ind]
            if token.info.marker_type is MARKER_TYPE_GOLD
                if token.info.offset != rgrping_offset and not in placed_boxes:
                    R.grab()
                    placed_boxes.append(token.info.offset)
                    count+=1
                else
                    #look for another box
                ind+=1

def drive(speed, seconds):
    """
    Function for setting a linear velocity

    Args: speed (int): the speed of the wheels
          seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0


def turn(speed, seconds):
    """
    Function for setting an angular velocity

    Args: speed (int): the speed of the wheels
          seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0



def find_golden_token():
    """
    Function to find the closest golden token

    Returns:
        dist (float): distance of the closest golden token (-1 if no golden token is detected)
        rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist = 100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
            if token.info.offset != rgrping_offset and not in placed_boxes:
                dist = token.dist
                rot_y = token.rot_y
    if dist == 100:
        return -1, -1
    else:
        return dist, rot_y


while 1:

    rgrping_point, rgrping_offset = set_rgrping_point()
    dist, rot_y = find_golden_token()
    if dist == -1:  # if no token is detected, we make the robot turn
        print("I don't see any token!!")
        turn(+10, 1)
    elif dist < d_th:  # if we are close to the token, we try grab it.
        print("Found it!")
        R.check_grab()
            if R.grab():  # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
            print("Gotcha!")
            R.go_home()
        else:
            print("Aww, I'm not close enough.")
    elif -a_th <= rot_y <= a_th:  # if the robot is well aligned with the token, we go forward
        print("Ah, that'll do.")
        drive(10, 0.5)
    elif rot_y < -a_th:  # if the robot is not well aligned with the token, we move it on the left or on the right
        print("Left a bit...")
        turn(-2, 0.5)
    elif rot_y > a_th:
        print("Right a bit...")
        turn(+2, 0.5)