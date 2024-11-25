import hashlib

# gerando hash do arquivo csv
def gerar_hash():
    # abre o arquivo csv como um arquivo binário
    with open("dispositivos.csv", "rb") as f:
        # lê o arquivo
        dados_arq = f.read()
        # cria um objeto hash
        hash_disp = hashlib.sha256(dados_arq).hexdigest()
        return hash_disp
