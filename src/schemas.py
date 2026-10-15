from pydantic import BaseModel


class ValidarRequest(BaseModel):
    cartao_id: int


class ValidarResponse(BaseModel):
    liberado: bool
    motivo: str
    mensagem: str
    nome: str | None = None
    saldo_restante: float | None = None