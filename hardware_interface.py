import serial
import time
from pubnub import pubnub
from threading import Thread
import pubnub_config

#COMPORT = "/dev/ttyUSB0"
COMPORT = "COM3"
BAUDRATE = 9600
JOINT = "j0"
joint_angle = 0
mode = 0

should_read_serial = True
angle_delta_threshold = 10


class HardwareController:
    def __init__(self, pub_nub):
        self.pub_nub = pub_nub
        self.should_read_serial = True

    def run(self):
        t1 = Thread(target=self.process_serial)
        t1.start()
        t2 = Thread(target=self.update_pubnub)
        t2.start()

    def update_pubnub(self):
        try:
            old_joint_angle = 0
            old_mode = 0
            while True:
                print (old_mode, mode)
                if old_mode != mode:
                    self.pub_nub.publish().channel("mode").message(mode).pn_async(self.publisher_callback)
                    old_mode = mode
                if old_mode == 1:
                    if abs(joint_angle - old_joint_angle) > angle_delta_threshold:
                        self.pub_nub.publish().channel(JOINT).message(joint_angle).pn_async(self.publisher_callback)
                        old_joint_angle = joint_angle
                time.sleep(1)
        except (KeyboardInterrupt):
            self.should_read_serial = False

    def process_serial(self):
        global joint_angle, mode
        ser = serial.Serial(port=COMPORT, baudrate=BAUDRATE)
        while self.should_read_serial:
            line = ser.readline().decode().strip()
            vals = line.split(" ")
            if vals[0] == "j":
                joint_angle = int(vals[1])
            elif vals[0] == "m":
                mode = int(vals[1])
        ser.close()

    def publisher_callback(self, envelope, status):
        if status.is_error():
            print("error", status.status_code)


if __name__ =="__main__":
    uuid = "tmfrasca"
    pn = pubnub_config.config(uuid)
    controller = HardwareController(pn)
    ts = Thread(target=controller.run())
    ts.start()

