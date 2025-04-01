import hashlib

# gerando hash do arquivo csv
def gerar_hash(arquivo_disp):
    # abre o arquivo csv como um arquivo binário
    with open(arquivo_disp, "rb") as f:
        # lê o arquivo
        dados_arq = f.read()
        # cria um objeto hash
        hash_result = hashlib.sha256(dados_arq).hexdigest()
        return hash_result
