"""Configuração central do SQLAlchemy para o PostgreSQL do projeto."""

import os

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from sgbd import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


# A conexão pode vir do ambiente, para não gravar usuário e senha em disco.
# Se a variável não estiver definida, cai nas mesmas constantes usadas pelos
# scripts em SQL puro (sgbd.py), para não exigir configuração extra do time.
DATABASE_URL = os.environ.get("DATABASE_URL") or (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
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
