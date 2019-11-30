import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy as np
import secrets


mu = 5
sigma = 2
VectSize = 100000
vect = np.random.randn(VectSize) * sigma + mu

def Affiche_fusion():
    x= []
    b1=[]
    b2=[]
    with open('mirai 0-a_median.csv') as csv1:
        with open('psybot 0-a_median.csv') as csv2:
            plotb1= csv.reader(csv1,delimiter=',')
            plotb2= csv.reader(csv2,delimiter=',')
            i=0
            for row1 in plotb1:
                if i != 0 :
                    x.append(float(row1[0]))
                    b1.append(float(row1[1]))
                i+=1
            i=0
            for row2 in plotb2:
                if i !=0:
                    b2.append(float(row2[1]))
                i+=1
    plt.plot(x,b1,label='mirai')
    plt.plot(x,b2,label='psybot')
    plt.legend(title="test")
    plt.grid(True)    
    plt.show()


def DeathFunction():
    # A modifier en fonction de la simulation
    secretsGenerator = secrets.SystemRandom()
    v = secretsGenerator.randint(0,VectSize-1)
    return int(vect[v])

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


#Affiche_fusion()
Stats_Botnet("mirai.csv",10,1000)
Stats_Botnet("psybot.csv",10,1000)