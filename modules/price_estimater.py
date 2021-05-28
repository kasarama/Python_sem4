import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
from modules.prepare_data_by_model import marge_and_split_by_model
import matplotlib.pyplot as plt


def estimate_price_1f(fuel, model, kms):
    basic_torvet = pd.read_csv("./data/torvet_" + fuel + ".csv", sep=";")
    basic_basen = pd.read_csv("./data/" + fuel + ".csv", sep=";")
    models = marge_and_split_by_model(basic_torvet,basic_basen, np)
    
    request_model = models[model]
    
    reg = linear_model.LinearRegression()
    reg.fit(request_model[['km']], request_model.price)
    
    reg.coef_
    reg.intercept_
    
    estimate = reg.predict(np.array([kms]).reshape(1, 1))
    
    print(reg.coef_)
    print(reg.intercept_)
    print(estimate)
    
    estimate = str(estimate[0])
    final_estimate ={}
    
    final_estimate['Model'] = ("Audi " + model)
    final_estimate['Coefficient'] = (reg.coef_)
    final_estimate['Intercept'] = (reg.intercept_)
    final_estimate['Estimated_Price'] = (estimate + " kr")
    
    fig1, ax1 = plt.subplots()

    ax1.ticklabel_format(style='plain')
    ax1.scatter(request_model.km,request_model.price, color ='red', marker ='+')
    ax1.plot(request_model.km, reg.predict(request_model[['km']]), color = 'blue')
    
    return final_estimate

##Audi_A1 = estimate_price_1f("Diesel", "A1", 200000)

def estimate_price_2f(fuel, model, kms, year):
    basic_torvet = pd.read_csv("./data/torvet_" + fuel + ".csv", sep=";")
    basic_basen = pd.read_csv("./data/" + fuel + ".csv", sep=";")
    models = marge_and_split_by_model(basic_torvet,basic_basen, np)
    
    request_model = models[model]
    
    reg = linear_model.LinearRegression()
    reg.fit(request_model[['km','year']], request_model.price)
    
    reg.coef_
    reg.intercept_
    
    estimate = reg.predict(np.array([kms,year]).reshape(1, 2))
    
    estimate = str(estimate[0])
    final_estimate ={}
    
    final_estimate['Model'] = ("Audi " + model)
    final_estimate['Coefficient'] = (reg.coef_)
    final_estimate['Intercept'] = (reg.intercept_)
    final_estimate['Estimated_Price'] = (estimate + " kr")
    
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.scatter3D(list(request_model['km']),list(request_model['year']),list(request_model['price']), c=request_model['price'], cmap="Blues")
    
    return final_estimate

## Audi_A1 = estimate_price_2f("Diesel", "A1", 500000,2015)

