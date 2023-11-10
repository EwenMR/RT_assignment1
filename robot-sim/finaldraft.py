from __future__ import print_function

import time
from sr.robot import *


a_th = 2.0
""" float: Threshold for the control of the linear distance"""

d_th = 0.4
""" float: Threshold for the control of the orientation"""


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

def find_token():
    """
    Function to find the closest golden token

    Returns:
        dist (float): distance of the closest golden token (-1 if no golden token is detected)
        rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
    """
    dist = 100
    for token in R.see():
        if token.info.offset in home:
            dist = token.dist
            rot_y = token.rot_y
            offset = token.info.offset

        elif token.info.offset not in home:
            if token.dist < dist:
                dist = token.dist
                rot_y = token.rot_y
                offset = token.info.offset
    if dist == 100:
        return -1,-1,-1
    else:
        return dist, rot_y, offset

# def find_golden_token(marker_code=None):
#     """
#     Function to find the closest golden token

#     Returns:
#         dist (float): distance of the closest golden token (-1 if no golden token is detected)
#         rot_y (float): angle between the robot and the golden token (-1 if no golden token is detected)
#     """
#     dist = 100
#     for token in R.see():
#         if marker_code is not None:
#             if token.dist < dist and not home:
#                 dist = token.dist
#                 rot_y = token.rot_y
#                 offset = token.info.offset
#             if dist == 100:
#                 return -1, -1, -1
#             else:
#                 return dist, rot_y, offset

# def find_home(marker_code):
#     dist = 100
#     for token in R.see():
#         if token.info.offset in home:
#             dist = token.dist
#             rot_y = token.rot_y
#         if dist == 100:
#             return -1, -1
#         else:
#             return dist, rot_y
        
def go_home(home):
    while 1:
        dist, rot_y = find_token(home)
        if dist == -1:  # if no token is detected, we make the robot turn
            print("I don't see any token!!")
            turn(-5,0.5)
        elif dist < 0.8:  # if we are close to the token, we try grab it.
            break
        elif -a_th <= rot_y <= a_th:  # if the robot is well aligned with the token, we go forward
            print("Ah, that'll do.")
            while dist > 1:
                drive(50,1)
            else:
                drive(10, 0.5)
        elif rot_y < -a_th:  # if the robot is not well aligned with the token, we move it on the left or on the right
            print("Left a bit...")
            turn(-2, 0.5)
        elif rot_y > a_th:
            print("Right a bit...")
            turn(+2, 0.5)

# def pickitup():
#     dist, rot_y = find_golden_token()
#     if dist == -1:
#          print("error")
#          turn(+10,1)
#     elif dist < d_th:
#         print("Found it")
#         R.grab()
        
#     elif -a_th <= rot_y <= a_th:
#          print("lets go")
#          drive(10,0.5)
#     elif rot_y > a_th:
#             print("right")
#             turn(2,0.5)
#     elif rot_y < -a_th:
#              print("left")
#              turn(-2,0.5)
#     return offset

while 13:
    home = []
    dist, rot_y, offset = find_token()

    if not home:
        print("made a home")
        home.append(offset)

    if dist == -1:
        print("i'm blind")
        turn(-20,0.5)
    elif dist > d_th:
        drive(50,1)
    elif -a_th > rot_y or rot_y > a_th:
        turn(10,0.1)
    elif dist < d_th:
        drive(10,1)
    R.grab()
    offset = offset
    turn(60,1)
    go_home(home)
    R.release()
    drive(-15,1)
    turn(30,1)
    drive(50,1)           
# grabbed = None        
# while 1:

#     home =[]

#     dist, rot_y, offset = find_home(grabbed)
    
#     if not home:
#         # lets choose the first box as the place we throw them all
#         print("Powiedz mi ze nie jestes tutaj")
#         home.append(offset)
    
    
#     if dist == -1:
#         # It either sees no boxes or no boxes
#         print("I dont see anything interesting")
#         turn(-20, 0.5)
#     elif dist > d_th :
#         # Robot sees marker
#         if rot_y > a_th:
#             # Rotate right
#             print("Right a bit...")
#             turn(2, 0.5)
#         elif rot_y < -a_th:  
#             # Rotate left 
#             print("Left a bit...")
#             turn(-2, 0.5)
#         else:
#             # Robot is oriented on the target, drive forward.
#             print("Ah, that'll do.")
#             if dist > 2.5*d_th:
#                 drive(3*35, 0.1)
#             else:
#                 drive(10, 0.5)
#     else:
#         # Robot is within threshold
#         if not grabbed:
#             # if current marker is empty, we are looking for  
#             if R.grab(): 
#                 # Robot grabbed the box
#                 print("Gotcha!")
#                 # set our main goal to the first marker
#                 for marker in R.see():
#                     if marker.dist <= d_th:
#                         home.append(offset)
#                 print(f"This is the list {home} and this is the list without the last element {home[:-1]}")
#                 grabbed = home[0]
#                 d_th = 1.5*d_th
#                 time.sleep(1)

#             else:
#                 print("Grab failed")
#         else:

#             R.release()
#             print("Box dumped")
#             grabbed = None
#             d_th = d_th / 1.5
#             print(home)
#             drive(-20, 3)
#             turn(10,2)
    

        
    
#     print(print(f"Closest marker {offset} is {dist} away and {rot_y}"))
#     print(R.see())

        # while 1:
        #     dist, rot_y = go_home(home)
        #     if dist == -1:
        #         print("i cant see")
        #         exit()
        #     elif dist < 1:
        #         break
        #     elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the goal, we go forward
        #         print("Ah, here we are!.")
        #         if dist> 1:
        #             drive(50,1)
        #         else:
        #             drive(10, 0.5)
        #     elif rot_y < -a_th: # if the robot is not well aligned with the goal, we move it on the left or on the right
        #         print("Left a bit...")
        #         turn(-2, 0.5)
        #     elif rot_y > a_th:
        #         print("Right a bit...")
        #         turn(+2, 0.5)


    #     home.append(offset)
    #     go_home(home)
    # elif -a_th <= rot_y <= a_th:  # if the robot is well aligned with the token, we go forward
    #     print("Ah, that'll do.")
    #     drive(10, 0.5)
    # elif rot_y < -a_th:  # if the robot is not well aligned with the token, we move it on the left or on the right
    #     print("Left a bit...")
    #     turn(-2, 0.5)
    # elif rot_y > a_th:
    #     print("Right a bit...")
    #     turn(+2, 0.5)
    
    # i = 0
    # while i < 6:
    #     offset = pickitup
    #     home.append(offset)
    #     while 13:
    #         hdist, hrot_y = find_home()
    #         if hdist == -1:
    #             print("I don't see the goal!!")
    #             turn(-20,0.5)
    #         elif hdist < 1: 
    #             break
    #         elif -a_th<= hrot_y <= a_th: # if the robot is well aligned with the goal, we go forward
    #             print("Ah, here we are!.")
    #             if hdist>1:
    #                 drive(50,1)
    #             else:
    #                 drive(10, 0.5)
    #         elif hrot_y < -a_th: # if the robot is not well aligned with the goal, we move it on the left or on the right
    #             print("Left a bit...")
    #             turn(-2, 0.5)
    #         elif hrot_y > a_th:
    #             print("Right a bit...")
    #             turn(+2, 0.5)
    # R.release()
    # drive(-15,1)
    # turn(30,1)
    # drive(50,1)


    #     dist, rot_y, offset = find_golden_token(home)
    #     if dist == -1:  # if no token is detected, we make the robot turn
    #         print("I don't see any token to pick up")
    #     while dist >= 1:
    #         if -a_th <= rot_y <= a_th:
    #             drive(50,1)

    #     while dist>d_th:
    #         drive(10,1)
    #         R.grab()
    #         offset1 = offset

    # home.append(offset)
    # turn(60,1)
    # go_home(home)
    # R.release()
    # drive(-15,1)
    # turn(30,1)
    # drive(50,1)