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

        
def find_token():
    """ 
    This is a function to find the closest token that hasn't 
    been hasn't been picked up yet (not in the regroup array).

    Returns:
        dist (float): distance of the closest token (-1 if no token is detected)
        rot_y (float): angle between the robot and the token (-1 if no token is detected)
        code (int): code number of the token the robot sees (-1 if not token is detected)
    """

    dist = 100
    
    for token in R.see():
        if token.dist < dist and (token.info.code not in regroup):
            dist = token.dist
            rot_y = token.rot_y
            code = token.info.code
    if dist ==100:
        return -1,-1,-1
    else:
        return dist, rot_y, code
        

def find_regroup():
    """
    This is a function to find the group of tokens in the array regroup

    Returns:
        rdist (float): distance of the closest token with its code in the regroup array (-1 if no token is detected)
        rro_ty (float): angle between the robot and a token in the regroup array (-1 if no token is detected)
    """

    rdist = 100

    for token in R.see():
        if token.info.code in regroup:
            rdist = token.dist 
            rrot_y = token.rot_y

    if rdist == 100:
        return -1,-1
    else:
        return rdist, rrot_y


def first_time():
    """
    This function is a list of code to execute when grabbing the first token.
    This function was made to make the main code slighlty easier to read.
    """
    turn(60,1)
    R.release()
    drive(-30,1)
    print("released")
    regroup.append(code)


# regroup array will store all tokens picked up 
regroup=[] 

# Search will be used to execute two different loosp, when search is true we are searching for a new token to grab
# when search is false we are looking for the group of tokens in the regroup array
search = True

# first will be used to execute the function first_time when the robot goes to pick up the first
# token. We want the first token to become the starting point for the regroupment.
first = 1

x = 6

while 1:

    if len(regroup) == x:
        print("All boxes have been gathered together.")
        break

    # we are searching for a token that hasn't been picked up
    if search is True:
        
        #  get dist, rot_y and code from the function find_token()
        dist, rot_y, code = find_token()

        # if the robot can't see anything then turn to try find something
        if dist == -1:
            print("I don't see any token to pick up :(")
            turn(-20,0.5)

        # if dist is equal or smaller than the threshold distance then the robot can grab the token
        elif dist <= d_th:
            print("I am able to reach the box")
            
            # if the robot grabs a token then search becomes false and if it is the first token grabbed execute
            # the first_time function
            if R.grab():                
                print("Got'cha!")
                search = False
                if first == 1:
                    first_time()
                    first = 0
                    search = True
              
            else:
                # failed grab error msg and back up to try again
                print("My hands are too small :)")
                drive(-20,1)
            
        # the robot is in line with the token
        elif -a_th < rot_y < a_th:
            print("The token is straight ahead of me")
            drive(40,0.01)
        # correcting the angle
        elif rot_y < -a_th:
            print("Lefty a little...")
            turn(-2,0.01)
        # correcting the angle
        elif rot_y > a_th:
            print("Righty a little...")
            turn(+2,0.01)


    # this is the case when we are searching for the regroupment
    else:
        # get the rdist, and rrot_y from the find_regroup() function
        rdist, rrot_y = find_regroup()

        # if the robot can't see anything then turn to try find something
        if rdist == -1:
            print("I'm lostn I can't find the group :/")
            turn(+40,0.01)
        # if we are within the threshold then release the object and search becomes true to look for another token
        elif rdist <= d_th+0.28:
            R.release()
            drive(-30,1)
            regroup.append(code)
            search = True
            print(search)
        # robot in line with token
        elif -a_th < rrot_y < a_th:
            drive(50,0.01)
            print("The group is right in font of me!")
        # adjusting agnle
        elif rrot_y < -a_th:
            print("Turn a little left")
            turn(-2,0.01)
        # adjusting angle
        elif rrot_y > a_th:
            print("Turn a little right")
            turn(+4,0.01)