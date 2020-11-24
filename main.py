import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

class MyBoxLayout(BoxLayout):
    pass

class MyApp(App): # <- Main Class
    def build(self):
        return MyBoxLayout()

window = MyApp()
window.run()