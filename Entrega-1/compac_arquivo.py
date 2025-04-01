import zipfile
from fastapi.responses import FileResponse

def compactar_csv(arq_disp):
    """Compacta arquivos e comprime transformando em arquivo zip.
    Args:
        
    Return:
        retorna um arquivo zip.
    """
    arq_zip = "dispositivos.zip"
    with zipfile.ZipFile(arq_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(arq_disp, arcname="dispositivos_test.csv")
    return FileResponse(arq_zip, media_type="application/zip", filename="dispositivos.zip")