import pandas as pd
from fastapi import FastAPI, HTTPException
from dispositivo import Dispositivo
from http import HTTPStatus
from manip_csv import abrir_arq, add_disp, salvar_todos
from cria_hash import gerar_hash
from count_registros_csv import count_disp
from compac_arquivo import compactar_csv

# Inicializando o FastAPI
app = FastAPI() 

# Lista de dispositivos
dispositivos = abrir_arq()

# Endpoint 1: listar todos os dispositivos
@app.get("/dispositivos/listar_dispositivos/")
def listar_disp():
    lista_disp = abrir_arq()
    return lista_disp

# Endpoint 2: retornar dispositivo procurado
@app.get("/dispositivos/buscar/{disp_model}", response_model=dict)
def buscar_item(disp_model: str):
    # Percorre a lista de dispositivos
    for dispositivo in dispositivos:
        if dispositivo["modelo"] == disp_model:
            return dispositivo
    raise HTTPException(status_code=404, detail="Dispositivo não está na lista")

# Endpoint 3: adicionar um dispositivo
@app.post("/dispositivos/adicionar/", response_model=dict, status_code=HTTPStatus.CREATED)
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
@app.put("/dispositivos/atualizar/{disp_model}", response_model= Dispositivo)
def atualizar_disp(disp_model: str, disp_atualizado :Dispositivo):
    if any(disp_atualizado.id == d["id"] and disp_atualizado.modelo == d["modelo"] for d in dispositivos):
        raise HTTPException(status_code= 404, detail="já existe um item com o mesmo id ou modelo cadastrado")
    for indice, disp_atual in enumerate(dispositivos):
        if disp_model == disp_atual["modelo"]:
            dispositivos[indice] = disp_atualizado.dict()
            # Salva de volta no arquivo CSV
            salvar_todos(dispositivos)
            return disp_atualizado
    raise HTTPException(status_code= 404, detail="o item a ser modificado não foi encontrado")

# Endpoint 5: Deletar dispositivos
@app.delete("/dispositivos/deletar/{disp_model}")
def deletar_disp(disp_model: str):
    for disp_atual in dispositivos:
        if disp_atual["modelo"] == disp_model:
            # Remove da lista
            dispositivos.remove(disp_atual)
            # Salva de volta no arquivo CSV
            salvar_todos(dispositivos)
            return {"msg": "Dispositivo removido da lista"}
    raise HTTPException(status_code= 404, detail="o item a ser deletado não foi encontrado")

# Endpoint 6: Mostra a quantidade de registros de dispositivos
@app.get("/dispositivos/contar_dispositivos")
def count_registros():
    total_disp = count_disp()
    return {"total_dispositivos": total_disp}
    
# Endpoint 7: Gera um hash do arquivo csv
@app.get("/dispositivos/gerar_hash")
def mostrar_hash():
    hash_gerado = gerar_hash()
    return {"hash_gerado": hash_gerado}
    
# Endpoint 8: Empacota e compacta o arquivo
@app.get("/dispositivos/compactar")
def compac_arq():
    arq_zip = compactar_csv()
    return arq_zip
