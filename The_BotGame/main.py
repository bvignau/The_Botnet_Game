from stats import *
import configparser
from parallal import *
import pyfastcopy
import os 
import re

def ConfToInt(conf):
	# Retourne un dict dont les valeurs sont converties en int
	res = {}
	for k, v in conf.items():
		res[k]=int(v)
	return res

def RecupBotnetsParam(Exploit, Botnet):
	# Retourne un dict dont les valeurs sont des listes de 2 int [victimes, replicats] 
	V={}
	for k,v in Exploit.items():
		V[k]= [ConfToList(Exploit)]  # ajout des vulnerabilites qu'exploitent les bots
	for k,v in Botnet.items():
		V[k].append(int(v)) # ajout du nombre de replicats {bot:[victimes,replicats]}
	
	return V
	
def ConfToList(conf):
	res = []
	for v in conf.values():
		liste = re.split(", ", re.sub("(\[|])", "", v))
		for val in liste:
			res.append(int(val))
	
	return res

def main():
	config = configparser.ConfigParser()
	config.read('Simultation.conf')
	SimulConf=ConfToInt(config['SIMULATION'])
	V=RecupBotnetsParam(config['EXPLOIT'],config['BOTNET']) # ex {mirai00 : [[1, 1, 0], 1]}
	env=Environnement(V,SimulConf['total'],SimulConf['time'],SimulConf['steps'],150,200, SimulConf['exposant'], SimulConf['seuil'], SimulConf['protection'], ConfToList(config['VULNERABILITE']))
	
	env.GenVictimes() 
	env.CountInfectedHost()
	
	AddBotToEnv(env,V)
	env.Game()
	files=env.Recup_CSV('w','a')
	#print("files = "+str(files))
	del env
	# threads
	threads=[]
	# creation des threads
	for i in range(SimulConf['threads']):
		threads.append(SimulThread(i,SimulConf['delay'],SimulConf['number'],V,SimulConf['total'],SimulConf['time'],SimulConf['steps'], SimulConf['exposant'], SimulConf['seuil'], SimulConf['protection'], ConfToList(config['VULNERABILITE'])))
	# run 
	for t in threads:
		t.start()
	# wait the end of all threads
	for t in threads:
		t.join()
	# concatenation des fichiers des threads en un fichier de stats par botnet
	botnetNames=[]
	for f in files:
		subname=f.split('-')[0]
		botnetNames.append(subname)
		with open(f,'ab') as afd:
			for i in range(SimulConf['threads']):
				filename=subname+'-'+str(i)+'.csv'
				print("filename ="+str(filename))
				with open(filename,'rb') as fd:
					for line in fd:
						afd.write(line)
				os.remove(filename)
		Stats_Botnet(f,SimulConf['steps'],SimulConf['time'])
	Affiche_fusion(botnetNames,SimulConf['steps'],SimulConf['time'])
	#



if __name__ == '__main__':
	main()