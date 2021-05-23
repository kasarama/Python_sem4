import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn import linear_model


def prepare_torvet_data():
    data = pd.read_csv("../data/torvet_Benzin.csv", sep=";")
    data = data.drop(["link", "location"], axis=1)

    for index in data.index:
        data.loc[index, "km"] = data.loc[index, "km"].replace(".", "")
        if data.loc[index, "km"].isdigit():
            data.loc[index, "km"] = float(data.loc[index, "km"])
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
    data.dropna(inplace=True)

    data = data.drop_duplicates()

    return data


def split_by_model(data):
    uniqe_models = np.unique(data["model"])

    # create a new dataframe for each model
    df_by_model = {}
    for model in uniqe_models:
        df_by_model[model] = pd.DataFrame(columns=data.columns)
        df_by_model[model] = df_by_model[model].append(data[data["model"] == model])
        df_by_model[model] = df_by_model[model].reset_index()
        df_by_model[model] = df_by_model[model].drop("index", axis=1)

    return df_by_model


def plot_price_by_year(tmp, model):
    fig = plt.figure()

    ax = fig.add_subplot(111)

    plt.ylabel("price")
    # tmp=df_by_model['A1']
    for c in np.unique(tmp["capacity"]):
        data_by_capa = tmp[tmp["capacity"] == c]
        y = data_by_capa["price"]
        x = data_by_capa["year"]
        plt.scatter(x, y, label=c)
        plt.suptitle(model)
        # plt.xlim([1990, 2020])
        # plt.ylim([5000,50000])

        plt.legend()


data = prepare_torvet_data()

models = split_by_model(data)

#for k in models.keys():
#    plot_price_by_year(models[k], k)
