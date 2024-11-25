import zipfile

# Função que compacta o arquivo CSV em ZIP
def compactar_csv():
    arq_zip = "dispositivos.zip"
    with zipfile.ZipFile(arq_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write("dispositivos.csv", arcname="dispositivos.csv")
    return arq_zip