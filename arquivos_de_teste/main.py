from fastapi import FastAPI, HTTPException
from dispositivo import Dispositivo
import pandas as pd
# import csv
# from pydantic import BaseModel

app = FastAPI()

# Nome do arquivo CSV
CSV_FILE = "dispositivos2.csv"
# Função auxiliar: Carregar CSV
def load_data():
    try:
        return pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        return pd.DataFrame(columns=["ID", "Marca", "Modelo", "Tipo", "Ano de Fabricação", "preço"])


# Função auxiliar: Salvar CSV
def save_data(df):
    df.to_csv(CSV_FILE, index=False, encoding="utf-8")


# Endpoint 1: Listar todos os dispositivos
@app.get("/dispositivos", response_model=list[Dispositivo])
def listar_dispositivos():
    df = load_data()
    return df.to_dict(orient="records")


# Endpoint 2: Obter dispositivo por ID
@app.get("/dispositivos/{dispositivo_id}", response_model=Dispositivo)
def obter_dispositivo(dispositivo_id: int):
    df = load_data()
    dispositivo = df[df["ID"] == dispositivo_id]
    if dispositivo.empty:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")
    return dispositivo.iloc[0].to_dict()


# Endpoint 3: Criar um novo dispositivo
@app.post("/dispositivos", response_model=Dispositivo)
def criar_dispositivo(dispositivo: Dispositivo):
    df = load_data()
    if dispositivo.id in df["ID"].values:
        raise HTTPException(status_code=400, detail="Dispositivo com esse ID já existe")
    novo_dispositivo = pd.DataFrame([dispositivo.dict()])
    df = pd.concat([df, novo_dispositivo], ignore_index=True)
    save_data(df)
    return dispositivo


# Endpoint 4: Atualizar dispositivo existente
@app.put("/dispositivos/{dispositivo_id}", response_model=Dispositivo)
def atualizar_dispositivo(dispositivo_id: int, dispositivo: Dispositivo):
    df = load_data()
    if dispositivo_id not in df["ID"].values:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")
    df.loc[df["ID"] == dispositivo_id, ["Marca", "Modelo", "Tipo", "Ano de Fabricação","preço"]] = (
        dispositivo.marca,
        dispositivo.modelo,
        dispositivo.tipo,
        dispositivo.ano_fabricacao,
        dispositivo.preco,
    )
    save_data(df)
    return dispositivo

# Endpoint 5: Deletar dispositivo
@app.delete("/dispositivos/{dispositivo_id}", response_model=dict)
def deletar_dispositivo(dispositivo_id: int):
    df = load_data()
    if dispositivo_id not in df["ID"].values:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")
    df = df[df["ID"] != dispositivo_id]
    save_data(df)
    return {"message": "Dispositivo excluído com sucesso"}
