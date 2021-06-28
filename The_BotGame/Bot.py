import secrets
import copy


class Bot():
	"""
		Classe mère de bot, a étendre pour modéliser le comportement de chaque botnet
		Pour faire un botnet, il faut étendre la méthode Gen_IP()
	"""
	def __init__(self, nom,Gen_IP,Test_IP,Exploit_IP,num,delay):
		self.nom = nom                      # nom du botnet (suivi d'un espace)
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
		self.Initial_Time= Gen_IP

	def Strat_IP(self,max_ip):          # Méthode de génération de l'IP reflétant la stratégie du botnet. A refaire pour chaque bot
		secretsGenerator = secrets.SystemRandom()
		return secretsGenerator.randint(0, max_ip-1)        # génération random type Mirai

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
				# print("génération IP")
				self.IP =  self.Strat_IP(max_ip)         # génération de l'adresse IP, doit varier pour chaque botnet en fonction de sa stratégie
				return {'IP':-1}
				# print("IP = "+str(self.IP))

	def ExploitTime(self):                  # méthode pour que l'environnement puisse passer le bot en phase d'exploit si il a trouvé une IP vulnérable
		self.State="Exploit_IP"
		#print("Exploit !!")
		self.Tps_restant=self.Tps_Exploit_IP

	def Next(self, max_ip, infected_rate, seuil, exposant):             # méthode gérant le graphe d'état
		# print("############################################")
		# print("   ")
		# print("ETAT = "+str(self.State))
		# print("############################################")

		
		# Augmentation du temps necessaire pour generer une addr ip quand le reseau est saturé
		if infected_rate*100 > seuil: 
			self.Tps_Gen_IP = self.Initial_Time + pow(1 - infected_rate + 1, exposant) 
			# etant donné que c'est de l'ordre du décimal, pas très impactant

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
				return {'IP':-1}    	# l'exploit est terminé, le nouveau bot est opérationnel
			else :
				return self.Gen_IP(max_ip)

#       Class pour le Bot Mirai, les valeur de temps sont random et doivent encore être définies
#       Action =

class MiraiBot0(Bot):
	"""
	Bot mirai qui ne supprime aucun autre bot lors d'une tentative d'infection d'une machine infectée
	"""
	def __init__(self,instance):
		self.nom = "mirai0 "+str(instance)
		self.num = instance
		self.Tps_Gen_IP = 3         # A ajuster en fonction des données trouvées
		self.Tps_Test_IP = 5        #   Idem
		self.Tps_Exploit_IP = 4    #   Idem
		self.State = "init"
		self.Protection = []
		self.Supression = []
		self.Tps_restant = 0
		self.IP=-1
		self.Delay=0
		self.Initial_Time = self.Tps_Gen_IP
		

class MiraiBot1(Bot):
	def __init__(self,instance):
		self.nom = "mirai1 "+str(instance)
		self.num = instance
		self.Tps_Gen_IP = 3         # A ajuster en fonction des données trouvées
		self.Tps_Test_IP = 5        #   Idem
		self.Tps_Exploit_IP = 4    #   Idem
		self.State = "init"
		self.Protection = ["*"]
		self.Supression = ["psybot"]
		self.Tps_restant = 0
		self.IP=-1
		self.Delay=100
		self.Initial_Time = self.Tps_Gen_IP
		

class MiraiBot2(Bot):
	def __init__(self,instance):
		self.nom = "mirai2 "+str(instance)
		self.num = instance
		self.Tps_Gen_IP = 3         # A ajuster en fonction des données trouvées
		self.Tps_Test_IP = 5        #   Idem
		self.Tps_Exploit_IP = 4    #   Idem
		self.State = "init"
		self.Protection = ["*"]
		self.Supression = ["psybot"]
		self.Tps_restant = 0
		self.IP=-1
		self.Delay=150
		self.Initial_Time = self.Tps_Gen_IP
		

class MiraiBot3(Bot):
	def __init__(self,instance):
		self.nom = "mirai3 "+str(instance)
		self.num = instance
		self.Tps_Gen_IP = 3         # A ajuster en fonction des données trouvées
		self.Tps_Test_IP = 5        #   Idem
		self.Tps_Exploit_IP = 4    #   Idem
		self.State = "init"
		self.Protection = ["*"]
		self.Supression = ["psybot"]
		self.Tps_restant = 0
		self.IP=-1
		self.Delay=300
		self.Initial_Time = self.Tps_Gen_IP
		

class MiraiBot4(Bot):
	def __init__(self,instance):
		self.nom = "mirai4 "+str(instance)
		self.num = instance
		self.Tps_Gen_IP = 3         # A ajuster en fonction des données trouvées
		self.Tps_Test_IP = 5        #   Idem
		self.Tps_Exploit_IP = 4    #   Idem
		self.State = "init"
		self.Protection = ["*"]
		self.Supression = ["psybot"]
		self.Tps_restant = 0
		self.IP=-1
		self.Delay=1000
		self.Initial_Time = self.Tps_Gen_IP
		

class MiraiBot5(Bot):
	""" Classe de bot Mirai, avec génération d'ip aléatoire et méthode de scan distribué dichotomique
	"""
	def __init__(self,instance):
		self.nom = "mirai5 "+str(instance)
		self.num = instance
		self.Tps_Gen_IP = 3         # A ajuster en fonction des données trouvées
		self.Tps_Test_IP = 5        #   Idem
		self.Tps_Exploit_IP = 4    #   Idem
		self.State = "init"
		self.Protection = ["*"]
		self.Supression = [""]
		self.Tps_restant = 0
		self.IP=-1
		self.Delay=0
		self.Derniere_IP = 0
		self.Max_IP = -1
		self.Initial_Time = self.Tps_Gen_IP
		

	def Clone(self):
		clone=copy.deepcopy(self)
		clone.IP=-1
		clone.Derniere_IP = int((self.Max_IP - self.Derniere_IP)/2) + 1
		clone.Max_IP = self.Max_IP
		clone.State="init"
		self.Max_IP = int((self.Max_IP - self.Derniere_IP)/2)

		# print("Clone - [Derniere IP : " + str(clone.Derniere_IP) + " ; Max IP : " + str(clone.Max_IP) + "]")
		return clone

	def Strat_IP(self, max_ip):
		secretsGenerator = secrets.SystemRandom()
		if self.Max_IP == -1:
			self.Max_IP = max_ip

		self.Derniere_IP = secretsGenerator.randint(self.Derniere_IP, self.Max_IP - 1)

		# print("Bot Scan - [Derniere IP : " + str(self.Derniere_IP) + " ; Max IP : " + str(self.Max_IP) + "]")

		return self.Derniere_IP


class PsyBot0(Bot):
	def __init__(self,instance):
		self.nom = "psybot0 "+str(instance)
		self.num = instance
		self.Tps_Gen_IP = 1        # A ajuster en fonction des données trouvées
		self.Tps_Test_IP = 1        #   Idem
		self.Tps_Exploit_IP = 1    #   Idem
		self.State = "init"
		self.Protection = []
		self.Supression = []
		self.Tps_restant = 0
		self.IP=-1
		self.Delay=0
		self.Initial_Time = self.Tps_Gen_IP
		

	def Strat_IP(self,max_ip):          # Méthode de génération de l'IP reflétant la stratégie du botnet. A refaire pour chaque bot
		if self.IP != max_ip:
			return self.IP+1		#check les IP jusqu'a IP max
		else :
			return 0

class PsyBot1(Bot):
	""" Classe de bot Psybot, avec génération d'ip séquentielle et méthode de scan distribué dichotomique
	"""
	def __init__(self,instance):
		self.nom = "psybot1 " + str(instance)
		self.num = instance
		self.Tps_Gen_IP = 1        # A ajuster en fonction des données trouvées
		self.Tps_Test_IP = 1        #   Idem
		self.Tps_Exploit_IP = 1    #   Idem
		self.State = "init"
		self.Protection = []
		self.Supression = []
		self.Tps_restant = 0
		self.IP=-1
		self.Delay=0
		self.Max_IP = -1	# Initialisation de la taille de population
		self.Initial_Time = self.Tps_Gen_IP
		

	def Clone(self):
		clone=copy.deepcopy(self)
		clone.State="init"
		clone.IP = self.IP + int((self.Max_IP-self.IP)/2) + 1
		clone.Max_IP = self.Max_IP
		self.Max_IP = self.IP + int((self.Max_IP-self.IP)/2) 

		return clone

	def Strat_IP(self,max_ip):          # Méthode de génération de l'IP reflétant la stratégie du botnet. A refaire pour chaque bot
		if self.Max_IP == -1:
			# Attribution de la taille de la pop.
			self.Max_IP = max_ip

		if self.IP < self.Max_IP:
			return self.IP+1
		else :
			return 0

class PsyBot2(Bot):
	""" Classe de bot Psybot, avec génération d'ip séquentielle et méthode de scan distribué dichotomique
	puis random à la fin du scan de la liste
	"""
	def __init__(self,instance):
		self.nom = "psybot2 " + str(instance)
		self.num = instance
		self.Tps_Gen_IP = 1        # A ajuster en fonction des données trouvées
		self.Tps_Test_IP = 1        #   Idem
		self.Tps_Exploit_IP = 1    #   Idem
		self.State = "init"
		self.Protection = []
		self.Supression = []
		self.Tps_restant = 0
		self.IP= -1
		self.Delay= 0
		self.Max_IP = -1	# Initialisation de la taille de population
		self.Initial_Time = self.Tps_Gen_IP
		

	def Clone(self):
		clone=copy.deepcopy(self)
		clone.State="init"
		clone.IP = self.IP + int((self.Max_IP-self.IP)/2) + 1
		clone.Max_IP = self.Max_IP
		self.Max_IP = self.IP + int((self.Max_IP-self.IP)/2) 

		return clone

	def Strat_IP(self,max_ip):
		if self.Max_IP == -1:
			# Attribution de la taille de la pop.
			self.Max_IP = max_ip
		elif self.IP == self.Max_IP:
			self.Max_IP = max_ip
			# Scan random sur l'ensemble de la population
			secretsGenerator = secrets.SystemRandom()
			self.IP = secretsGenerator.randint(0, self.Max_IP-1)

		if self.IP < self.Max_IP:
			return self.IP+1
		else :
			return 0



