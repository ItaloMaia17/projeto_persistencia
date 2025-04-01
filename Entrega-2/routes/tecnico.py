from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from database_config import get_session
from models.tecnico_servico import Tecnico, Servico
from .responses import TecnicoResponse

# cria a rota para os tecnicos
router = APIRouter(prefix="/tecnicos", tags=["Técnicos"])

# Cria nova peça
@router.post("/tecnico", response_model= TecnicoResponse)
def create_tecnico(tecnico: Tecnico, session: Session = Depends(get_session)):
    #Verifica se ja existe um técnico com mesmo nome
    tecnico_exist = session.exec(
        select(Tecnico).where(Tecnico.nome == tecnico.nome)).first()
    if tecnico_exist:
        raise HTTPException(status_code=400, detail="Tecnico já existente")
    # Adicona a peça
    session.add(tecnico)
    session.commit()
    session.refresh(tecnico)
    
    return tecnico

# Retorna todos os técnicos
@router.get("/tecnico", response_model= list[Tecnico])
def get_all_tecnicos(session: Session = Depends(get_session),
                    offset: int = 0, limit: int = Query(default=5, le=100)):
    # Seleciona todos os técnicos
    statement = (select(Tecnico).offset(offset).limit(limit))
    # Execução da consulta
    tecnicos = session.exec(statement).all()

    return tecnicos

# Retorna a peça procurado por id
@router.get("/{id_tecnico}", response_model= TecnicoResponse)
def get_tecnico_by_id(id_tecnico: int, session: Session = Depends(get_session),
                    offset: int = 0, limit: int = Query(default=5, le=100)):
    # Consulta
    statement = (select(Tecnico).offset(offset).limit(limit).where(Tecnico.id == id_tecnico))
    # Execução da consulta
    tecnico = session.exec(statement).first()

    if not tecnico:
        raise HTTPException(status_code=404, detail="Técnico não encontrado")
    return tecnico

# Retorna o técnico procurado por nome
@router.get("/nome_tecnico/{nome_tecnico}", response_model= list[Tecnico])
def get_tecnico_by_name(nome_tecnico: str, session: Session = Depends(get_session),
                            offset: int = 0, limit: int = Query(default=5, le=100)):
    # Consulta
    statement = (select(Tecnico).offset(offset).limit(limit).where(Tecnico.nome.like(f'{nome_tecnico}%')))
    # Execução da consulta
    tecnico = session.exec(statement).all()

    if not tecnico:
        raise HTTPException(status_code=404, detail="Técnico não encontrado")
    return tecnico

# Lista todos os serviços realizados por um técnico
@router.get("/tecnicos/{tecnico_id}/servicos", response_model= TecnicoResponse)
def listar_servicos_tecnico(tecnico_id: int, session: Session = Depends(get_session)):
    # Consulta
    tecnico = session.get(Tecnico, tecnico_id)
    if not tecnico:
        raise HTTPException(status_code=404, detail="Técnico não encontrado")
    return tecnico

# Conta a quantidade de serviços realizados por um técnico
@router.get("/tecnicos/{tecnico_id}/servicos/cont_services")
def contar_servicos_tecnico(tecnico_id: int, session: Session = Depends(get_session)):
    # Conta todos os serviços associados a um tecnico
    statement = select(func.count(Servico.id)).where(Servico.tecnico_id == tecnico_id)
    result = session.execute(statement).scalar()
    # count = result[0]
    return {"tecnico_id": tecnico_id, "quantidade_servicos": result}

# Atualiza os dados de um Técnico existente
@router.put("/{id_tecnico}", response_model=TecnicoResponse)
def update_tecnico(id_tecnico: int, tecnico_atualizado: Tecnico, session: Session = Depends(get_session)):
    tecnico = session.exec(
        select(Tecnico).where(Tecnico.id == id_tecnico)
    ).first()

    if not tecnico:
        raise HTTPException(status_code=404, detail="Técnico não encontrado")

    # Atualiza os campos
    for key, value in tecnico_atualizado.dict(exclude_unset= True).items():
        setattr(tecnico, key, value)
           
    session.add(tecnico)
    session.commit()
    session.refresh(tecnico)

    return tecnico
# Deleta um técnico do banco
@router.delete("/{id_tecnico}")
def delete_tecnico(id_tecnico: int, session: Session = Depends(get_session)):
    tecnico = session.get(Tecnico, id_tecnico)
    if not tecnico:
        raise HTTPException(status_code=404, detail="Técnico não encontrado")
    # Deleta registro do tecnico do bd
    session.delete(tecnico)
    session.commit()
    return {"msg":"registro apagado com sucesso"}