import pandas as pd

def count_disp():
    df = pd.read_csv("dispositivos.csv")
    quant_regist = len(df)
    return quant_regist