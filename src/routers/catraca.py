from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..config import TARIFA
from ..database import get_db
from ..models import Cartao, Viagem
from ..schemas import ValidarRequest, ValidarResponse

router = APIRouter(prefix="/catraca", tags=["catraca"])


def recusar(motivo, mensagem, nome=None, saldo=None):
    return ValidarResponse(
        liberado=False,
        motivo=motivo,
        mensagem=mensagem,
        nome=nome,
        saldo_restante=saldo,
    )


@router.post("/validar", response_model=ValidarResponse)
def validar(dados: ValidarRequest, db: Session = Depends(get_db)):
    cartao = db.execute(
        select(Cartao).where(Cartao.id == dados.cartao_id).with_for_update()
    ).scalar_one_or_none()

    if cartao is None:
        return recusar("cartao_nao_encontrado", "Cartão não encontrado")

    usuario = cartao.usuario
    saldo_atual = float(cartao.saldo)

    if cartao.status != "ativo":
        return recusar("cartao_bloqueado", "Cartão bloqueado", usuario.nome, saldo_atual)

    if not usuario.ativo:
        return recusar("usuario_inativo", "Usuário inativo", usuario.nome, saldo_atual)

    if cartao.saldo < TARIFA:
        return recusar("saldo_insuficiente", "Saldo insuficiente", usuario.nome, saldo_atual)

    cartao.saldo -= TARIFA
    db.add(Viagem(cartao_id=cartao.id, valor_cobrado=TARIFA))
    db.commit()

    return ValidarResponse(
        liberado=True,
        motivo="ok",
        mensagem="Passagem liberada",
        nome=usuario.nome,
        saldo_restante=float(cartao.saldo),
    )