from pubnub import pubnub
from pubnub.pubnub import SubscribeCallback
import pubnub_config
import serial
from threading import Thread
import time

#COMPORT = "/dev/ttyUSB1"
COMPORT = "COM3"
BAUDRATE = 9600
JOINT = "j0"


class Listener(SubscribeCallback):
    def __init__(self, hardware_controller):
        super().__init__()
        self.hardware_controller = hardware_controller

    def message(self, pn, message):
        if message.channel == "mode":
            print("msg",message.message)
            self.hardware_controller.update_mode(message.message)

class HardwareController:
    def __init__(self, pub_nub):
        self.pub_nub = pub_nub
        self.should_read_serial = True
        self.current_mode = 0
        self.joint_angle = 0
        self.old_joint_angle = 0
        self.mode = 0
        self.old_mode = 0
        self.angle_delta_threshold = 5
        self.ser = serial.Serial(port=COMPORT, baudrate=BAUDRATE)

    def run(self):
        t1 = Thread(target=self.process_serial)
        t1.start()
        t2 = Thread(target=self.update_pubnub)
        t2.start()

    def update_pubnub(self):
        try:
            while True:
                #print (self.old_mode, self.mode)
                if self.old_mode != self.mode:
                    self.old_mode = self.mode
                    self.pub_nub.publish().channel("mode").message(self.old_mode).pn_async(self.publisher_callback)
                if self.old_mode == 1:
                    if abs(self.joint_angle - self.old_joint_angle) > self.angle_delta_threshold:
                        self.pub_nub.publish().channel(JOINT).message(self.joint_angle).pn_async(self.publisher_callback)
                        self.old_joint_angle = self.joint_angle
                time.sleep(1)
        except (KeyboardInterrupt):
            self.should_read_serial = False

    def process_serial(self):
        while self.should_read_serial:
            line = self.ser.readline().decode().strip()
            vals = line.split(" ")
            if vals[0] == "j":
                self.joint_angle = int(vals[1])
            elif vals[0] == "m":
                self.mode = int(vals[1])
                #print("Mode c:",self.mode)
            else:
                print(vals)
        self.ser.close()

    def publisher_callback(self, envelope, status):
        if status.is_error():
            print("error", status.status_code)

    def update_mode(self, mode):
        if self.old_mode != mode:
            self.mode = mode
            self.ser.write(str(mode).encode())
            #print("Mode p:", self.mode)

if __name__ =="__main__":
    uuid = "tmfrasca"
    pn = pubnub_config.config(uuid)
    controller = HardwareController(pn)
    listener = Listener(controller)
    pn.add_listener(listener)
    pn.subscribe().channels(["mode"]).execute()
    ts = Thread(target=controller.run())
    ts.start()

