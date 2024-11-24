# import pandas as pd
from pydantic import BaseModel
# import csv

# Definindo a classe Dispositivo
class Dispositivo(BaseModel):
    id: int
    marca: str
    modelo: str
    tipo: str
    ano_fabricacao: int
    preco: float

def __init__(self, id, marca, modelo, tipo, ano_fabricacao, preco):
    self.id = id
    self.marca = marca
    self.modelo = modelo
    self.tipo = tipo
    self.ano_fabricacao = ano_fabricacao
    self.preco = preco

# dispositivos = [
#     Dispositivo(1, "Redmi", "Note 13 pro", "Smartphone", 2024, 1389.99),
#     Dispositivo(2, "Lenovo", "LOQ", "Notebook", 2024, 4559.80),
#     Dispositivo(3, "Samsumg", "Galaxy tab A9", "Tablet", 2020, 997.00),
#     Dispositivo(4, "LG", "UltraGear 24in", "Monitor", 2024, 1019.51),
#     Dispositivo(5, "Xiaomi", "Mi band 8", "smartband", 2023, 328.60),
#     Dispositivo(6, "Samsumg", "A05s", "Smartphone", 2024 , 789.01),
#     Dispositivo(7, "Sony", "PlayStation 5 slim", "VideoGame", 2020 , 2999.00),
#     Dispositivo(8, "Dell", "inspiron 15 i7-1255U", "Noteboook", 2022 , 4199.00 ),
#     Dispositivo(9, "apple", "iphone 13 pro ", "Smartphone", 2021 , 3499.00),
#     Dispositivo(10, "Nitendo", "Switch Oled", "VideoGame", 2022 , 2069.01),
# ]

# # Nome do arquivo CSV
# arquivo_csv = "dispositivos.csv"

# # Salvando os dados em um arquivo CSV
# with open(arquivo_csv, mode="w", newline="", encoding="utf-8") as file:
#     writer = csv.writer(file)
#     # Cabeçalhos
#     writer.writerow(["ID", "Marca", "Modelo", "Tipo",  "Ano de Fabricação"])
#     # # Dados dos dispositivos
#     # for dispositivo in dispositivos:
#     #     writer.writerow([
#     #         dispositivo.id,
#     #         dispositivo.marca,
#     #         dispositivo.modelo,
#     #         dispositivo.tipo,
#     #         dispositivo.ano_lancamento,
#     #     ])

# print(f"Arquivo '{arquivo_csv}' criado com sucesso!")
