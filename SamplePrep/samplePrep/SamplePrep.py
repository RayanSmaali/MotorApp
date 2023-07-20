#interface functions
import kivy
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.widget import Widget
from kivy.lang import Builder
#motor functions
from motorControl import dmcCommand
from motorControl import initMotor
from motorControl import resetMotor
from motorControl import spinMotor
from motorControl import moveMotor
from motorControl import finalMove
#pressure controller functions
import time
from Fluigent.SDK import fgt_init, fgt_close
from Fluigent.SDK import fgt_set_pressure, fgt_get_pressure, fgt_get_pressureRange
#temperature control fuctions
from MCP3008 import MCP3008
adc = MCP3008()
resistance = 0
global delay  
delay = 100

initMotor()


#this function reads the adc for temperature and modifies the global variable 

        

class HomeScreen(Screen):
        def __init__(self, **kwargs):
                super(HomeScreen, self).__init__(**kwargs)
                layout = GridLayout(rows = 4,padding = 75)

                #sub-layout that contains buttons used for navigation
                buttonLayout = GridLayout(cols=2,spacing = 500,size_hint = (1,0.5))
                button1 = Button(text="debug", on_release=self.toDebug)
                button2 = Button(text="next", on_release=self.toTemperature)

                buttonLayout.add_widget(button1)
                buttonLayout.add_widget(button2)

                #labels
                title = Label(text='Welcome to the sample preparation program', size_hint = (0.2,0.2))
                text = Label(text = "press next to start preparation, or debug to test the instruments indivudually")
                
                #add every sub-layout to the global layout
                layout.add_widget(title)
                layout.add_widget(text)
                layout.add_widget(Label())
                layout.add_widget(buttonLayout)

                #add global layout to the screen
                self.add_widget(layout)

        #called when the debug button is pressed    
        def toTemperature(self, *args):
                app = App.get_running_app()
                app.root.current = 'temperature'
        def toDebug(self, *args):
                app = App.get_running_app()
                app.root.current = 'debug'
                #init pressures controllers
                fgt_init()
                fgt_set_pressure(0,0)


class DebugScreen(Screen):
        sens = -1
        
        def __init__(self, **kwargs):
                super(DebugScreen, self).__init__(**kwargs)
                layout = GridLayout(rows = 4,padding = 75)

                #sub-layout containing a button to test the motor
                direction = 1
                motorLayout = GridLayout(cols=2)
                motorLabel = Label(text="motor")
                motorButton = Button(text="move",on_release=self.motorTest)     
                
                motorLayout.add_widget(motorLabel)
                motorLayout.add_widget(motorButton)

                #sub-layout containing a slider to test the pressure controller
                pressureLayout = GridLayout(cols=2)
                pressureLabel = Label(text = "pressure controller")
                pressureSlider = Slider(min=0, max=1000,value = 0,value_track = True, on_touch_up=self.pressureTest)     
                self.ids["pressureSlider"] = pressureSlider
                pressureLayout.add_widget(pressureLabel)
                pressureLayout.add_widget(pressureSlider)

                #sub-layout that contains buttons used for navigation
                buttonLayout = GridLayout(cols=2,spacing = 500,size_hint = (1,0.5))
                label = Label()
                button = Button(text="home", on_release=self.toHome)        
                buttonLayout.add_widget(label)
                buttonLayout.add_widget(button)
                
                #add every sub-layout to the global layout
                layout.add_widget(motorLayout)
                layout.add_widget(pressureLayout)
                layout.add_widget(Label())
                layout.add_widget(buttonLayout)
                
                #add global layout to the screen
                self.add_widget(layout)
               
                

        def toHome(self, *args):
                app = App.get_running_app()
                app.root.current = 'homescreen'
        def pressureTest(self,*args):
                print("setting pressure to " + str(int(self.ids['pressureSlider'].value)))
                fgt_set_pressure(1,int(self.ids['pressureSlider'].value))
        def motorTest(self, *args):
                spinMotor(self.sens)
                self.sens = self.sens * -1
                time.sleep(1)
                
class TemperatureScreen(Screen):

        
        def __init__(self, **kwargs):
                super(TemperatureScreen, self).__init__(**kwargs)
                
                layout = GridLayout(rows = 4,padding = 75)

                #sub-layout that contains buttons used for navigation
                buttonLayout = GridLayout(cols=2,spacing = 500,size_hint = (1,0.5))
                button1 = Button(text="Home", on_release=self.toHome)
                button2 = Button(text="Spray", on_release=self.toSpray)

                buttonLayout.add_widget(button1)
                buttonLayout.add_widget(button2)

                #labels
                title = Label(text='temperature control')
                text = Label(text = "be sure the conductive paste is well applied. temperature should be -186°C.")
                temperature = Label(text =  "temperature : not yet implemented")
                self.ids["temperature"] = temperature
                
                
                #add every sub-layout to the global layout
                layout.add_widget(title)
                layout.add_widget(text)
                layout.add_widget(temperature)
                layout.add_widget(buttonLayout)

                #add global layout to the screen
                self.add_widget(layout)
                
                #this will update the temperature detected every .5 seconds
                Clock.schedule_interval(self.updateTemperature,0.5)

        #called when the debug button is pressed    
        def toSpray(self, *args):
                app = App.get_running_app()
                app.root.current = 'spray'
        def toHome(self, *args):
                app = App.get_running_app()
                app.root.current = 'homescreen'
        def updateTemperature(self,dt) : 
                app = App.get_running_app()
                if app.root.current == 'temperature':
                        adc = MCP3008()
                        #R1 est a spécifié ici
                        R1 = 100.4                       
                        valeur = adc.read( channel = 0 ) # Vous pouvez bien entendu adapter le canal à lire
                        valeur = valeur / 1023.0 * 3.3
                        gain = valeur/3.3
                        print("\nTension appliquée : %.2f" % (valeur) )
                        print("par consequent, la résistance est d'environ : %.3f" %((gain*R1)/(1-gain)))
                        global resistance
                        resistance = ((gain*R1)/(1-gain))
                        self.ids["temperature"].text = str(resistance)

class SprayScreen(Screen):
        def __init__(self, **kwargs):
                super(SprayScreen, self).__init__(**kwargs)
                layout = GridLayout(rows = 4,padding = 75)

                #sub-layout that contains buttons used for navigation
                buttonLayout = GridLayout(cols=2,spacing = 500,size_hint = (1,0.5))
                button1 = Button(text="Temperature", on_release=self.toTemperature)
                button2 = Button(text="launch", on_release=self.tolaunch)

                buttonLayout.add_widget(button1)
                buttonLayout.add_widget(button2)

                #sub-layout that contains buttons used motor placement
                motorLayout = GridLayout(cols=2)
                button3 = Button(text="-",on_release = self.motorPlacementF )
                button4 = Button(text="+",on_release = self.motorPlacementB )

                motorLayout.add_widget(button3)
                motorLayout.add_widget(button4)

                #labels
                title = Label(text='The spraying of the sample will soon begin')
                text = Label(text = "Place a used grid in front of it using the buttons on the screen and the adjustment wheel on the right of the device")                
                
                #add every sub-layout to the global layout
                layout.add_widget(title)
                layout.add_widget(text)
                layout.add_widget(motorLayout)
                layout.add_widget(buttonLayout)

                #add global layout to the screen
                self.add_widget(layout)
                
                
                Clock.schedule_interval(self.updatePressure,0.5)
                

        #called when the debug button is pressed    
        def tolaunch(self, *args):
                fgt_set_pressure(1,0)
                fgt_set_pressure(0,0)
                app = App.get_running_app()
                app.root.current = 'launch'
        def toTemperature(self, *args):
                fgt_set_pressure(1,0)
                fgt_set_pressure(0,0)
                app = App.get_running_app()
                app.root.current = 'temperature'
        def motorPlacementF(self,*args):
                moveMotor(1)
        def motorPlacementB(self,*args):
                moveMotor(-1)
        def updatePressure(self,*args):
                app = App.get_running_app()
                if app.root.current == 'spray':
                        fgt_set_pressure(1,1000)
                        fgt_set_pressure(0,1000)


                
                

                
class LaunchScreen(Screen):
        def __init__(self, **kwargs):
                super(LaunchScreen, self).__init__(**kwargs)
                layout = GridLayout(rows = 4,padding = 75)
                

                #sub-layout that contains buttons used for navigation
                buttonLayout = GridLayout(cols=2,spacing = 500,size_hint = (1,0.5))
                button1 = Button(text="spray", on_release=self.toSpray)
                button2 = Button(text="launch", on_release=self.launch)
                

                buttonLayout.add_widget(button1)
                buttonLayout.add_widget(button2)

                #sub-layout that contains buttons used for delay control
                delayLayout = GridLayout(cols=4)
                button3 = Button(text="-",on_release= self.delayMinus)
                button4 = Button(text="+",on_release= self.delayPlus)
                button5 = Button(text="- -",on_release= self.delayMinusMinus)
                button6 = Button(text="++",on_release= self.delayPlusPlus)

                delayLayout.add_widget(button5)
                delayLayout.add_widget(button3)
                delayLayout.add_widget(button4)
                delayLayout.add_widget(button6)

                #labels
                title = Label(text='replace the used grid with a new one\ninput to desired delay and press launch.')
                delayLabel = Label(text = "100 ms")     
                self.ids["delayLabel"] = delayLabel           
                
                #add every sub-layout to the global layout
                layout.add_widget(title)
                layout.add_widget(delayLabel)
                layout.add_widget(delayLayout)
                layout.add_widget(buttonLayout)

                #add global layout to the screen
                self.add_widget(layout)
                #Clock.schedule_interval(self.updateSpeed,0.5)

        #called when the debug button is pressed    
        def toSpray(self, *args):
                app = App.get_running_app()
                app.root.current = 'spray'
        def launch(self, *args):
                fgt_set_pressure(1,1000)
                fgt_set_pressure(0,1000)
                time.sleep(delay*0.001)
                finalMove()
        def delayPlus(self, *args) : 
                global delay
                delay = delay + 10
                self.ids["delayLabel"].text = str(delay) + ' ms'
        def delayPlusPlus(self, *args) : 
                global delay
                delay = delay + 100
                self.ids["delayLabel"].text = str(delay) + ' ms'
        def delayMinus(self, *args) : 
                global delay
                delay = delay - 10
                self.ids["delayLabel"].text = str(delay) + ' ms'
        def delayMinusMinus(self, *args) : 
                global delay
                delay = delay - 100
                self.ids["delayLabel"].text = str(delay) + ' ms'
        

                



class MyApp(App):
        
        def build(self):
                # create a ScreenManager
                sm = ScreenManager()

                # add all screens to the ScreenManager
                home = HomeScreen(name='homescreen')
                debug = DebugScreen(name='debug')
                temperature = TemperatureScreen(name='temperature')
                spray = SprayScreen(name='spray')
                launch = LaunchScreen(name='launch')
                sm.add_widget(home)
                sm.add_widget(debug)
                sm.add_widget(temperature)
                sm.add_widget(spray)
                sm.add_widget(launch)

                return sm

if __name__ == '__main__':
        MyApp().run()
