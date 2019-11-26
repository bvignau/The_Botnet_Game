import secrets
import copy


class Bot():
    # Classe mère de bot, a étendre pour modéliser le comportement de chaque botnet
    # Pour faire un botnet, il faut étendre la méthode Gen_IP()
    def __init__(self, nom,Gen_IP,Test_IP,Exploit_IP,num,delay):
        self.nom = nom                      # nom du botnet
        self.num = num                      # numéro du botnet
        self.Tps_Gen_IP = Gen_IP            # Temps de génération d'adresse IP
        self.Tps_Test_IP = Test_IP          # Temps de test pour savoir si une IP est vulnérable ou non
        self.Tps_Exploit_IP = Exploit_IP    # temps d'exploitation d'une IP
        self.Protection = list()        # représente les fonctionnalité d'efficacité permettant de patcher contre d'autre bot (ex :fermeture port)
        self.Supression = list()        # idem mais supression d'autre bots (ex wifatch)
        self.Tps_restant = 0            # variable interne pour chronométrer le temps à rester dans un état
        self.State = "init"             # état actuel
        self.IP=-1                      # IP en cours d'exploitation/ test
        self.Delay = delay              # delay avant de commencer = pour le retard
    
    def Strat_IP(self,max_ip):          # Méthode de génération de l'IP reflétant la stratégie du botnet. A refaire pour chaque bot
        secretsGenerator = secrets.SystemRandom()
        return secretsGenerator.randint(0,max_ip-1)        # génération random type Mirai

    def Change_Instance(self,i):
        nom=self.nom.split()[0]+" "+str(i)
        #print("nom = "+nom)
        self.nom=nom
        self.num=i

    def Clone(self):
        clone=copy.deepcopy(self)
        clone.IP=-1
        clone.State="init"
        return clone
    

    # def AddBot(self, environnement, num):
    #     for i in range(num):
    #         b = self.Clone()
    #         b.Change_Instance(i)
    #         environnement.AddNewBot(b)
    
    def Gen_IP(self, max_ip):                       
        if self.State != "Gen_IP" :                  # on vient de rentrer dans l'état de génération d'adresses IP 
            self.State="Gen_IP"
            self.Tps_restant = self.Tps_Gen_IP
            return {'IP':-1}
        else :
            if self.Tps_restant > 0 :               # tant que le temps n'est pas écoulé la génération n'est pas terminé
                self.Tps_restant-=1
                return {'IP':-1}
            else :
                self.State = "Test_IP"             # le temps est écoulé, on crée une adresse ip
                self.Tps_restant = self.Tps_Test_IP
                #print("génération IP")
                self.IP =  self.Strat_IP(max_ip)         # génération de l'adresse IP, doit varier pour chaque botnet en fonction de sa stratégie
                return {'IP':-1}
                #print("IP = "+str(self.IP))

    def ExploitTime(self):                  # méthode pour que l'environnement puisse passer le bot en phase d'exploit si il a trouvé une IP vulnérable
        self.State="Exploit_IP"
        #print("Exploit !!")
        self.Tps_restant=self.Tps_Exploit_IP
    
    def Next(self, max_ip):             # méthode gérant le graphe d'état
        # print("############################################")
        # print("   ")
        # print("ETAT = "+str(self.State))
        # print("############################################")
        if self.State == "init" :       # initialisation du bot
            #print("OK "+str(max_ip))
            self.Gen_IP(max_ip)
            return {'IP':-1}
        if self.State == "Gen_IP" :     # génération d'adresse IP
            self.Gen_IP(max_ip)
            return {'IP':-1} 
        if self.State == "Test_IP" :    # on est en phase de scan sur une adresse IP
            if self.Tps_restant > 0:
                self.Tps_restant-=1
                #print("dans test IP")
                return {'IP':-1}
            else :                      # on vient de terminer le temps pour tester une IP
                self.State="Waiting Env"
                #print("demande env test")
                #print(str(self.IP))
                return {'IP':int(self.IP), 'nom':self.nom, 'protection':self.Protection, 'supression':self.Supression} # envoie à l'environnement tous les paramètres
        if self.State == "Exploit_IP":
            if self.Tps_restant > 0 :
                self.Tps_restant-=1
                #print("Temps d'exploit")
                return {'IP':-1}    # l'exploit est terminé, le nouveau bot est opérationnel
            else :
                return self.Gen_IP(max_ip)

#
#       Class pour le Bot Mirai, les valeur de temps sont random et doivent encore être définies
#       Action = 
#       Action = 

class MiraiBot(Bot):
    def __init__(self,instance):
        self.nom = "mirai "+str(instance)
        self.num = instance
        self.Tps_Gen_IP = 3         # A ajuster en fonction des données trouvées
        self.Tps_Test_IP = 2        #   Idem    
        self.Tps_Exploit_IP = 4    #   Idem
        self.State = "init"
        self.Protection = ["*"]
        self.Supression = ["psybot"]
        self.Tps_restant = 0
        self.IP=-1
        self.Delay=250

class PsyBot(Bot):
    def __init__(self,instance):
        self.nom = "psybot "+str(instance)
        self.num = instance
        self.Tps_Gen_IP = 1         # A ajuster en fonction des données trouvées
        self.Tps_Test_IP = 2        #   Idem    
        self.Tps_Exploit_IP = 4    #   Idem
        self.State = "init"
        self.Protection = []
        self.Supression = []
        self.Tps_restant = 0
        self.IP=-1
        self.Delay=0
    
    def Strat_IP(self,max_ip):          # Méthode de génération de l'IP reflétant la stratégie du botnet. A refaire pour chaque bot
        if self.IP != max_ip :
            return self.IP+1
        else :
            return 0