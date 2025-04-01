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