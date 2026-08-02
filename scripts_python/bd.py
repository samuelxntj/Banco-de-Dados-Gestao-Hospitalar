"""Configuração central do SQLAlchemy para o PostgreSQL do projeto."""

import os

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker


# A conexão fica no ambiente para não gravar usuário e senha.
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    # mensagem de erro
    raise RuntimeError(
        "A variável DATABASE_URL não foi definida. "
        "Use uma URL no formato "
        "postgresql+psycopg2://usuario:senha@localhost:5432/banco."
    )


# administra o acesso ao PostgreSQL e o conjunto de conexões reutilizáveis:
engine: Engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    echo=False,
)


# Cada operação da aplicação deve criar sua própria Session por esta fábrica:
SessionLocal: sessionmaker[Session] = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
