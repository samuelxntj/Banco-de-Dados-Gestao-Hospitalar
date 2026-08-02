from sqlalchemy import text

from bd import SessionLocal


def main():
    try:
        with SessionLocal() as session:
            resultado = session.scalar(text("SELECT 1"))
            banco = session.scalar(text("SELECT current_database()"))
            usuario = session.scalar(text("SELECT current_user"))

        print("Conexão realizada com sucesso!")
        print(f"SELECT 1: {resultado}")
        print(f"Banco: {banco}")
        print(f"Usuário: {usuario}")

    except Exception as erro:
        print(f"Erro ao conectar: {erro}")


if __name__ == "__main__":
    main()