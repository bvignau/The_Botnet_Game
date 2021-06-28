class Victime():
	""" 
	"""
	def __init__(self, numero, vulnerabilites):
		"""
		"""
		self.numero = numero
		self.vulnerabilites = list()	# liste des vulnerabilités de la victime
		self.vulnerables = list()		# liste de bots dont elle est vulnérable	
		self.infection = list() 		# liste de bots qui ont infecté la victime

		for vul in vulnerabilites:
			self.vulnerabilites.append(int(vul))
		 

	def AddVulnerabilite(self, vul):
		self.vulnerabilites.append(int(vul))  

 
	def vulnerable(self, bot, protection, clean, vulns): 
		""" Retourne un tuple contenant un boolean qui définit si l'infection a été faite ainsi que la liste des infections 
		supprimées.

		Parameters:
			bot (Bot): le bot qui tente d'infecter la victime 
			protection (list):  la liste des bots dont le bot est protégé  
			clean (list): liste des infections qu'elle supprime 
			vulns(list): liste de boolean indiquant les vul. exploitable par le  bot
		Returns: 
			(bool) : infecté ou non
			(list) : liste des infections retirées 
		""" 
    
		vulnerable = False	 		# vérifie que la victime a des vul. exploitables par le bot
		for i in range(len(vulns)):
			if self.vulnerabilites[i] == 1 and self.vulnerabilites[i] == vulns[i] :
				vulnerable = True
  
		if bot not in self.infection and vulnerable == True: # si le bot attaquant utilise une vulnérabilité présente sur la victime et qu'il ne l'a pas déjà infecté
			#print("Vulnérable au bot "+bot)
			#print("immunisé à "+str(vul))   # si le bot va immuniser l'appareil contre d'autres bots
			if len(protection) > 0:
				if protection[0] == "*" :
					for vul in self.vulnerabilites:
						vul = 0   
			removed=[]
			for c in clean :    # si le bot clean d'autres infections. 
				if c in self.infection :
					self.infection.remove(c)
					removed.append(c)
					#print("on remove : "+str(c))
			self.infection.append(bot)  # la victime a été infecté => modifier les bots 
			#print("removed = "+str(removed))
			return True,removed # True pour dire que l'infection a été faite
		else :
			return False,[]    # False si la victime est immunisé à ce bot
		

