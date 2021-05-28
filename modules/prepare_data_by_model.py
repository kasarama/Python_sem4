import pandas as pd
import numpy as np

def _prepare_torvet_data(data):
    
    data = data.drop(["link", "location"], axis=1)

    for index in data.index:
        data.loc[index, "km"] = data.loc[index, "km"].replace(".", "")
        if data.loc[index, "km"].isdigit():
            data.loc[index, "km"] = int(data.loc[index, "km"])
        else:
            data.loc[index, "km"] = None

        if "Audi" not in data.loc[index, "model"]:
            data.loc[index, "model"] = None
        else:
            data.loc[index, "model"] = (
                data.loc[index, "model"].replace("Audi", "").strip()
            )

    data.dropna(inplace=True)

    typ = data["type"]
    capacity = []
    count = 0
    for t in list(typ):

        a = t.split("TFSi")
        if len(a) == 2:
            capacity.append(a[0].strip())
        else:
            b = a[0].split(" ")
            capacity.append(b[0])

        if capacity[count] == None or len(capacity[count]) > 3:

            c = (
                t.replace("Sportback", "")
                .replace("Lang", "")
                .replace("Avant", "")
                .replace("Roadster", "")
                .replace("Spyder", "")
                .strip()
            )
            c = c.split(" ")

            c = c[0]
            capacity[count] = c

        count += 1

    data["capacity"] = capacity

    for index in data.index:
        for col in data.columns:
            if data.loc[index, col] == "-":
                data.loc[index, col] = None
        try:
            capacity=float(data.loc[index,"capacity"].replace(",","."))
            data.loc[index,'capacity']=capacity
        except Exception as e:
            data.loc[index,'capacity']=None

        
    data.dropna(inplace=True)
    data = data.drop(["type"], axis=1)


    data = data.drop_duplicates()

    return data

def _prepare_basen_data(data):
    data= data.drop(['location'], axis=1)

    capa=[None for i in data.index]
    data['capacity']= capa

    for index in data.index:
        data.loc[index, 'km']=str(data.loc[index, 'km']).replace('.','')
        if(data.loc[index, 'km'].isdigit()):
            data.loc[index, 'km']=int(data.loc[index, 'km'])
            if (data.loc[index, 'km']>1000000):
                data.loc[index, 'km']=data.loc[index, 'km']/1000
                #print(index, data.loc[index, 'km'])
        else:
            data.loc[index, 'km']=None
        
        if "Audi" not in data.loc[index,'model']:
            data.loc[index,'model']=None
        else:
            model=data.loc[index,'model'].replace('Audi','').strip().split(' ')[0]
            cap =data.loc[index,'model'].replace('Audi','').strip().split(' ')[1].replace(",",".")
            data.loc[index,'model']=model
            try:
                capacity=float(cap)
                data.loc[index,'capacity']=capacity
            except Exception as e:
                data.loc[index,'capacity']=None
            
            
        data.loc[index, 'price']=data.loc[index, 'price'].replace('kr.','').replace('.','').strip()
        if(data.loc[index, 'price'].isdigit() and int(data.loc[index, 'price'])>1234):
            data.loc[index, 'price']=int(data.loc[index, 'price'])
        else:
            data.loc[index, 'price']=None
  
    data=data.drop_duplicates()
    data.dropna(inplace=True)

    return data


def _split_by_model(data, np):
    uniqe_models = np.unique(data["model"])

    # create a new dataframe for each model
    df_by_model = {}
    for model in uniqe_models:
        df_by_model[model] = pd.DataFrame(columns=data.columns)
        df_by_model[model] = df_by_model[model].append(data[data["model"] == model])
        df_by_model[model] = df_by_model[model].reset_index()
        df_by_model[model] = df_by_model[model].drop("index", axis=1)

    return df_by_model



def marge_and_split_by_model(torvet_data,basen_data, np):
    torvet=_prepare_torvet_data(torvet_data)
    
    basen = _prepare_basen_data(basen_data)


    marge=torvet.append(basen)
    marge=marge.drop_duplicates()
    models=_split_by_model(marge,np)
  
    return models

