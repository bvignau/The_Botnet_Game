from stats import *
import configparser
from parallal import *
import pyfastcopy
import os

def ConfToInt(conf):
    res = {}
    for k, v in conf.items():
        res[k]=int(v)
    return res

def RecupBotnetsParam(Population, Botnet):
    V={}
    for k,v in Population.items():
        V[k]=[int(v)]   # ajout du nombre de victimes
    for k,v in Botnet.items():
        V[k].append(int(v)) # ajout du nombre de replicats {bot:[victimes,replicats]}
    print(str(V))
    return V
    

def main():
    config = configparser.ConfigParser()
    config.read('Simultation.conf')
    SimulConf=ConfToInt(config['SIMULATION'])
    V=RecupBotnetsParam(config['POPULATION'],config['BOTNET'])
    env=Environnement(V,SimulConf['total'],SimulConf['time'],SimulConf['steps'])
    env.GenVictimes()
    AddBotToEnv(env,V)
    env.Game()
    files=env.Recup_CSV('w','a')
    #print("files = "+str(files))
    del env
    # threads
    threads=[]
    # creation des threads
    for i in range(SimulConf['threads']):
        threads.append(SimulThread(i,SimulConf['delay'],SimulConf['number'],V,SimulConf['total'],SimulConf['time'],SimulConf['steps']))
    # run 
    for t in threads:
        t.start()
    # wait the end of all threads
    for t in threads:
        t.join()
    # concatenation des fichiers des threads en un fichier de stats par botnet
    for f in files:
        subname=f.split('-')[0]
        with open(f,'ab') as afd:
            for i in range(SimulConf['threads']):
                filename=subname+'-'+str(i)+'.csv'
                print("filename ="+str(filename))
                with open(filename,'rb') as fd:
                    for line in fd:
                        afd.write(line)
                os.remove(filename)
        Stats_Botnet(f,SimulConf['steps'],SimulConf['time'])
    #



if __name__ == '__main__':
    main()