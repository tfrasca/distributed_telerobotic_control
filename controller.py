from gui import ControllerApp
from hardware_interface import HardwareController
import pubnub_config

if __name__ == "__main__":
    uuid = "tmfrasca"
    pn = pubnub_config.config(uuid)
    hardware_controller = HardwareController(pn)
    hardware_controller.run()
    gui_controller = ControllerApp(pn).run()
