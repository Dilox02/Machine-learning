import pandas as pd
from decimal import Decimal



df = pd.read_excel("classificazione.xlsx")

def return_prob(colonna, features):#genera la coppia feature|yes e feature|no e la attribuisce a un dizionario: probs con chiave: feature
    probs = {}
    for feature in features:
        probs[feature] =[0,0]
        count_si = len([+1 for t, target in zip(list(df.iloc[0:h, colonna]), list(df.iloc[0:h, -1])) if t == feature and target == 'si'])/sum(df.iloc[0:h, -1] == 'si') #uso di list comprehension per appesantire la lettura 
        count_no = len([+1 for t, target in zip(list(df.iloc[0:h, colonna]), list(df.iloc[0:h, -1])) if t == feature and target == 'no'])/sum(df.iloc[0:h, -1] == 'no')
        probs[feature][0] = round(Decimal(f"{count_si}"),2)
        probs[feature][1] =round(Decimal(f"{count_no}"),2)
    return probs

def read_column(colonna):
    # restituisce un dizionario contenente tutte le probabilità di quella colonna
    features = []
    [features.append(val) for val in list(df.iloc[0:h, colonna]) if val not in features] #estrae le features senza ripetizioni e le inserisce in una lista
    return return_prob(colonna, features)






def extract_value(label, feature,index):
    return mappa[label][feature][index]

def multiply(features,index):
    res = 1
    counter = 0
    for x in range(0, len(list(mappa.keys()))-1):
        
        res *= round(extract_value(list(mappa.keys())[counter], features[counter],index),2)
        counter += 1
    return res

def return_response(valori: list):
    #print(mappa) #debug
    p0 = round(multiply(valori,0) * extract_value(list(mappa.keys())[-1], 'si',0),6)
    p1 = round(multiply(valori,1) * extract_value(list(mappa.keys())[-1], 'no',1),6)
    print(f"pyes at {p0} - p_no at {p1}")
    if p0 > p1:
        return f"si al {p0*100}%"
    return f"no al {p1*100}%"


#init, costruzione del dizionario mappa con le probabilità
h = len(df)
print(f"h dataframe: {h}")
mappa = {}
colonne = len(df.columns) # n. colonne
for i in range(1, colonne):
    name = df.columns[i]
    mappa[name] = read_column(i) 
mappa['target']['si'][0]=round(Decimal(f"{sum(df.iloc[0:h, -1] == 'si')/h}"),2) #uso di round e Decimal per motivi di perdità di informazione causa floating point scadenti in python
mappa["target"]["no"][1]=round(Decimal(f"{sum(df.iloc[0:h, -1] == 'no')/h}"),2)

values=["freddo","alta","soleggiato","forte"]
print(return_response(values))