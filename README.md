# distributed_telerobotic_control
This project works towards developing a distributed human-machine interface for telerobotic control.
We are using arduinos as the input controllers and an Arbotix microcontroller to
control the physical robot.
The servo motors we are using are Dynamixel AX-12As, however other motors can be
used, but RobotControl.ino  will need to be modified to handle the different motors.

## Requirements:
Install Arduino IDE >= 1.8.x

python >= 3.8.5

pubnub >= 4.6.1

Dynamixel Hardware and Arbotix microcontroller set up for Arduino 
* `git clone https://github.com/Interbotix/arbotix/tree/arduino-1-6`

* follwow instructions at https://learn.trossenrobotics.com/projects/182-arbotix-getting-started-guide-arduino-ide-1-6-x-setup.html
  * Note: I'm using Arduino IDE 1.8.x instead of 1.6.x and it seems to work
  * Note: use the hardware and libraries directories from cloned repo in prior step


## Additional Notes:
add pub nub keys to pubnub_keys.py

either move or link the PotButton and RobotControl directories to the Arduino directory (not the IDE directory)

modify COMPORT in controller.py and robot_controller.py

## Run:
upload Arduino code to hardware

### User Control
`python controller.py`

### Robot Controller
`python robot_controller.py`
