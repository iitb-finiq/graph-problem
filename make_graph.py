import pandas as pd

file_name = input("Enter workflow name: ")

df = pd.read_excel("./data/"+file_name+".xlsx",
                   sheet_name='Sheet1', engine='openpyxl')

queue_id = {}
reverse_queue_id = {}
n = len(df["Queue Name"])

for ele in range(len(df["Queue Name"])):
    queue_id[df['Queue Name'][ele]] = ele
    reverse_queue_id[ele] = df['Queue Name'][ele]
