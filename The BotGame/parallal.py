import threading
import time
from environnement import *

def AddBotToEnv(env,V):
    for bot,param in V.items():
        if bot == "mirai":
            Mirai=MiraiBot(0)
            env.AddNewBot(Mirai,param[1])
        if bot == "psybot":
            Psybot=PsyBot(0)
            env.AddNewBot(Psybot,param[1])

class SimulThread(threading.Thread):
    def __init__(self, ThreadID,Delay,Simul,V,T,Time,Step):
        threading.Thread.__init__(self)
        self.ThreadID = ThreadID
        self.Delay = Delay
        self.Simul = Simul
        self.V = V.copy()
        self.T = T
        self.Time = Time
        self.Step = Step
    
    def run(self):
        for i in range(self.Simul):
            env=Environnement(self.V,self.T,self.Time,self.Step)
            env.GenVictimes()
            AddBotToEnv(env,self.V)
            env.Game()
            env.Recup_CSV('a',self.ThreadID)
            del env
            time.sleep(self.Delay)