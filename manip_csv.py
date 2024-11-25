import pandas as pd
import os

# Este arquivo python contém as funções utilizadas para manipular o arquivo csv

# Lê o arquivo CSV como um DataFrame e converte pra lista de dicionários
def abrir_arq():
    if not os.path.exists("dispositivos.csv"):  # Verifica se o arquivo existe
        # Cria o arquivo e preenche o cabeçalho
        with open("dispositivos.csv", "w") as arq:
            arq.write("id,marca,modelo,tipo,ano_fabricacao,preco\n")
            return []
    
    df = pd.read_csv("dispositivos.csv")
    # Converte para uma lista de dicionários
    dic_disp = df.to_dict(orient="records")
    return dic_disp

# Adiciona novos dispositivos
def add_disp(df):
    # abre o arquivo pra incluir o novo dispositivo
    with open("dispositivos.csv","a", newline="") as arq:
        df.to_csv(arq, index=False, header=False, encoding="utf-8")

# reescreve a lista de dispositivos
def salvar_todos(list_disp):
    df = pd.DataFrame(list_disp)
    df.to_csv("dispositivos.csv", index=False, mode="w", header=True, encoding="utf-8")
