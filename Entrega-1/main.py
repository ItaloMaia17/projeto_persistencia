from fastapi import FastAPI, HTTPException
from dispositivo import Dispositivo
from http import HTTPStatus
from manip_csv import abrir_arq, add_disp, salvar_todos
from cria_hash import gerar_hash
from compac_arquivo import compactar_csv

# Inicializando o FastAPI
app = FastAPI() 

# arquivo CSV
CSV_FILE = "dispositivos.csv" 
# Lista de dispositivos
dispositivos = abrir_arq(CSV_FILE)

# Endpoint 1: listar todos os dispositivos
@app.get("/dispositivos/listar_dispositivos/")
def listar_disp():
    return dispositivos

# Endpoint 2: retornar dispositivo procurado
@app.get("/dispositivos/buscar/{disp_id}", response_model=dict)
def buscar_item(disp_id: int):
    # Percorre a lista de dispositivos
    if not dispositivos:
        raise HTTPException(status_code=404, detail="Não existem dispositivos registrados")
    for dispositivo in dispositivos:
        if dispositivo["id"] == disp_id:
            return dispositivo
    raise HTTPException(status_code=404, detail="Dispositivo não está na lista")

# Endpoint 3: adicionar um dispositivo
@app.post("/dispositivos/adicionar/", response_model=dict, status_code=HTTPStatus.CREATED)
def adicionar_disp(disp: Dispositivo):
    # Verifica se o dispositivo já existe na lista
    if any(disp.id == d["id"] for d in dispositivos):
        raise HTTPException(status_code=400, detail="Modelo já existente")
    disp_novo = disp.__dict__
    # Salva de volta no arquivo CSV
    add_disp(CSV_FILE, disp_novo)
    # Atualiza a lista em memória
    dispositivos.append(disp_novo)  

    return disp_novo  # Retorna o dispositivo adicionado

# Endpoint 4: atualizar dados sobre os dispositivos
@app.put("/dispositivos/atualizar/{disp_id}", response_model= dict)
def atualizar_disp(disp_id: int, disp_atualizado :Dispositivo):
    for indice, disp_atual in enumerate(dispositivos):
        if disp_id == disp_atual["id"]:
            dict_disp = disp_atualizado.__dict__
            dispositivos[indice] = dict_disp
            # Salva de volta no arquivo CSV
            salvar_todos(CSV_FILE, dispositivos)
            return dict_disp
    raise HTTPException(status_code= 404, detail="o item a ser modificado não foi encontrado")

# Endpoint 5: Deletar dispositivos
@app.delete("/dispositivos/deletar/{disp_model}")
def deletar_disp(disp_id: int):
    for disp_atual in dispositivos:
        if disp_atual["id"] == disp_id:
            # Remove da lista
            dispositivos.remove(disp_atual)
            # Salva de volta no arquivo CSV
            salvar_todos(CSV_FILE, dispositivos)
            return {"msg": "Dispositivo removido da lista"}
    raise HTTPException(status_code= 404, detail="o item a ser deletado não foi encontrado")

# Endpoint 6: Mostra a quantidade de registros de dispositivos
@app.get("/dispositivos/contar_dispositivos")
def count_registros():
    return {"total_dispositivos": len(dispositivos)}
    
# Endpoint 7: Gera um hash do arquivo csv
@app.get("/dispositivos/gerar_hash")
def mostrar_hash():
    return {"hash_gerado": gerar_hash(CSV_FILE)}
    
# Endpoint 8: Empacota e compacta o arquivo
@app.get("/dispositivos/compactar")
def compac_arq():
    return compactar_csv(CSV_FILE)
