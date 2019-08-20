from Victime import *
from Bot import *
import matplotlib.pyplot as plt
import csv
import numpy as np

COLOR=['b','g','r','c','m','y','k','w']
STYLE=['.','v','<','1','s','p','P','*','D','--']

#TODO => Revoir le système de gestion de la concurence !!
#           => Ordre Randomisé de passage
#           => Supression des infections (Wifatch etc)
#TODO => Tools de visualisation pour X simulations
#TODO => Tool visualisation vicitimes
#       => combien de bots les ont infectés, nombre de bots par victimes, nombre de supression ?
#TODO => Interface de gestion des victimes !!

def GenReplicaVicitme(bot,replicat):
    vuln=[]
    for i in range(replicat):
        vuln.append(bot+' '+str(i))
    #print("Vuln = "+str(vuln))
    return vuln



class Environnement():
    def __init__(self,V,T,TimeMax,step):
        self.V=V.copy()
        self.T = T
        self.TimeMax=TimeMax
        self.Step=step
        self.Victimes = list()
        self.Bots = dict()
        self.res=dict()
    

    # def detectPsybot(self,ip):        # USE TO DEBUG
    #     count=0
    #     for v in self.Victimes:
    #         if 'psybot 0' in v.vulnerables:
    #             #print("Victime vulnérable à psybot")
    #             count+=1
    #             if ip == v.numero:
    #                 print("ip vulnéable à psybot")
    #     print("count = "+str(count))

    def AddNewBot(self, bot, num):
        for i in range(num):
            b = bot.Clone()
            b.Change_Instance(i)
            self.Bots[b.nom]=[]
            self.Bots[b.nom].append(b)

    def GenVictimesEnsemble(self):
        secretsGenerator = secrets.SystemRandom()
        for i in range(self.T):
            v = secretsGenerator.randint(0,self.T)
            victim=Victime(i,[])
            for bot,param in self.V.items():
                #print("bot = "+str(bot))
                #print("param = "+str(param))
                if v <= param[0]:
                    #print("Ajout Victime")
                    victim.AddBot(GenReplicaVicitme(bot,param[1]))
            #print('vuln : '+str(victim.vulnerables))
            self.Victimes.append(victim)
        #print("génération de victimes terminée")

    def GenVictimesRandom(self):
        secretsGenerator = secrets.SystemRandom()
        for i in range(self.T):
            victim=Victime(i,[])
            for bot,param in self.V.items():
                #print("bot = "+str(bot))
                #print("param = "+str(param))
                v = secretsGenerator.randint(0,self.T)
                if v <= param[0]:
                    #print("Ajout Victime")
                    victim.AddBot(GenReplicaVicitme(bot,param[1]))
            #print('vuln : '+str(victim.vulnerables))
            self.Victimes.append(victim)
        #print("génération de victimes terminée")
    
    def BotReplicats(self,bot):
        nom=[]
        for b in bot :
            if b in self.V:
                for i in range(self.V[b][1]):
                    nom.append(b+" "+str(i))
        return nom
    
    def Turn(self):
        # TODO RANDOM ORDRE
        for Botnet in self.Bots :
            for B in self.Bots[Botnet] :
                rep = B.Next(self.T)
                #print("Rep = "+str(rep))
                if rep['IP'] != -1 :
                    #print('Dans vul,rm')
                    supp=self.BotReplicats(rep['supression'])
                    vul,removed=self.Victimes[rep['IP']].vulnerable(rep['nom'],rep['protection'],supp)
                    #print("vul = "+str(vul))
                    #print("removed bis = "+str(removed))
                    if  vul == True :
                        # la victime est vulnérable => on passe le bot en état d'exploit
                        B.ExploitTime()
                        if   len(removed) > 0:    # si la liste n'est pas vide, on doit supprimer un bot
                            for r in removed:
                                #print("avant "+str(len(self.Bots[r])))
                                #print("r = "+str(r))
                                if len(self.Bots[r]) > 1:
                                    del self.Bots[r][0]
                                #print("après "+str(len(self.Bots[r])))
                            pass
                        nBot=B.Clone()
                        nBot.ExploitTime()
                        self.Bots[B.nom].append(nBot) # on ajoute un bot en état d'exploit
                    else :
                        B.Gen_IP(self.T)
                        # la victime n'est pas vulnérable on passe le bot en état de génération IP
    
    def Game(self):
        for i in range(self.TimeMax):
            self.Turn()
            if i%self.Step == 0 :
                self.CountBots()
    
    def CountBots(self):
        for name, Botnet in self.Bots.items():
            if name in self.res :
                self.res[name].append(len(Botnet))
            else :
                self.res[name]=[]
        return self.res

    def StyleLine(self,color,style,c,s):
        stylline=color[c]+style[s]
        if c == len(color):
            c = 0
            if s < len(s):
                s+=1
        else :
            c+=1
        return stylline,c,s
    # TODO
    def Recup_CSV(self, option, thread):
        files=[]
        for Botnet, stats in self.res.items():
            nom=Botnet+"-"+str(thread)+".csv"
            files.append(nom)
            with open(nom, option, newline='\n') as csvfile:
                reswritter = csv.writer(csvfile,delimiter=';',quotechar='"',quoting=csv.QUOTE_MINIMAL)
                if option == 'w':
                    x=np.arange(0,self.TimeMax,self.Step)
                    reswritter.writerow(x)
                reswritter.writerow(stats)
        return files

    def Plot(self):
        plt.axis([0,self.TimeMax,0,self.T])
        color=0
        style=0
        for Botnet, stats in self.res.items():
            x=[]
            y=[]
            i=0
            for b in stats:
                x.append(i*self.Step)
                y.append(b)
                i+=1
            lineStyle,color,style=self.StyleLine(COLOR,STYLE,color,style,)
            # print("lineStyle "+lineStyle)
            # print("color "+str(color))
            # print("style "+str(style))
            # print("x ="+str(x))
            # print('y= '+str(y))
            plt.plot(x,y)
            plt.plot(x,y,lineStyle,label=Botnet)
            plt.legend()
        plt.grid(True)    
        plt.show()

