import pandas as pd
import numpy as np
import pickle as pkl
from pandas.core.base import NoNewAttributesMixin

np.random.seed(4)

df = pd.read_excel("./data/graph_data.xlsx",
                   sheet_name='Sheet1', engine='openpyxl')
n = len(df["Queue Name"])

def get_inputs():
    inputs = []
    # edge weights
    for i in range(n):
        if str(df['Success Queue'][i]) != 'nan':
            inputs.append("0,"+str(df["Queue Name"][i])+","+str(df['Success Queue'][i])+","+str(np.random.randint(10)))
        if str(df['Fail Queue'][i]) != 'nan':
            inputs.append("0,"+str(df["Queue Name"][i])+","+str(df['Fail Queue'][i])+","+str(np.random.randint(10)))
 
    # node weights
    for i in range(n):
        inputs.append("1,"+str(df["Queue Name"][i])+",0")

    return inputs