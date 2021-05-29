import pandas as pd
import numpy as np
from modules.prepare_data_by_model import marge_and_split_by_model
from sklearn import linear_model



def _prepare_regressions_for_fuel(fuel):
    result={}
    for model in fuel.keys():
        data=fuel[model]
        reg = linear_model.LinearRegression()
        reg.fit(data[['km','year', 'capacity']],data.price)
        result[model]=reg
    return result

def prepare_regressions():
    basic_torvet_Diesel = pd.read_csv("./data/torvet_Diesel.csv", sep=";")
    basic_basen_Diesel = pd.read_csv("./data/Diesel.csv", sep=";")
    diesel_models= marge_and_split_by_model(basic_torvet_Diesel,basic_basen_Diesel,np)

    basic_torvet_Benzin = pd.read_csv("./data/torvet_Benzin.csv", sep=";")
    basic_basen_Benzin = pd.read_csv("./data/Benzin.csv", sep=";")
    benzin_models= marge_and_split_by_model(basic_torvet_Benzin,basic_basen_Benzin,np)

    reg_diesel = _prepare_regressions_for_fuel(diesel_models)
    reg_benzin = _prepare_regressions_for_fuel(benzin_models)
    models = {"Diesel": diesel_models, "Benzin": benzin_models}
    regressions={"Diesel":reg_diesel,"Benzin":reg_benzin}
    return regressions, models

def estimate_price(regressions, car):
    fuel=car['fuel']
    model=car['model']
    reg= regressions[fuel][model]
    
    estimate = reg.predict(np.array([car['km'],car['year'],car['capacity']]).reshape(1, 3))

    return estimate



def plot_price_by(models,model,fuel,features):
    request_model=models[fuel][model]
   
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter3D(list(request_model[features[0]]),list(request_model[features[1]]),list(request_model['price']), c=request_model['price'], cmap="Blues")
    return fig



