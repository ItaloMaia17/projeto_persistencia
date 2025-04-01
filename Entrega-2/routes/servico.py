from fastapi import APIRouter, HTTPException, Depends, Query
from sqlmodel import Session, select
from sqlalchemy.orm import joinedload
from database_config import get_session
from models.tecnico_servico import Servico, ServicoPeca, Tecnico, CreateServico
from .responses import ServicoResponse
from datetime import datetime

# cria a rota para os Servicos
router = APIRouter(prefix="/servicos", tags=["Serviços"])

# Cria novo Servico
@router.post("/servico", response_model= ServicoResponse)
def create_servico(servico_create: CreateServico, session: Session = Depends(get_session)):
    # Adicona o Servico
    # Criação do serviço
    servico = Servico(**servico_create.dict(exclude={"pecas_ids"}))
    session.add(servico)
    session.commit()
    session.refresh(servico)

    # Preenchendo a tabela associativa (ServicoPeca)
    for peca_id in servico_create.pecas_ids:
        servico_peca = ServicoPeca(servico_id=servico.id, peca_id=peca_id)
        session.add(servico_peca)

    session.commit()
    
    return servico

# Retorna todos os Servicos
@router.get("/servico", response_model= list[Servico])
def get_all_servicos(session: Session = Depends(get_session),
                    offset: int = 0, limit: int = Query(default=5, le=100)):
    # Seleciona todos os serviços
    statement = (select(Servico).offset(offset).limit(limit))
    # Execução da consulta
    servicos = session.exec(statement).all()

    return servicos

# Retorna o Serviço procurado por id
@router.get("/{servico_id}", response_model= ServicoResponse)
def get_servico_by_id(servico_id: int, session: Session = Depends(get_session),
                    offset: int = 0, limit: int = Query(default=5, le=100)):
    # Consulta por Serviço
    statement = (select(Servico).options(joinedload(Servico.dispositivo),joinedload(Servico.tecnico),joinedload(Servico.pecas)).where(Servico.id == servico_id).offset(offset).limit(limit))
    # Execução da consulta
    servico = session.exec(statement).first()

    if not servico:
        raise HTTPException(status_code=404, detail="Servico não encontrado")
    
    return servico

# Retorna o serviço procurando por tipo
@router.get("/tipo/{tipo_servico}", response_model= list[ServicoResponse])
def get_servico_by_typ(tipo_servico: str, session: Session = Depends(get_session),
                            offset: int = 0, limit: int = Query(default=5, le=100)):
    # Consulta
    statement = (select(Servico).offset(offset).limit(limit).where(Servico.tipo_de_servico.like(f'{tipo_servico}%')))
    # Execução da consulta
    servico = session.exec(statement).all()

    if not servico:
        raise HTTPException(status_code=404, detail="Servico não encontrado")
    return servico

# Procura por serviços realizados em um intervalo de tempo
@router.get("/servicos/ano/{ano}", response_model= list[Servico])
def listar_servicos_por_ano(dia_inicio: int,  mes_inicio: int, ano_inicio: int, dia_final: int, mes_final: int, ano_final: int, session: Session = Depends(get_session)):
    # Criar objetos datetime para o intervalo
    data_inicio = datetime(ano_inicio, mes_inicio, dia_inicio)
    data_final = datetime(ano_final, mes_final, dia_final)
    # Consulta
    statement = select(Servico).where(Servico.cadastrado_em.between(data_inicio, data_final))
    result = session.exec(statement).all()

    if not result:
        raise HTTPException(status_code=404, detail="Servico não encontrado ou data utilizada errada")
    
    return result

# Retorna a lista de serviços baseado no preço(ordem crescente ou decrescente)
@router.get("/servicos/ordenados/", response_model= list[Servico])
def lista_servicos_ordenados(ordem: str = "desc", db: Session = Depends(get_session)):
    if ordem == "desc":
        statement = select(Servico).order_by(Servico.valor.desc())
    else:
        statement = select(Servico).order_by(Servico.valor.asc())
    resultados = db.exec(statement).all()
    if not resultados:
        raise HTTPException(status_code=404, detail="Servicos não encontrados")
    return resultados

# Consulta por dispositivo e peca
@router.get("/servicos/consulta_esp_peca/", response_model= ServicoResponse)
def servicos_por_especialidade_e_peca(especialidade: str, peca_id: int, db: Session = Depends(get_session)):
    consult = (
        select(Servico).options(joinedload(Servico.dispositivo),joinedload(Servico.pecas)).where(Tecnico.especialidade == especialidade).where(ServicoPeca.peca_id == peca_id)
    )
    result = db.exec(consult).first()
    return result

# Atualiza os dados de um Servico existente
@router.put("/{id_servico}", response_model=ServicoResponse)
def update_servico(id_servico: int, servico_atualizado: Servico, session: Session = Depends(get_session)):
    servico = session.exec(
        select(Servico).where(Servico.id == id_servico)
    ).first()

    if not servico:
        raise HTTPException(status_code=404, detail="Servico não encontrado")

    # Atualiza os campos
    for key, value in servico_atualizado.dict(exclude_unset= True).items():
        setattr(servico, key, value)
           
    session.add(servico)
    session.commit()
    session.refresh(servico)

    return servico
# Deleta um Servico do banco
@router.delete("/{id_servico}")
def delete_servico(id_servico: int, session: Session = Depends(get_session)):
    servico = session.get(Servico, id_servico)
    if not servico:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    # Deleta o Servico do bd
    session.delete(servico)
    session.commit()
    return {"msg":"registro apagado com sucesso"}