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

def find_token(search):

    dist = 100

    for token in R.see():
        if search:
            if token.info.offset not in regroup:
                if token.dist < dist:
                    dist = token.dist
                    rot_y = token.rot_y
                    offset = token.info.offset
        else:
            if token.info.offset in regroup:
                dist = token.dist
                rot_y = token.rot_y
                offset = token.info.offset
        
    if dist == 100:
        return -1,-1,-1
    else:
        return dist, rot_y, offset
    
# def find_regroup(search):

#     if not search:

#         while 13:
#             dist, rot_y =  find_token(search)

#             if dist == -1:
#                 print("Im blind")
#                 turn(-20,0.5)
#             elif dist < d_th:
#                 break
#             elif -a_th <= rot_y <= a_th:
#                 print("I see it")
#                 drive(10,0.5)
#             elif rot_y > a_th:
#                 print("right a bit")
#                 turn(+2,0.5)
#             elif rot_y < -a_th:
#                 print("left a bit")
#                 turn(-2,0.5)

# def find_next_token(search):

#     if search:
#         dist, rot_y, offset = find_token(search)
#         if dist == -1:
#             print("I really am blind")
#             turn(-20,0.5)
#         if dist >= 0.7:
#             drive(50,1)
#             dist, rot_y, offset = find_token(search)

#         elif dist > d_th:
#             drive(10,1)
#             dist, rot_y, offset = find_token(search)

#         elif rot_y< -a_th:
#             turn(-2,0.5)

#         elif rot_y > a_th:
#             turn(2,0.5)

#         R.grab()
#         return offset
    
# search = True
# while 13:

#     regroup = []
#     for i in range(6):
#         offset = find_next_token(search)
#         regroup.append(offset)
#         search = False
#         find_regroup(search)
#         R.release()
#         drive(-15,1)
#         turn(30,1)
#         drive(50,1)
#         search = True

search = True
while 13:

    regroup=[]
    dist, rot_y, offset = find_token(search)

    if not regroup:
        regroup.append(offset)

    if dist == -1:
        print("I'm blind")
        turn(+10,1)
    elif dist< d_th:
        print("found it")
        if search:
            if R.grab():
                for marker in R.see():
                    if marker.dist <= d_th:
                        regroup.append(offset)
                search = False

        else:
            R.release()
            search = True
    elif -a_th <= rot_y <= a_th:  # if the robot is well aligned with the token, we go forward
        print("Ah, that'll do.")
        drive(10, 0.5)
    elif rot_y < -a_th:  # if the robot is not well aligned with the token, we move it on the left or on the right
        print("Left a bit...")
        turn(-2, 0.5)
    elif rot_y > a_th:
        print("Right a bit...")
        turn(+2, 0.5)
 
# while 13:

#     regroup = []
#     dist, rot_y, offset = find_token(regroup)

#     if not regroup:
#         regroup.append(offset)

#     if dist == -1:
#         print("I am blind for good")
#         turn(-20,0.5)
#     if dist > 0.4:

#         if rot_y > a_th:
#             print("turn righttt")
#             turn(+2,0.5)
#         elif rot_y < -a_th:
#             print("tunr lefty")
#             turn(-2,0.5)
#         else:
#             drive(20,1)
#     else:
#         if search:
#             if R.grab():
#                 search = False
#                 print("got you")
#                 regroup.append(offset)
                

#             else:
#                 print("grab failed")
#                 drive(-10,2)
#         else:
#             R.release()
#             search = True


