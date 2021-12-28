import pandas as pd

file_name = input("Enter token file name: ")

df = pd.read_excel("./data/"+file_name+".xlsx", sheet_name='Sheet1', engine='openpyxl')

def convert_date_format():
    n = len(df["Date"])
    print(n)
    
    for i in range(n):
        # change date format 
        if "/" in str(df["Date"][i]).strip():
            x = str(df["Date"][i]).strip().split("/")
            (x[0], x[1]) = (x[1], x[0])
            df["Date"][i] = "-".join(x)
        else:
            d = str(df["Date"][i]).strip().split()[0].split("-")
            d = d[::-1]
            df["Date"][i] = "-".join(d)
        
        # change time format
        if str(df["Format"][i]) == "PM":
            x = str(df["Time"][i]).split(":")
            x[0] = str(12 + int(x[0]) % 12)
            df["Time"][i] = ':'.join(x)


# usually takes 6-7 minutes to run
convert_date_format()

# save the modified file
fname = "./data/latency_formatted.xlsx"
df.to_excel(fname)