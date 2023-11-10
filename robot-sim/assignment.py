from __future__ import print_function

import time
from sr.robot import *

a_th = 2.0
""" float: Threshold for the control of the orientation"""
d_th = 0.3
""" float: Threshold for the control of the linear distance"""


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

def find_token(regroup):

    dist = 100

    for token in R.see(regroup):
        if token.info.offset not in regroup:
            if token.dist < dist:
                dist = token.dist
                rot_y = token.rot_y
                offset = token.info.offset
        else:
            dist = token.dist
            rot_y = token.rot_y
            offset = token.info.offset
    if dist  == -1:
        return -1,-1,-1
    else:
        return dist, rot_y, offset


while 1:

    regroup = []
    dist, rot_y, offset  = find_token(regroup)

    if dist == -1:
        print("I can't see")
        turn(-2,0.5)
    elif dist < d_th:
        print("i found it")
        if R.grab():
            print("gotu")
            regroup.append(offset)
            print(f"Box {regroup} has been captured")
        else:
            print("awww man")

    elif -a_th <= rot_y <= a_th:  # if the robot is well aligned with the token, we go forward
        print("Ah, that'll do.")
        drive(10, 0.5)
    elif rot_y < -a_th:  # if the robot is not well aligned with the token, we move it on the left or on the right
        print("Left a bit...")
        turn(-2, 0.5)
    elif rot_y > a_th:
        print("Right a bit...")
        turn(+2, 0.5)