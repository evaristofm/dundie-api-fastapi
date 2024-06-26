from datetime import datetime
from typing import List
from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select

from prev.routes import crud
from prev.utils import calcula_data_carencia
from prev.db import ActiveSession
from prev.models.user import Resgate
from prev.serializers import ResgateRequest, ResgateIdResponse



router = APIRouter()


@router.get("/", response_model=List[ResgateRequest])
async def get_resgate_all(*, session: Session = ActiveSession):
    """Lista regates."""
    aportes = session.exec(select(Resgate)).all()
    return aportes


@router.post("/", response_model=ResgateIdResponse, status_code=status.HTTP_201_CREATED)
async def create_resgate(*, session: Session = ActiveSession, resgate_request: ResgateRequest):
    """Criar novos resgates"""

    db_plano = crud.get_plano(db=session, plano_id=resgate_request.idPlano)
    db_produto = crud.get_produto(db=session, producto_id=db_plano.idProduto)

    if not db_plano:
        raise HTTPException(status_code=404, detail="Plano não encontrado")

    data_atual = datetime.now()
    dias_diferenca = calcula_data_carencia(db_plano.dataDaContratacao, data_atual)

    if dias_diferenca < db_produto.carenciaInicialDeResgate:
        return dias_diferenca

    if db_plano.aporte < resgate_request.valorResgate:
        raise HTTPException(status_code=400, detail="Saldo insuficiente para resgate.")

    db_plano.aporte -= resgate_request.valorResgate

    if db_plano.aporte == 0:
        session.delete(db_plano)
    
    db_resgate = crud.create_resgate(db=session, resgate=resgate_request)
    
    session.commit()
    session.refresh(db_plano)

    return db_resgate

