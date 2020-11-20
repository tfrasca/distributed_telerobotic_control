from pubnub import pubnub
from pubnub.pubnub import SubscribeCallback
import pubnub_config 
import time

uuid = "tmfrasca"

class Listener(SubscribeCallback):
  def __init__(self, kwargs=None):
    super().__init__()
    self.mode = 0
  def message(self, pn, message):
    if message.channel == "mode":
      self.mode = message.message
      #print("new mode", self.mode)
    if self.mode == 1:
      print(message.channel, message.message)

class RobotController():
  def set_joints(self):
    print("setting joints")

  
try:
  pn = pubnub_config.config(uuid)
  rc = RobotController()
  listener = Listener(rc)
  pn.add_listener(listener)
  pn.subscribe().channels(["j0","mode"]).execute()
except (KeyboardInterrupt):
  pass
