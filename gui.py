from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
#from controller import HardwareController
import pubnub_config


class Controller(GridLayout):
    def submitCoordinates(self):
        try:
            coordinate = (float(self.ids.x.text), float(self.ids.y.text), float(self.ids.w.text))
            print (coordinate)
            pub_nub = App.get_running_app().pub_nub
            pub_nub.publish().channel("ee_position").message(coordinate).pn_async(self.publisher_callback)
        except ValueError:
            print("value must be a number")

    def publisher_callback(self, envelope, status):
        if status.is_error():
            print("error", status.status_code)



class ControllerApp(App):
    def __init__(self, pub_nub):
        super(ControllerApp, self).__init__()
        self.pub_nub = pub_nub

    def build(self):
        self.load_kv(filename="gui.kv")



if __name__ == "__main__":
    uuid = "tmfrasca"
    pn = pubnub_config.config(uuid)
    ControllerApp(None).run()
