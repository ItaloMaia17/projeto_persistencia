from sqlmodel import SQLModel, Field, Relationship
from .tecnico_servico import Servico
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .tecnico_servico import Servico


class Dispositivo(SQLModel, table=True):
    __tablename__ = 'dispositivos'
    id: int | None = Field(default=None, primary_key=True)
    modelo: str = Field(max_length=100, description="Modelo do dispositivo")
    tipo: str = Field(max_length=50, description="Tipo do dispositivo")
    fabricante: str = Field(max_length=50, description="Fabricante do dispositivo")
    servicos: list["Servico"] = Relationship(back_populates="dispositivo")