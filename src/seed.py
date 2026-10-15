from .database import Base, SessionLocal, engine
from .models import Cartao, Usuario


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(Usuario).count() > 0:
            print("Banco já tem dados, nada foi feito.")
            return

        ana = Usuario(nome="Ana", ativo=True)
        bruno = Usuario(nome="Bruno", ativo=True)
        carla = Usuario(nome="Carla", ativo=True)
        diego = Usuario(nome="Diego", ativo=False)
        db.add_all([ana, bruno, carla, diego])
        db.flush()

        db.add_all([
            Cartao(usuario_id=ana.id, saldo=20.00, status="ativo"),
            Cartao(usuario_id=bruno.id, saldo=1.00, status="ativo"),
            Cartao(usuario_id=carla.id, saldo=15.00, status="bloqueado"),
            Cartao(usuario_id=diego.id, saldo=10.00, status="ativo"),
        ])
        db.commit()
        print("Dados de teste criados.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()