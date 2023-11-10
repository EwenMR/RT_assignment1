from __future__ import print_function

import time
from sr.robot import *

closest_token_offset = None

a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""

size  = 0

R = Robot()
""" instance of the class Robot"""


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

def robot_size():
    global size
    for marker in R.see():
        size = marker.info.size/2

    return size

def find_regrouping_token():
    global closest_token_offset
    if closest_token_offset is not None:
        return closest_token_offset
    
    dist = 100
    for token in R.see():
        if token.dist < dist and closest_token_offset is None:
            dist  = token.dist
            closest_token_offset = token.info.offset

    return closest_token_offset

def go_home():
    ghdist = 100
    for token in R.see():
        if token.info.marker_type is MARKER_TOKEN_GOLD and token.info.offset is closest_token_offset:
            ghdist = token.dist
            ghrot_y = token.rot_y
    if ghdist == 100:
        return -1, -1
    else:
        return ghdist, ghrot_y

def find_golden_token():
    """
    Function to find the closest golden token

    Returns:
        dist (float): distance of the closest golden token (-1 if no golden token is detected)
        rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist = 100
    for token in R.see():
        if token.info.offset is not closest_token_offset:
            if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD:
                dist = token.dist
                rot_y = token.rot_y
        if dist == 100:
            return -1, -1
        else:
            return dist, rot_y


while 1:
    
        dist, rot_y = find_golden_token()
        ghdist, ghrot_y = go_home()
        closest_token_offset = find_regrouping_token()
        size = robot_size()
        if dist == -1:  # if no token is detected, we make the robot turn
            print("I don't see any token!!")
            turn(+10, 1)
        elif dist < d_th:  # if we are close to the token, we try grab it.
            print("Found it!")
            if R.grab():  # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
                print("Gotcha!")
                # go home part
                if ghdist < size:
                    print("Let me drop this off")
                    R.release()
                elif -a_th <= ghrot_y <= a_th:
                    print("Ah, that'll do.")
                    drive(10, 0.5)
                elif ghrot_y < -a_th:  # if the robot is not well aligned with the token, we move it on the left or on the right
                    print("Left a bit...")
                    turn(-2, 0.5)
                elif ghrot_y > a_th:
                    print("Right a bit...")
                    turn(+2, 0.5)
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
