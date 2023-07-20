import gclib
g = gclib.py()

#This function will perform error trapping on any GCommand calls. 
#It is intended to capture any gclib errors and report the message to the title bar 
def dmcCommand(cmd):
	try: 
		print("sent cmd : " + cmd) 
		rc = g.GCommand(cmd)#Send command into the GCommand gclib API 
	except Exception as e: 
		print (e) 
		tc1 = g.GCommand('TC1') 
		print (tc1) 
def resetMotor(): dmcCommand("RS")
		
def initMotor():
	#opens ethernet communication
	g.GOpen('192.168.1.222')
	#inititate motor
	dmcCommand("MO")
	dmcCommand("BA A")
	dmcCommand("BMA = 2000")
	dmcCommand("BXA=-3")
	dmcCommand("SH")
	
	
	#programs an movement (PR : Position absolute)
	#it will be done at the desired speed (SP) and acceleration (AC)
	dmcCommand("SP4000")
	#dmcCommand("AC20000")
	dmcCommand("PA-1000")
	dmcCommand("BGA")
	print(g.GInfo())

#called when pressing the spin button
#begins the movement that was pre-programmed
def spinMotor(sens):		
	
	dmcCommand("PR" + str(4000*sens))
	dmcCommand("AMA")
	dmcCommand("BGA")
def moveMotor(sens):
	dmcCommand("PR" + str(25*sens))
	dmcCommand("AMA")
	dmcCommand("BGA")
def finalMove():
	dmcCommand("SP9999")
	dmcCommand("PA" + str(-2000))
	dmcCommand("AMA")
	dmcCommand("BGA")

