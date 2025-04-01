from pydantic import BaseModel
from datetime import datetime

class SimpleDispositivo(BaseModel):
    id: int
    modelo: str
    tipo: str
    fabricante: str 
class DispositivoResponse(SimpleDispositivo):

    servicos: list["SimpleServico"] | None

class SimpleTecnico(BaseModel):
    id: int
    nome: str
    especialidade: str
    contato: str
    salario: float

class TecnicoResponse(SimpleTecnico):
    servicos: list["SimpleServico"] | None

class SimplePeca(BaseModel):
    id: int
    nome: str
    fabricante: str

class PecaResponse(SimplePeca):
    servicos: list["SimpleServico"] | None

class SimpleServico(BaseModel):
    id: int
    tipo_de_servico: str
    descricao: str
    valor: float
    cadastrado_em: datetime

class ServicoResponse(SimpleServico): 
    dispositivo: SimpleDispositivo
    tecnico: SimpleTecnico
    pecas: list[SimplePeca]

