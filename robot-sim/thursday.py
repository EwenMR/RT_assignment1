from __future__ import print_function

import time
from sr.robot import *

a_th = 2.0
""" float: Threshold for the control of the orientation"""
d_th = 0.4
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

def make_regroup():

    dist = 100
    for token in R.see():
        if not regroup:
            if token.dist< dist:
                code = token.info.code
        if dist == -1:
            return -1
        else:
            return code
        
def find_token():

    dist = 100
    rot_y = 0
    code = 0

    for token in R.see():
        if token.dist < dist and token.info.code not in regroup:
            dist = token.dist
            rot_y = token.rot_y
            code = token.info.code
        if dist == -1:
            return -1,-1,-1
        else:
            return dist, rot_y, code
        
def find_regroup():

    dist = 100
    rot_y = 0

    for token in R.see():
        if token.info.code in regroup:
            dist = token.dist 
            rot_y = token.rot_y
        if dist == -1:
            return -1,-1
        else:
            return dist, rot_y

search = True        
while 1:

    regroup = []

    if not regroup:
        code = make_regroup()
        regroup.append(code)

    dist, rot_y, code = find_token()
    if search:
    
    
        print(f"This is the distance {dist}")

        if dist == -1:
            print("I am blind for real")
            turn(-20,0.5)
        elif dist <= d_th:
            print("I am able to reach the box")
            if R.grab():
                print("gotcha")
                for token in R.see():
                    if token.dist <= d_th:
                        regroup.append(code)
                search = False
            else:
                print("my arms are too small")
                drive(-20,1)
        # the robot is in line with the token
        elif -a_th < rot_y < a_th:
            print("straight ahead")
            drive(30,0.5)
        # correcting the angle
        elif rot_y < -a_th:
            print("lefty")
            turn(-2,0.5)
        # correcting the angle
        elif rot_y > a_th:
            print("righty")
            turn(+2,0.5)

        dist, rot_y = find_regroup()
    else:

        if dist ==-1:
            print("I can't see a thing")
            turn(-20,0.5)
        elif dist > d_th:
            if rot_y < -a_th:
                print("lefty")
                turn(-2,0.5)
            elif rot_y > a_th:
                print("righty")
                turn(+2,0.5)   
            elif -a_th < rot_y < a_th:
                drive(25,0.1) 
        elif dist < d_th:
            if not regroup:
                R.release()
                regroup = True
                drive(-20,1)        

    
