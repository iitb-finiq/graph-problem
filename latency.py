import pandas as pd
import numpy as np
import pickle as pkl

df = pd.read_excel("data/date_formatted.xlsx",
                   sheet_name='Sheet1', engine='openpyxl')
n = len(df["TS_TID"])


def f(x):
    return 1/(1+np.exp(-x))

# find difference of two dates
# date format: dd-mm-yyyy


def date_diff(d1, d2):
    dt1 = [int(x) for x in str(d1).split("-")]
    dt2 = [int(x) for x in str(d2).split("-")]
    t1 = dt1[0]+dt1[1]*22+dt1[2]*252
    t2 = dt2[0]+dt2[1]*22+dt2[2]*252
    return (t2 - t1)*24*60*60

# find difference of two times
# time format: hh:mm:ss


def time_diff(t1, t2):
    ti1 = [int(x) for x in str(t1).split(":")]
    ti2 = [int(x) for x in str(t2).split(":")]
    x1 = ti1[0]*60*60+ti1[1]*60+ti1[2]
    x2 = ti2[0]*60*60+ti2[1]*60+ti2[2]
    return x2 - x1

# find latency for the given data


def find_latency():
    for i in range(1, n):
        if df["TS_TID"][i - 1] == df["TS_TID"][i]:
            df["Latency"][i] = date_diff(str(
                df["Date"][i - 1]), str(df["Date"][i])) + time_diff(df["Time"][i - 1], df["Time"][i])


# usually takes 6-7 minutes to run
find_latency()

fname = "data/latency.xlsx"
df.to_excel(fname)

file_name = input("Enter workflow name: ")

df2 = pd.read_excel("./data/"+file_name+".xlsx",
                   sheet_name='Sheet1', engine='openpyxl')

queue_id = {}
m = len(df2["Id"])

# store the weights on the edges
# corresponding to the found latency
weights = np.zeros((2 * m, 2 * m))
cnt = np.zeros((2 * m, 2 * m))

for ele in range(m):
    queue_id[df2['Id'][ele]] = ele


for i in range(1, n):
    if df["TS_TID"][i - 1] == df["TS_TID"][i]:
        # drop latency greater than a day
        if df["Latency"][i] < 24*60*60:
            e1 = queue_id[df["QS_ID"][i-1]] + m
            e2 = queue_id[df["QS_ID"][i]]
            weights[e1][e2] += df["Latency"][i]
            cnt[e1][e2] += 1

weights = f(np.divide(weights, cnt + 1e-12))

file = open('data/average_latency', 'wb')
pkl.dump([weights], file)
file.close()
