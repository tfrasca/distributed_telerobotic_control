# distributed_telerobotic_control
This project works towards developing a distributed human-machine interface for telerobotic control.
We are using arduinos as the input controllers and the robot controller.

## Requirements:
Install Arduino >= 1.8.13

python >= 3.8.5

pubnub >= 4.6.1

## Note:
add pub nub keys to pubnub_keys.py

either move or link the Arudino code directories to the Arduino library directory

modify COMPORT in controller.py and robot_controller.py

## Run:
upload Arduino code to hardware

### User Control
`python controller.py`

### Robot Controller
`python robot_controller.py`
