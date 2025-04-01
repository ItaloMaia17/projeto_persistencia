from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from database_config import get_session
from models.peca import Peca
from .responses import PecaResponse


# cria a rota para as Pecas
router = APIRouter(prefix="/Pecas", tags=["Peças"])

# Cria nova peça
@router.post("/peca", response_model= PecaResponse)
def create_peca(peca: Peca, session: Session = Depends(get_session)):
    #Verifica se ja existe uma peça com mesmo nome
    peca_exist = session.exec(select(Peca).where(Peca.nome == peca.nome)).first()
    if peca_exist:
        raise HTTPException(status_code=400, detail="Peca já existente")
    # Adicona a peça
    session.add(peca)
    session.commit()
    session.refresh(peca)
    
    return peca

# Retorna todas as Pecas
@router.get("/peca", response_model= list[Peca])
def get_all_pecas(session: Session = Depends(get_session),
                    offset: int = 0, limit: int = Query(default=5, le=100)):
    # seleciona todas as Pecas
    statement = (select(Peca).offset(offset).limit(limit))
    # Execução da consulta
    pecas = session.exec(statement).all()

    return pecas

# Retorna a peça procurada por id
@router.get("/{id_peca}", response_model= PecaResponse)
def get_peca_by_id(id_peca: int, session: Session = Depends(get_session),
                    offset: int = 0, limit: int = Query(default=5, le=100)):
    # Consulta
    statement = (select(Peca).options(joinedload(Peca.servicos)).where(Peca.id == id_peca).offset(offset).limit(limit))
    # Execução da consulta
    peca = session.exec(statement).first()

    if not peca:
        raise HTTPException(status_code=404, detail="Peca não encontrada")
    return peca

# Retorna a peça procurada por nome
@router.get("/nome_peca/{nome_peca}", response_model= list[PecaResponse])
def get_peca_by_name(nome_peca: str, session: Session = Depends(get_session),
                            offset: int = 0, limit: int = Query(default=5, le=100)):
    # Consulta
    statement = (select(Peca).offset(offset).limit(limit).where(Peca.nome.like(f'{nome_peca}%')))
    # Execução da consulta
    peca = session.exec(statement).all()

    if not peca:
        raise HTTPException(status_code=404, detail="Peca não encontrada")
    return peca

# Atualiza as dados de uma Peca existente
@router.put("/{id_peca}", response_model=PecaResponse)
def update_peca(id_peca: int, peca_atualizado: Peca, session: Session = Depends(get_session)):
    peca = session.exec(
        select(Peca).where(Peca.id == id_peca)
    ).first()

    if not peca:
        raise HTTPException(status_code=404, detail="Peca não encontrada")

    # Atualiza os campos
    for key, value in peca_atualizado.dict(exclude_unset= True).items():
        setattr(peca, key, value)
           
    session.add(peca)
    session.commit()
    session.refresh(peca)

    return peca
# Deleta uma peça do banco
@router.delete("/{id_peca}")
def delete_peca(id_peca: int, session: Session = Depends(get_session)):
    peca = session.get(Peca, id_peca)
    if not peca:
        raise HTTPException(status_code=404, detail="Peca não encontrada")
    session.delete(peca)
    session.commit()
    return {"msg":"registro apagado com sucesso"}