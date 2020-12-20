# distributed_telerobotic_control
This project works towards developing a distributed human-machine interface for telerobotic control.
We are using arduinos as the input controllers and an Arbotix microcontroller to
control the physical robot.
The servo motors we are using are Dynamixel AX-12As, however other motors can be
used, but RobotControl.ino  will need to be modified to handle the different motors.

## Requirements (What we used, other versions might work):
Install Arduino IDE >= 1.8.x

python >= 3.8.5

pubnub >= 4.6.1

pyserial >= 3.5

pygame >= 2.0.0

kivy >= 2.0.0

Dynamixel Hardware and Arbotix microcontroller set up for Arduino 
* `git clone https://github.com/Interbotix/arbotix/tree/arduino-1-6`

* Follow instructions at https://learn.trossenrobotics.com/projects/182-arbotix-getting-started-guide-arduino-ide-1-6-x-setup.html
  * Note: I'm using Arduino IDE 1.8.x instead of 1.6.x and it seems to work
  * Note: use the hardware and libraries directories from cloned repo in prior step

## Run:
### Notes:
Add pub nub keys to pubnub_keys.py

Either move or link the PotButton and RobotControl directories to the Arduino directory (not the IDE directory)

### Arduino
Connect a button to the Arduino digital pin 2 which can act as an interupt pin.
If you are using a different Arduino which has a different interrupt pin, then you will need to change the code accordingly.
Connect a potentiometer to digital pin 0 and upload the PotButton code to the Arduino. 
For the robot controller, upload the RobotControl sketch to the Arbotix or other microcontroller connected to the servo motors.

### User Control
Modify COMPORT in controller.py, future updates can probably have a drop down in the GUI.

`python controller.py`

The system starts in mode 0, which has no control. Click the button once to put it into joint-angle mode.
Then use the potentiometer to control the associated joint. If you want to control a different joint, you will need to change JOINT in hardware_interface.py.
Pressing the button again will allow you to input x,y,w values using the GUI.
Another press will switch to autonomous mode, which currently is under development.
One more press will cycle back to joint-angle mode.

### Robot Controller
Modify COMPORT in robot_controller.py

`python robot_controller.py`
