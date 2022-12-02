import gclib
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang import Builder

Builder.load_file("motorApp.kv")

g = gclib.py()
g.GOpen('192.168.1.222')
g.GCommand("MO")
g.GCommand("BA A")
g.GCommand("BMA = 2000")
g.GCommand("BXA=-3")
g.GCommand("SH")
g.GCommand("SP4000")
g.GCommand("PR-4000")
print(g.GInfo())

class motorApp(Widget):
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
	def coolMoves(self):
		print("izi")
		
		self.sens = self.sens*-1
		self.dmcCommand("PR" + str(4000*self.sens))
		self.dmcCommand("BGA")
		
		
		
class LanguageLearnerApp(App):
    def build(self):
        return GameScreen()   
        

if __name__ == '__main__':
    LanguageLearnerApp().run()

