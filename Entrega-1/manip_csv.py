import os
import csv
import pandas as pd

def abrir_arq(path_arquivo):
    """abre o arquivo csv e envia em forma de lista de dicionarios
    Args:
        path_arquivo(str): string contendo o caminho para o arquivo
    Returns:
        List: retorna uma lista de dicionários
    """
    if not os.path.exists(path_arquivo):  # Verifica se o arquivo existe
        # Cria o arquivo e preenche o cabeçalho
        with open(path_arquivo, "w") as arq:
            arq.write("id,marca,modelo,tipo,ano_fabricacao,preco\n")
            return []
    
    df = pd.read_csv(path_arquivo)
    # Converte para uma lista de dicionários
    dic_disp = df.to_dict(orient="records")
    return dic_disp

def add_disp(arquivo, novo_disp):
    """Insere novos dispositivos no arquivo csv
    Args:
        arquivo(str): Caminho para o arquivo que vai ser modificado
        novo_disp(Dict): Novo dispositivo a ser adicionado
    Return:
    
    """
    if not os.path.exists(arquivo):  # Verifica se o arquivo existe
        abrir_arq(arquivo)
    # abre o arquivo pra incluir o novo dispositivo
    with open(arquivo,"a", newline="", encoding="Utf-8") as arq:
        writer = csv.DictWriter(arq, fieldnames=novo_disp.keys())
        # Verifica se o arquivo está vazio
        if arq.tell() == 0:
            writer.writeheader()
        writer.writerow(novo_disp)
            
        
def salvar_todos(arquivo, list_disp):
    """reescreve todo o csv
    Args:
        list_disp(List): Recebe uma lista de dicionarios que sera convertida em um DataFrame e adicionada ao csv.
    Return:

    """
    df = pd.DataFrame(list_disp)
    df.to_csv(arquivo, index=False, mode="w", header=True, encoding="utf-8")
