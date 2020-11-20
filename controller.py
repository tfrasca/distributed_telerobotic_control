import serial
import time
from pubnub import pubnub
from threading import Thread
import pubnub_config

COMPORT = "/dev/ttyUSB0"
BAUDRATE = 9600
JOINT = "j0"
joint_angle = 0
mode = 0

should_read_serial = True
angle_delta_threshold = 10

def process_serial():
  global joint_angle, mode
  ser = serial.Serial(port=COMPORT, baudrate=BAUDRATE)
  while should_read_serial:
    line = ser.readline().decode().strip()
    vals = line.split(" ")
    #print(vals)
    if vals[0] == "j":
      joint_angle = int(vals[1])
    elif vals[0] =="m":
      mode = int(vals[1])
      #print(mode)
  ser.close()

ts = Thread(target=process_serial)
ts.start()

def publisher_callback(envelope, status):
  if status.is_error():
    print("error", status.status_code)


try:
  uuid = "tmfrasca"
  pn = pubnub_config.config(uuid)
  old_joint_angle = 0
  old_mode = 0
  while True:
    print (old_mode, mode)
    if old_mode != mode:
      pn.publish().channel("mode").message(mode).pn_async(publisher_callback)
      old_mode = mode
    if old_mode == 1:
      if abs(joint_angle - old_joint_angle) > angle_delta_threshold:
        pn.publish().channel(JOINT).message(joint_angle).pn_async(publisher_callback)
        old_joint_angle = joint_angle
    time.sleep(1)

except (KeyboardInterrupt):
  should_read_serial = False
