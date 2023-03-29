#motor control libraries
import gclib
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
#pressure control libraries
import time
from Fluigent.SDK import fgt_init, fgt_close
from Fluigent.SDK import fgt_set_pressure, fgt_get_pressure, fgt_get_pressureRange

Builder.load_file("motorApp.kv")

g = gclib.py()
sm = ScreenManager()

# here we define all the screens used in the app	
class LanguageLearnerApp(App):
	def build(self):
		sm = ScreenManager()
		sm.add_widget(testScreen(name='test'))
		sm.add_widget(prepScreen(name='preparation'))
		sm.add_widget(launchScreen(name='launch'))
		sm.add_widget(fluidScreen(name='fluid'))
		return sm   

#initiate all the different screens

class testScreen(Screen):
	sens = 1	
#This function will perform error trapping on any GCommand calls. 
#It is intended to capture any gclib errors and report the message to the title bar 
	def dmcCommand(self, cmd):
		try: 
			print("sent cmd : " + cmd) 
			rc = g.GCommand(cmd)#Send command into the GCommand gclib API 
		except Exception as e: 
			print (e) 
			tc1 = g.GCommand('TC1') 
			print (tc1) 
			
	def reset(self): self.dmcCommand("RS")
		
	def init(self):
		#opens ethernet communication
		g.GOpen('192.168.1.222')
		#inititate motor
		self.dmcCommand("MO")
		self.dmcCommand("BA A")
		self.dmcCommand("BMA = 2000")
		self.dmcCommand("BXA=-3")
		self.dmcCommand("SH")
		
		#programs a relative movement (PR : Position Relative)
		#it will be done at the desired speed (SP)
		self.dmcCommand("SP4000")
		self.dmcCommand("PR4000")
		print(g.GInfo())

        #called when pressing the spin button
        #begins the movement that was pre-programmed
	def spinMotor(self):		
		self.sens = self.sens*-1
		self.dmcCommand("PR" + str(4000*self.sens))
		self.dmcCommand("BGA")
	
	pass
class prepScreen(Screen):
	pass
class launchScreen(Screen):
	pass
#this screen simply transfers the slider value to the pressure controller
class fluidScreen(Screen):
	fgt_init()
	fgt_set_pressure(0,0)
	def setPressure(self):
		print("setting pressure to " + str(int(self.ids['pressureSlider'].value)))
		fgt_set_pressure(0,int(self.ids['pressureSlider'].value))
	def exitFct(self):
		fgt_set_pressure(0, 0)
		fgt_close()
        

if __name__ == '__main__':
    LanguageLearnerApp().run()

