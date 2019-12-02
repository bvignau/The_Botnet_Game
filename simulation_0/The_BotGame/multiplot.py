import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy as np
import secrets


mu = 5
sigma = 2
VectSize = 100000
vect = np.random.randn(VectSize) * sigma + mu
STYLE=['+','.','v','*','<','1','s','p','P','D','--']


def affRes(nb, nom):
    fileAll=nom+"_a.csv"
    with open(fileAll,"a") as afd :
        for i in range(nb):
            filleD=nom+" 0-"+str(i)+".csv"
            with open(filleD,"r") as fd :
                for line in fd:
                        afd.write(line)

def Stats_Botnet(file,step,maxTime):
    df=pd.read_csv(file,delimiter=';')
    nom=file.split('.')[0]
    meanT=[]
    maxT=[]
    minT=[]
    medianT=[]
    x=[]
    for i in range(0,(maxTime+step),step):
        x.append(i)
        meanT.append(df[str(i)].mean())
        maxT.append(df[str(i)].max())
        minT.append(df[str(i)].min())
        medianT.append(df[str(i)].median())
    median={'time':x,'median':medianT}
    df = pd.DataFrame(median, columns=['time','median'])
    filename=nom.split('-')[0]+"_median.csv"
    export_csv = df.to_csv(filename,index=None,header=True)
    plt.plot(x,meanT,marker="+",label="moyenne")
    plt.plot(x,maxT,marker=".",label="max")
    plt.plot(x,minT,marker="v",label="min")
    plt.plot(x,medianT,marker="*",label="medianne")
    plt.legend(title=nom)
    plt.grid(True)    
    plt.show()


def Affiche_fusion(botnet,step,maxTime):
    # botnet = liste des noms de botnet
    x= range(0,(maxTime+step),step)
    B={}
    for b in botnet :
        file=b+"_median.csv"
        with open(file) as csvf:
            i=0
            pltbot= csv.reader(csvf,delimiter=',')
            B[b]=[]
            for row in pltbot:
                if i !=0:
                    B[b].append(float(row[1]))
                i+=1
    for b in B.keys() :
        i=0
        plt.plot(x,B[b],marker=STYLE[i],label=b)
        i+=1
    plt.legend(title="all botnet")
    plt.grid(True)    
    plt.show()

#Affiche_fusion()
Stats_Botnet("mirai.csv",50,5000)
Stats_Botnet("psybot.csv",50,5000)
Affiche_fusion(["mirai","psybot"],50,5000)