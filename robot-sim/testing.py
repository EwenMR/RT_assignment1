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
        
def find_token(search):

    dist = 100

    for token in R.see():
        if search:
            if token.dist < dist and token.info.code not in regroup:
                dist = token.dist
                rot_y = token.rot_y
                code = token.info.code
            else:
                print(f"This fella no {token.info.code} was already collected")
                dist = 100 # Make sure we are not following this one 
        else:
            if token.info.code in regroup:
                dist = token.dist
                rot_y = token.rot_y
                code = token.info.code

        if dist == 100:
        # Robot does not see a box that we are interested in the range
            return -1, -1, -1
        else:
            return dist, rot_y, code
    
        
regroup=[] 
search = True
while 1:


  
    # dist, rot_y, code = find_token(search)
    
    # if not regroup:
    #     # the first, nearest box is set as the point where we group alll
    #     regroup.append(code)
    
    
    # if dist == -1:
    #     # doesnt see boxes that it is looking for
    #     print("I dont see anything interesting")
    #     turn(-35, 0.2)
    # elif dist > d_th :
    #     # Robot sees marker
    #     if rot_y > a_th:
    #         # Rotate right
    #         print("Turning right a bit...")
    #         turn(2, 0.2)
    #     elif rot_y < -a_th:  
    #         # Rotate left 
    #         print("Turning left a bit...")
    #         turn(-2, 0.2)
    #     else:
    #         # Robot is oriented on the target, drive forward.
    #         print(f"Driving towards box no {code}")
    #         # adapt velocity to the distance
    #         if dist >= 2*d_th:
    #             # Robot is far from the target, go fast
    #             speed = 10 * dist * 25
    #             drive(speed, 0.2)
    #         else:
    #             # slow down for precise driving, we need to ensure that grab will be succesful
    #             drive(25, 0.1)
    # else:
    #     # Robot is within dist_threshold
    #     if regroup:
    #         # Grab the closest object
    #         if R.grab(): 
    #             # Robot grabbed the box
    #             print("Gotcha!")
    #             # Add this box to the captured
    #             for token in R.see():
    #                 if token.dist <= d_th:
    #                     regroup.append(code)
    #             # Switch mode to find the group
    #             regroup = False
    #         else:
    #             # Go back to make another attempt
    #             print("Grab failed")
    #             drive(-20, 3)
    #     else:
    #         # Drop the box
    #         R.release()
    #         regroup = True
        
    #         print(f"Box {regroup[-1]} dumped") # The last element is the Robot should be holding
    #         print(f" Captured boxes: {regroup}")
    #         # go back a little 
    #         drive(-20, 3)









         
        dist, rot_y, code = find_token(search)
        # if no token code in regroup choose closes one
        print(f"This is the distance {dist}")

        if not regroup:
            regroup.append(code)

        if dist == -1:
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
            if regroup:
                if R.grab():        
                    print("gotcha")
                    for token in R.see():
                        if token.dist <= d_th:
                            regroup.append(code)
                    search = False
                else:
                    print("my hands are too small")
                    drive(-20,1)
            else:
                R.release()
                regroup = True
                drive(-20,1)



    #         print("I am able to reach the box")
    #         # time.sleep(0.5)
    #         # Here when I grab i append the code to the regroup array and make search false so that the next loop starts
    #         if R.grab():                
    #             print("gotcha")
    #             regroup.append(code)
    #             search = False
    #             # failed grab error msg and back up to try again
    #         else:
    #             print("my hands are too small")
    #             drive(-20,1)
    #     # the robot is in line with the token
    #     elif -a_th < rot_y < a_th:
    #         print("straight ahead")
    #         drive(30,0.5)
    #     # correcting the angle
    #     elif rot_y < -a_th:
    #         print("lefty")
    #         turn(-2,0.5)
    #     # correcting the angle
    #     elif rot_y > a_th:
    #         print("righty")
    #         turn(+2,0.5)


    # # this is the case when we are searching for the regroupment
    # else:
    #     dist, rot_y, code = find_token()

    #     if dist == -1:
    #         print("I'm lost")
    #         turn(+20,0.5)
    #     # if we are within the threshold then release the object and search becomes true to look for another token
    #     elif dist <= d_th:
    #         R.release()
    #         search = True
    #     # robot in line with token
    #     elif -a_th < rot_y < a_th:
    #         drive(50,0.5)
    #     # adjusting agnle
    #     elif rot_y < -a_th:
    #         print("turn left a little")
    #         turn(-2,0.5)
    #     # adjusting angle
    #     elif rot_y > a_th:
    #         print("righty")
    #         turn(+2,0.5)