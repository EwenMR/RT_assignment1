Python Robotics Simulator Assignment 1
================================

This is the finished proposed assignment continuing in class exercises of a python robotics simulator. The objective of the robot is to regroup all the golden boxes in one same are.

The work done here is by Ewen Gay-Semenkoff

Installing and running
----------------------

To run this code, python3 must be installed alongside some libraries (pygame, PyPyBoxd2D, time, PyYAML). Once all the libraries have been installed you will need to clone this github repository and move to the correct pathway using the commands below:

```bash
$ git clone https://github.com/EwenMR/RT_assignment1.git
```
We then move to the robot-sim folder:

```bash
$ cd RT_assignment1
$ cd robot-sim
```
And we can run the code using:

```bash
$ python3 run.py assignment.py
```

If done succesfully this should open a little window of a robot simulator that will gather all tokens together.

## Functions

### 'drive(speed, seconds)'

- Start and stop the motors for the specified duration.
- Args:
  - `speed (int)`: Speed of the wheels.
  - `seconds (int)`: Time interval.



```python
def drive(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

```



### 'turn(speed, seconds)'

- Start and stop the motors for the specified duration while turning the robot.
- Args:
  - `speed (int)`: Speed of the wheels.
  - `seconds (int)`: Time interval.




```python
def turn(speed, seconds):
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

```



### 'find_token()'

- Find the closest token that hasn't been picked up yet
- Returns:
  - dist (float): distance of the closest token (-1 if no token is detected)
  - rot_y (float): angle between the robot and the token (-1 if no token is detected)
  - code (int): code number of the token the robot sees (-1 if not token is detected)



```python
def find_token():
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
```



### 'find_regroup()'

- Find the location of the regrouping of tokens (based on the regroup array)
- Returns:
  - rdist (float): distance of the closest token with its code in the regroup array (-1 if no token is detected)
  - rro_ty (float): angle between the robot and a token in the regroup array (-1 if no token is detected)



```python
def find_regroup():
  rdist = 100

    for token in R.see():
        if token.info.code in regroup:
            rdist = token.dist 
            rrot_y = token.rot_y

    if rdist == 100:
        return -1,-1
    else:
        return rdist, rrot_y
```




#### 'first_time()'

- List of code to execute when grabbing the first token. It will allow us to use the first box to be the regrouping point without moving it far.



```python
def first_time():
  turn(60,1)
    R.release()
    drive(-30,1)
    print("released")
    regroup.append(code)
```




## Main program

- Initialises an array to keep track of all the tokens that have been regrouped.
- Initialises 'search' to true and 'first' to 1.
- Initialises 'x' to 6 which is the number of tokens.
- The main while loop executes a loop that will make the robot drive to the closest token to get picked up if search is true. If it is the first token being picked up turn around and release it to serve as regrouping point. If token successfully grabbed make 'search' equal to false.
- This executes the second part of the loop that will go to the token(s) that are found in the regroup array to release the token close to them. Upon release it appends the token's code to the regroup array and resumes the process until all tokens have been regrouped.


![Flowchart](https://github.com/EwenMR/RT_assignment1/RT_assignment_flowchart.png)

--------------------------------

Robot API
---------

The API for controlling a simulated robot is designed to be as similar as possible to the [SR API][sr-api].

### Motors ###

The simulated robot has two motors configured for skid steering, connected to a two-output [Motor Board](https://studentrobotics.org/docs/kit/motor_board). The left motor is connected to output `0` and the right motor to output `1`.

The Motor Board API is identical to [that of the SR API](https://studentrobotics.org/docs/programming/sr/motors/), except that motor boards cannot be addressed by serial number. So, to turn on the spot at one quarter of full power, one might write the following:

```python
R.motors[0].m0.power = 25
R.motors[0].m1.power = -25
```

### The Grabber ###

The robot is equipped with a grabber, capable of picking up a token which is in front of the robot and within 0.4 metres of the robot's centre. To pick up a token, call the `R.grab` method:

```python
success = R.grab()
```

The `R.grab` function returns `True` if a token was successfully picked up, or `False` otherwise. If the robot is already holding a token, it will throw an `AlreadyHoldingSomethingException`.

To drop the token, call the `R.release` method.

Cable-tie flails are not implemented.

### Vision ###

To help the robot find tokens and navigate, each token has markers stuck to it, as does each wall. The `R.see` method returns a list of all the markers the robot can see, as `Marker` objects. The robot can only see markers which it is facing towards.

Each `Marker` object has the following attributes:

* `info`: a `MarkerInfo` object describing the marker itself. Has the following attributes:
  * `code`: the numeric code of the marker.
  * `marker_type`: the type of object the marker is attached to (either `MARKER_TOKEN_GOLD`, `MARKER_TOKEN_SILVER` or `MARKER_ARENA`).
  * `offset`: offset of the numeric code of the marker from the lowest numbered marker of its type. For example, token number 3 has the code 43, but offset 3.
  * `size`: the size that the marker would be in the real game, for compatibility with the SR API.
* `centre`: the location of the marker in polar coordinates, as a `PolarCoord` object. Has the following attributes:
  * `length`: the distance from the centre of the robot to the object (in metres).
  * `rot_y`: rotation about the Y axis in degrees.
* `dist`: an alias for `centre.length`
* `res`: the value of the `res` parameter of `R.see`, for compatibility with the SR API.
* `rot_y`: an alias for `centre.rot_y`
* `timestamp`: the time at which the marker was seen (when `R.see` was called).

For example, the following code lists all of the markers the robot can see:

```python
markers = R.see()
print "I can see", len(markers), "markers:"

for m in markers:
    if m.info.marker_type in (MARKER_TOKEN_GOLD, MARKER_TOKEN_SILVER):
        print " - Token {0} is {1} metres away".format( m.info.offset, m.dist )
    elif m.info.marker_type == MARKER_ARENA:
        print " - Arena marker {0} is {1} metres away".format( m.info.offset, m.dist )
```

[sr-api]: https://studentrobotics.org/docs/programming/sr/


## Future Work

In general this code can be built on in many different sectors.

- Additional functions could be made to increase clarity in the main program.
- A faster route to new tokens could be made using different values for the speeds and times when driving and turning.
- A path planner could be added as to optimise the time of completion.
- When there is a larger gorup of tokens, sometimes the robot pushes the boxes before releasing, perhaps finding a better way to create a regrouping point could be researched.