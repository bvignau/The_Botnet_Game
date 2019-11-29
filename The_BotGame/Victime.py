class Victime():
    def __init__(self, numero, vulnerables):
        self.numero = numero
        self.vulnerables = list()
        self.infection = list()
        for i in vulnerables :
            self.vulnerables.append(i)
    
    def AddBot(self,vul):
        self.vulnerables.extend(vul)

    def vulnerable(self, bot, vul, clean):
        if bot in self.vulnerables and bot not in self.infection : # si le bot attaquant utilise une vulnérabilité présente sur la victime et qu'il ne l'a pas déjà infecté
            #print("Vulnérable au bot "+bot)
            #print("immunisé à "+str(vul))   # si le bot va immuniser l'appareil contre d'autres bots
            if len(vul) > 0:
                if vul[0] == "*" :
                    self.vulnerables=[]
                else :
                    for v in vul :
                        self.vulnerable.remove(v)
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
        

