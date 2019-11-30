from Victime import *
from Bot import *
import matplotlib.pyplot as plt
import csv
import numpy as np
from random import shuffle

mu = 5
sigma = 2
VectSize = 1000
vect = np.random.randn(VectSize) * sigma + mu
COLOR=['b','g','r','c','m','y','k','w']
STYLE=['.','v','<','1','s','p','P','*','D','--']

# TODO multiples réplicats avec immunité et delay différents

def GenReplicaVicitme(bot,replicat):
    vuln=[]
    for i in range(replicat):
        vuln.append(bot+' '+str(i))
    #print("Vuln = "+str(vuln))
    return vuln



class Environnement():
    def __init__(self,V,T,TimeMax,step,freqD,freqB):
        self.V=V.copy()
        self.T = T
        self.TimeMax=TimeMax
        self.Step=step
        self.Victimes = list()
        self.Bots = dict()
        self.res=dict()
        self.freqD = freqD
        self.freqB = freqB

    def DeathRate(self):
        # A modifier en fonction de la simulation
        secretsGenerator = secrets.SystemRandom()
        v = secretsGenerator.randint(0,VectSize-1)
        return int(vect[v])



    
    def BirthRate(self):
        # A modifier en fonction de la simulation
        secretsGenerator = secrets.SystemRandom()
        v = secretsGenerator.randint(0,VectSize-1)
        return int(vect[v])
    

    # def detectPsybot(self):        # USE TO DEBUG
    #     count=0
    #     for v in self.Victimes:
    #         if 'psybot 0' in v.vulnerables:
    #             #print("Victime vulnérable à psybot")
    #             count+=1
    #             # if ip == v.numero:
    #             #     print("ip vulnéable à psybot")
    #     print("count = "+str(count))

    def AddNewBot(self, bot, num):
        for i in range(num):
            b = bot.Clone()
            b.Change_Instance(i)
            self.Bots[b.nom]=[]
            self.Bots[b.nom].append(b)

    def GenVictimesEnsemble(self):
        # Dans cette fonction => un random par victime
        # quand vulnérable à 1, le sera aussi a tout ceux qui infecte plus de victimes
        # A revoir
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
    
    def Naissance(self,num):
        # on crée des naissances avec des nouveaux items vulnérables ou non
        secretsGenerator = secrets.SystemRandom()
        victimeSize=len(self.Victimes)
        for i in range(num):
            victim=Victime(victimeSize+i,[])
            for bot,param in self.V.items():
                v = secretsGenerator.randint(0,self.T)
                if v <= param[0]:
                    victim.AddBot(GenReplicaVicitme(bot,param[1]))
            self.Victimes.append(victim)

    def Mort(self,num):
        # selectionner une victime
        # si elle est infectée, supprimer un bot
        secretsGenerator = secrets.SystemRandom()
        victimeSize=len(self.Victimes)
        #print(str(num)+" victimes vont décéder")
        for i in range(num):
            v = secretsGenerator.randint(0,victimeSize-1)
            if len(self.Victimes[v].infection) > 0 :
                #print("victime infectee par "+str(self.Victimes[v].infection))
                for b in self.Victimes[v].infection :
                    if b in self.Bots :
                        botnetSize=len(self.Bots[b])
                        nb = secretsGenerator.randint(0,botnetSize)
                        #print('on tue le bot '+str(nb)+" de "+str(b))
                        del self.Bots[b][nb]
            del self.Victimes[v]
                    # TODO DEL VICTIME DE LA LISTE !!

    def GenVictimesRandom(self):
        # dans cette fonction => reroll random pour chaque bot
        # quand vulnerable à un bot ne l'est pas forcément aux autres
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

    def randomOrder(self,i):
        orderList=[]
        for Botnet in self.Bots :
            for B in self.Bots[Botnet] :
                orderList.append(B)
        shuffle(orderList)
        return orderList
    
    def Turn(self,time):
        secretsGenerator = secrets.SystemRandom()
        orderList = self.randomOrder(time)
        for B in orderList :
            rep={'IP':-1}
            if time >= B.Delay :
                rep = B.Next(self.T)
            #print("Rep = "+str(rep))
            if rep['IP'] != -1 and rep.has_key("nom") and rep.has_key("protection"):
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
                            if len(self.Bots[r]) > 0:
                                # On del un bot random du réseau
                                v = secretsGenerator.randint(0,len(self.Bots[r])-1)
                                del self.Bots[r][v]
                            #print("après "+str(len(self.Bots[r])))
                        pass
                    nBot=B.Clone()
                    nBot.ExploitTime()
                    self.Bots[B.nom].append(nBot) # on ajoute un bot en état d'exploit
                else :
                    B.Gen_IP(self.T)
                    # la victime n'est pas vulnérable on passe le bot en état de génération IP
    
    def Game(self):
        #self.detectPsybot()
        for i in range(self.TimeMax):
            self.Turn(i)
            if i%self.Step == 0 :
                self.CountBots()
                print("tour "+str(i))
            if i%self.freqB == 0 :
                self.Naissance(self.BirthRate())
            if i%self.freqD == 0 :
                self.Mort(self.DeathRate())

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
        self.CountBots()
        for Botnet, stats in self.res.items():
            gstats=[0]
            gstats.extend(stats)
            parts=Botnet.split(" ")
            nom=parts[0]+parts[1]+"-"+str(thread)+".csv"
            files.append(nom)
            with open(nom, option, newline='\n') as csvfile:
                reswritter = csv.writer(csvfile,delimiter=';',quotechar='"',quoting=csv.QUOTE_MINIMAL)
                if option == 'w':
                    x=np.arange(0,self.TimeMax+self.Step,self.Step)
                    reswritter.writerow(x)
                reswritter.writerow(gstats)
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

