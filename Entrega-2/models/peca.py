from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING
from .tecnico_servico import Servico, ServicoPeca

class Peca(SQLModel, table=True):
    __tablename__ = 'pecas'
    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(max_length=100, description="Nome da peça")
    fabricante: str = Field(max_length=100, description="Fabricante da peça")
    servicos: list["Servico"] = Relationship(back_populates="pecas", link_model=ServicoPeca)