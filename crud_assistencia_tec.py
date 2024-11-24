from fastapi import FastAPI, HTTPException
from dispositivo import Dispositivo
from http import HTTPStatus
import pandas as pd
import os

# Inicializando o FastAPI
app = FastAPI() 
# cria o arquivo e preenche o cabeçalho
arquivo_disp = "dispositivo.csv"
with open(arquivo_disp, "w") as arq:
    arq.write("Id, Marca, Modelo, Tipo, Ano de Fabricacao,preco\n")

# Lê o arquivo CSV como um DataFrame e converte pra lista de dicionários
def abrir_arq(arquivo_disp):
    if not os.path.exists(arquivo_disp):  # Verifica se o arquivo existe
        return []
    df = pd.read_csv(arquivo_disp)
    # Converte para uma lista de dicionários
    dic_disp = df.to_dict(orient="records")
    return dic_disp

# Adiciona novos dispositivos
def add_disp(df):
    df.to_csv(arquivo_disp, index=False, mode="a", header=False, encoding="utf-8")
# reescreve a lista de dispositivos
def salvar_todos(list_disp):
    df = pd.DataFrame(list_disp)
    df.to_csv(arquivo_disp, index=False, mode="w", header=True, encoding="utf-8")
# Lista de dispositivos
dispositivos = abrir_arq(arquivo_disp)

# Endpoint 1: listar todos os dispositivos
@app.get("/dispositivos/")
def listar_disp():
    lista_disp = abrir_arq(arquivo_disp)
    return lista_disp
# Endpoint 2: retornar dispositivo procurado
@app.get("/dispositivos/{disp_model}", response_model=dict)
def buscar_item(disp_model: str):
    # Percorre a lista de dispositivos
    for dispositivo in dispositivos:
        if dispositivo["modelo"] == disp_model:
            return dispositivo
    raise HTTPException(status_code=404, detail="Dispositivo não está na lista")
# Endpoint 3: adicionar um dispositivo
@app.post("/dispositivos/", response_model=dict, status_code=HTTPStatus.CREATED)
def adicionar_disp(disp: Dispositivo):
    # Verifica se o dispositivo já existe na lista
    if any(disp.id == d["id"] or disp.modelo == d["modelo"] for d in dispositivos):
        raise HTTPException(status_code=400, detail="Modelo já existente")
    disp_novo = disp.dict()
    # Salva de volta no arquivo CSV
    df = pd.DataFrame([disp_novo])
    add_disp(df)
    # Atualiza a lista em memória
    dispositivos.append(disp_novo)  

    return disp_novo  # Retorna o dispositivo adicionado
# Endpoint 4: atualizar dados sobre os dispositivos
@app.put("/dispositivos/{disp_model}", response_model= Dispositivo)
def atualizar_disp(disp_model: str, disp_atualizado :Dispositivo):
    for indice, disp_atual in enumerate(dispositivos):
        if disp_model == disp_atual["modelo"]:
            dispositivos[indice] = disp_atualizado.dict()
            # Salva de volta no arquivo CSV
            salvar_todos(dispositivos)
            return disp_atualizado
    raise HTTPException(status_code= 404, detail="o item a ser modificado não foi encontrado")
# Endpoint 5 deletar dispositivos
@app.delete("/dispositivos/{disp_model}")
def deletar_disp(disp_model: str):
    for disp_atual in dispositivos:
        if disp_atual["modelo"] == disp_model:
            # Remove da lista
            dispositivos.remove(disp_atual)
            # Salva de volta no arquivo CSV
            salvar_todos(dispositivos)
            return {"msg": "Dispositivo removido da lista"}
    raise HTTPException(status_code= 404, detail="o item a ser deletado não foi encontrado")