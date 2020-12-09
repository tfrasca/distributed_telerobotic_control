from pubnub import pubnub
from pubnub.pubnub import SubscribeCallback
import pubnub_config 
import math
import time
import signal
from threading import Thread
import sys
import serial

uuid = "tmfrasca"
COMPORT = "/dev/ttyUSB0"
BAUDRATE = 9600

class Listener(SubscribeCallback):
  def __init__(self, robot_controller):
    super().__init__()
    self.robot_controller = robot_controller
    self.joints = self.robot_controller.get_joints()

  def message(self, pn, message):
    if message.channel == "mode":
      self.robot_controller.set_mode(message.message)
    elif message.channel in self.joints:
      self.robot_controller.set_joint(message.channel, message.message)
    elif message.channel == "ee_position":
      self.robot_controller.set_ee_position(message.message)

class RobotController():
  def __init__(self):
    self.joints={"j0":0, "j1":0, "j2":0}
    self.mode = 0
    self.should_run = True
    self.move = False
    # commented for testing with only one device
    #try:
    #  self.ser = serial.Serial(COMPORT, baudrate=BAUDRATE)
    #except (FileNotFoundError, serial.SerialException):
    #  print("device not found at", COMPORT)

  def set_mode(self, mode):
    self.mode = mode

  def set_joint(self, joint, value):
    print("setting ", joint, value)
    self.joints[joint] = value
    self.move = True

  def set_ee_position(self, position):
    if self.mode == 2:
      print("moving end effector to position", position)
      self.ee_position = position

  def get_joints(self):
    return self.joints.keys()

  def terminate_execution(self):
    self.should_run = False

  def send_joint_angles(self):
    message = ""
    for key in self.joints:
      message += key
      message += " "
      message += str(self.joints[key])
      message += " "
    print(message)
    #self.ser.write

  # position should be triple (x,y,z)
  # instead, we want to use a position input of (x,y,theta) where theta is in degrees
  # now, the user will input x, y, and theta rather than x,y,z
  # for now, the lengths of the linkages are defined in the function
  def calculate_inverse_kinematics(self, position):
    # See Figure 3 in: https://www.researchgate.net/publication/328583527_A_Geometric_Approach_to_Inverse_Kinematics_of_a_3_DOF_Robotic_Arm
    # interpret j0 as a joint with rotation around an axis orthogonal to the surface (shoulder for a human)
    # j1 as the first joint (elbow for a human)
    # j2 as the second joint (wrist for human )
  
    # Linkage lengths are not defined, feel free to change them here
    L1 = 10
    L2 = 10
  
    # Calculated X,Y distance
    dist = math.sqrt(position[0] * position[0] + position[1] * position[1])
  
    # Check if point is out of reach
    if dist > L1 + L2:
      print("Error: point out of reach!")
      return
  
    # Calculate angle
    alpha = math.atan2(position[1], position[0])
  
    # cos phi 1
    cos_phi_1 = ((L1 * L1) + (dist * dist) - (L2 * L2)) / (2 * L1 * dist)
    phi_1 = math.acos(cos_phi_1)
  
    # theta 1
    theta1 = alpha - phi_1
  
    # cos phi 2
    cos_phi_2 = ((L1 * L1) + (L2 * L2) - (dist * dist)) / (2 * L1 * L2)
    phi_2 = math.acos(cos_phi_2)
  
    # theta 2
    theta2 = math.pi - phi_2
  
    # Change to degrees
    theta1 = theta1 * (180 / math.pi)
    theta2 = theta2 * (180 / math.pi)
    theta = position[2]
  
    # Change joint angles
    self.joints = (theta, theta1, theta2)
    pass

  def run(self):
    while self.should_run:
      if self.mode == 1 or self.mode == 2: # user control either joint or end effector position
        if self.move:
          if self.mode == 2:
            self.calculate_inverse_kinematics(self.ee_position)
          print("moving")
          self.send_joint_angles()
          self.move = False
      if self.mode == 3: # fully autonomous
        pass

def handle_signal(signal,frame):
  rc.terminate_execution()
  pn.remove_listener(listener) # something isn't working properly when trying to exit
  sys.exit()
  

if __name__ == "__main__":
  pn = pubnub_config.config(uuid)
  rc = RobotController()
  listener = Listener(rc)
  pn.add_listener(listener)
  pn.subscribe().channels(["j0","j1","j2","ee_position","mode"]).execute()
  t1 = Thread(target=rc.run)
  t1.start()
  signal.signal(signal.SIGINT, handle_signal)
