import pandas as pd
import matplotlib.pyplot as plt

def Stats_Botnet(file,step,maxTime):
    df=pd.read_csv(file,delimiter=';')
    nom=file.split('.')[0]
    meanT=[]
    maxT=[]
    minT=[]
    medianT=[]
    x=[]
    for i in range(0,(maxTime-step),step):
        x.append(i)
        meanT.append(df[str(i)].mean())
        maxT.append(df[str(i)].max())
        minT.append(df[str(i)].min())
        medianT.append(df[str(i)].median())
    plt.plot(x,meanT,label="moyenne")
    plt.plot(x,maxT,label="max")
    plt.plot(x,minT,label="min")
    plt.plot(x,medianT,label="medianne")
    plt.legend(title=nom)
    plt.grid(True)    
    plt.show()