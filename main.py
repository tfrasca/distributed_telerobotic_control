import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import  TextInput
from kivy.uix.button import Button

class MyGrid(GridLayout):
    def __init__(self, **kwargs):
        super(MyGrid, self).__init__(**kwargs)
        self.cols = 2
    
        
        self.add_widget(Label(text="X-Coordinate: "))
        self.xvar = TextInput(multiline=False)
        self.add_widget(self.xvar)

        self.add_widget(Label(text="Y-Coordinate: "))
        self.yvar = TextInput(multiline=False)
        self.add_widget(self.yvar)
        
        self.add_widget(Label(text="Z-Coordinate:"))
        self.zvar = TextInput(multiline=False)
        self.add_widget(self.zvar)
        
        self.add_widget(self.inside)
        self.submit = Button(text="Submit", font_size=25)
        self.add_widget(self.submit)
    

class MyTextInput(TextInput):
    def on_enter(instance, value):
        print('User pressed enter in', instance)
    
    textinput = TextInput(text='Hello world', multiline=False)
    textinput.bind(on_text_validate=on_enter)
    pass
    
    
class MyApp(App): # <- Main Class
    def build(self):
        return MyGrid()

window = MyApp()
window.run()