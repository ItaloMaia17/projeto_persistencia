from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .dispositivo import Dispositivo
    from .peca import Peca


class ServicoPeca(SQLModel, table=True):
    __tablename__ = 'servicos_pecas'
    servico_id: int = Field(foreign_key="servicos.id", primary_key=True)
    peca_id: int = Field(foreign_key="pecas.id", primary_key=True)
    quantidade: int = Field(default=1, description="Quantidade de peças usadas no serviço")


class Tecnico(SQLModel, table=True):
    __tablename__ = 'tecnicos'
    id: int | None = Field(default=None, primary_key=True)
    nome: str = Field(max_length=100, description="Nome do técnico")
    especialidade: str = Field(max_length=50, description="Especialidade do técnico")
    contato: str = Field(max_length=50, description="Contato do técnico (telefone ou e-mail)")
    salario: float = Field(description="Salário do técnico")
    servicos: list["Servico"] = Relationship(back_populates="tecnico")

class CreateServico(BaseModel):
    tipo_de_servico: str
    descricao: str
    valor: float
    dispositivo_id: int
    tecnico_id: int
    pecas_ids: list[int]

class Servico(SQLModel, table=True):
    __tablename__ = 'servicos'
    id: int | None = Field(default=None, primary_key=True)
    tipo_de_servico: str = Field(max_length=100, description="Tipo do serviço")
    descricao: str = Field(default=None, max_length=255, description="Descrição detalhada do serviço")
    valor: float = Field(description="Preço do serviço")
    cadastrado_em: datetime | None = Field(default_factory=lambda: datetime.now(timezone.utc).date(), description="Data e hora do cadastro do serviço")

    dispositivo_id: int = Field(foreign_key="dispositivos.id", description="ID do dispositivo relacionado")
    dispositivo: "Dispositivo" = Relationship(back_populates="servicos")

    tecnico_id: int = Field(foreign_key="tecnicos.id", description="ID do técnico responsável pelo serviço")
    tecnico: "Tecnico" = Relationship(back_populates="servicos")

    pecas: list["Peca"] = Relationship(back_populates="servicos", link_model=ServicoPeca)



