import threading
import time
from environnement import *

def AddBotToEnv(env,V):
	for bot,param in V.items():
		# add here if new class are created
		if bot == "mirai0":
			Mirai=MiraiBot0(0)
			env.AddNewBot(Mirai,param[1])
		if bot == "mirai1":
			Mirai=MiraiBot1(0)
			env.AddNewBot(Mirai,param[1])
		if bot == "mirai2":
			Mirai=MiraiBot2(0)
			env.AddNewBot(Mirai,param[1])
		if bot == "mirai3":
			Mirai=MiraiBot3(0)
			env.AddNewBot(Mirai,param[1])
		if bot == "mirai4":
			Mirai=MiraiBot4(0)
			env.AddNewBot(Mirai,param[1])
		if bot == "mirai5":
			Mirai=MiraiBot5(0)
			env.AddNewBot(Mirai,param[1])
		if bot == "psybot0":
			Psybot=PsyBot0(0)
			env.AddNewBot(Psybot,param[1])
		if bot == "psybot1":
			Psybot=PsyBot1(0)
			env.AddNewBot(Psybot,param[1])
		if bot == "psybot2":
			Psybot=PsyBot2(0)
			env.AddNewBot(Psybot,param[1])

class SimulThread(threading.Thread):
	def __init__(self, ThreadID,Delay,Simul,V,T,Time,Step, exposant, seuil, protection, vul):
		threading.Thread.__init__(self)
		self.ThreadID = ThreadID
		self.Delay = Delay
		self.Simul = Simul
		self.V = V.copy()
		self.T = T
		self.Time = Time
		self.Step = Step 
		self.exposant = exposant
		self.seuil = seuil
		self.protection = protection
		self.vulnerabilites = vul
	
	def run(self):
		for i in range(self.Simul):
			env=Environnement(self.V,self.T,self.Time,self.Step,150,200,self.exposant,self.seuil,self.protection,self.vulnerabilites)
			
			env.GenVictimes()  
   
			AddBotToEnv(env,self.V)
			env.Game()
			env.Recup_CSV('a',self.ThreadID)
			del env
			time.sleep(self.Delay)