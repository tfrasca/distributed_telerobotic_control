from gui import ControllerApp
from hardware_interface import Listener, HardwareController
import pubnub_config

if __name__ == "__main__":
    uuid = "tmfrasca"
    pn = pubnub_config.config(uuid)
    hardware_controller = HardwareController(pn)
    listener = Listener(hardware_controller)
    pn.add_listener(listener)
    pn.subscribe().channels(["mode"]).execute()
    hardware_controller.run()
    gui_controller = ControllerApp(pn).run()
