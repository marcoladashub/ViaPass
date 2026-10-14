from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    ativo: Mapped[bool] = mapped_column(Boolean, default=True)

    cartoes: Mapped[list["Cartao"]] = relationship(back_populates="usuario")


class Cartao(Base):
    __tablename__ = "cartoes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    saldo: Mapped[float] = mapped_column(Numeric(10, 2), default=0)
    status: Mapped[str] = mapped_column(String(20), default="ativo")

    usuario: Mapped["Usuario"] = relationship(back_populates="cartoes")
    viagens: Mapped[list["Viagem"]] = relationship(back_populates="cartao")
    recargas: Mapped[list["Recarga"]] = relationship(back_populates="cartao")


class Viagem(Base):
    __tablename__ = "viagens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cartao_id: Mapped[int] = mapped_column(ForeignKey("cartoes.id"))
    valor_cobrado: Mapped[float] = mapped_column(Numeric(10, 2))
    data_hora: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    cartao: Mapped["Cartao"] = relationship(back_populates="viagens")


class Recarga(Base):
    __tablename__ = "recargas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    cartao_id: Mapped[int] = mapped_column(ForeignKey("cartoes.id"))
    valor: Mapped[float] = mapped_column(Numeric(10, 2))
    data_hora: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    cartao: Mapped["Cartao"] = relationship(back_populates="recargas")