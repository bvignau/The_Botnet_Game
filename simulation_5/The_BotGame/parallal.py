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
        if bot == "psybot":
            Psybot=PsyBot(0)
            env.AddNewBot(Psybot,param[1])

class SimulThread(threading.Thread):
    def __init__(self, ThreadID,Delay,Simul,V,T,Time,Step,ensemble):
        threading.Thread.__init__(self)
        self.ThreadID = ThreadID
        self.Delay = Delay
        self.Simul = Simul
        self.V = V.copy()
        self.T = T
        self.Time = Time
        self.Step = Step
        self.Ensemble=ensemble
    
    def run(self):
        for i in range(self.Simul):
            env=Environnement(self.V,self.T,self.Time,self.Step,150,200)
            if self.Ensemble == 0:
                env.GenVictimesRandom()
            else :
                env.GenVictimesEnsemble()
            AddBotToEnv(env,self.V)
            env.Game()
            env.Recup_CSV('a',self.ThreadID)
            del env
            time.sleep(self.Delay)