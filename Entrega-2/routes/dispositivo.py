from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from database_config import get_session
from models.dispositivo import Dispositivo
from .responses import DispositivoResponse

# cria a rota para os dispositivos
router = APIRouter(prefix="/dispositivos", tags=["Dispositivos"])

# Cria novo Dispositivo
@router.post("/novo_disp", response_model= DispositivoResponse)
def create_dispositivo(dispositivo: Dispositivo, session: Session = Depends(get_session)):
    #Verifica se já existe um dispositivo com mesmo nome
    dispositivo_exist = session.exec(
        select(Dispositivo).where(Dispositivo.modelo == dispositivo.modelo)).first()
    if dispositivo_exist:
        raise HTTPException(status_code=400, detail="Dispositivo já existente")
    # Adicona o dispositivo
    session.add(dispositivo)
    session.commit()
    session.refresh(dispositivo)
    
    return dispositivo

# Retorna todos os dispositivos
@router.get("/dispositivo", response_model= list[Dispositivo])
def get_all_disp(session: Session = Depends(get_session),
                    offset: int = 0, limit: int = Query(default=5, le=100)):
    # Seleciona todos os dispositivos
    statement = (select(Dispositivo).offset(offset).limit(limit))
    # Execução da consulta
    dispositivos = session.exec(statement).all()

    return dispositivos

# Retorna o Dispositivo procurado por id
@router.get("/{id_disp}", response_model= DispositivoResponse)
def get_dispositivo_by_id(id_disp: int, session: Session = Depends(get_session),
                    offset: int = 0, limit: int = Query(default=5, le=100)):
    # Consulta por dispositivo
    statement = (select(Dispositivo).options(joinedload(Dispositivo.servicos)).where(Dispositivo.id == id_disp).offset(offset).limit(limit))
    # Execução da consulta
    dispositivo = session.exec(statement).first()

    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")
    return dispositivo

# Retorna o Dispositivo procurado por modelo
@router.get("/model/{model_disp}", response_model= list[DispositivoResponse])
def get_dispositivo_by_model(model_disp: str, session: Session = Depends(get_session),
                            offset: int = 0, limit: int = Query(default=5, le=100)):
    # Consulta
    statement = (select(Dispositivo).offset(offset).limit(limit).where(Dispositivo.modelo.like(f'{model_disp}%')))
    # Execução da consulta
    dispositivo = session.exec(statement).all()

    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")
    return dispositivo

# Lista os serviços relizados em um dispositivo
@router.get("/dispositivos/{dispositivo_id}/servicos", response_model= DispositivoResponse)
def listar_servicos_dispositivo(dispositivo_id: int, session: Session = Depends(get_session)):
    # Consulta
    dispositivo = session.get(Dispositivo, dispositivo_id)
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")
    return dispositivo.servicos

# Atualiza os dados de um Dispositivo existente
@router.put("/{id_disp}", response_model=DispositivoResponse)
def update_disp(id_disp: int, dispositivo_atualizado: Dispositivo, session: Session = Depends(get_session)):
    dispositivo = session.exec(
        select(Dispositivo).where(Dispositivo.id == id_disp)
    ).first()

    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")

    # Atualiza os campos
    for key, value in dispositivo_atualizado.dict(exclude_unset= True).items():
        setattr(dispositivo, key, value)
           
    session.add(dispositivo)
    session.commit()
    session.refresh(dispositivo)

    return dispositivo
# Deleta um dispositivo do banco
@router.delete("/{id_disp}")
def delete_disp(id_disp: int, session: Session = Depends(get_session)):
    dispositivo = session.get(Dispositivo, id_disp)
    if not dispositivo:
        raise HTTPException(status_code=404, detail="Dispositivo não encontrado")
    # Deleta o dispositivo do bd
    session.delete(dispositivo)
    session.commit()
    return {"msg":"registro apagado com sucesso"}