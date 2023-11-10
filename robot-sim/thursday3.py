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
    for token in R.see():
            if token.info.offset not in regroup:
                if token.dist<dist:
                    dist = token.dist
                    rot_y = token.rot_y
                    offset = token.info.offset

            if dist == 100:
                return -1,-1,-1
            else:
                return dist, rot_y, offset
            

def find_regroup(regroup):
    dist  = 100
    for token in R.see():
            if token.info.offset in regroup:
                dist = token.dist
                rot_y = token.rot_y
                

            if dist == 100:
                return -1,-1,-1
            else:
                return dist, rot_y
            
def go_to_token(regroup):
    while 1:

        dist, rot_y, offset = find_token(regroup)

        if dist == -1:  # if no token is detected, we make the robot turn
            print("I don't see any token!!")
            turn(+10, 1)
        elif dist < d_th:  # if we are close to the token, we try grab it.
            print("Found it!")
            if R.grab():  # if we grab the token, we move the robot forward and on the right, we release the token, and we go back to the initial position
                print("Gotcha!")
                return offset
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

    
def go_to_regroup(regroup):

    dist, rot_y  = find_regroup(regroup)

    while 1 :
        if dist == -1:
            print("I'm blind")
            turn(-2,0.5)
        elif dist < 0.9:
            break
        elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the goal, we go forward
            print("Ah, here we are!.")
            if dist>d_th:
                drive(50,1)
            else:
                drive(10, 0.5)
        elif rot_y < -a_th: # if the robot is not well aligned with the goal, we move it on the left or on the right
            print("Left a bit...")
            turn(-2, 0.5)
        elif rot_y > a_th:
            print("Right a bit...")
            turn(+2, 0.5)

regroup = []
search =  True

while 13:

    if search :
        offset = go_to_token(regroup)
        regroup.append(offset)
        search =False
    else:
        go_to_regroup(regroup)
        R.release()
        print("delivery")
        drive(-15,1)
        turn(30,1)
        drive(50,1)
        search = True