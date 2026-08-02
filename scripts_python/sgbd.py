"""
Script que cria as tabelas a partir de
'tables.sql' e insere os dados de 'adicionando_dados.sql'.

Antes de criar, apaga (DROP) as tabelas existentes, para que o script possa
ser executado quantas vezes for necessário partindo sempre do zero.
"""

import psycopg2

# Configuração da conexão
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "gestao_hospitalar"
DB_USER = "hospital"
DB_PASSWORD = "hospital"

# Arquivos SQL
ARQUIVO_TABELAS = "scripts_SQL/tables.sql"
ARQUIVO_DADOS = "scripts_SQL/adicionando_dados.sql"
ARQUIVO_TRIGGERS = "scripts_SQL/triggers.sql"

# Todas as tabelas, para o DROP.
TABELAS = [
    "ATENDIMENTO_PROCEDIMENTO",
    "AUDITORIA_ATENDIMENTO",
    "ESCALA_PLANTAO",
    "ATENDIMENTO",
    "INTERNACAO",
    "ALERGIA_PACIENTE",
    "ALERGIA",
    "TELEFONE",
    "RESIDENTE",
    "PRECEPTOR",
    "PROFISSIONAL",
    "PACIENTE",
    "PROCEDIMENTO",
    "UNIDADE",
    "PESSOA",
]


def apagar_tabelas(cursor):
    # Apaga todas as tabelas, se existirem.
    for tabela in TABELAS:
        cursor.execute(f"DROP TABLE IF EXISTS {tabela} CASCADE;")
    print("Tabelas antigas removidas.")


def executar_arquivo_sql(cursor, caminho):
    # Lê um arquivo .sql e executa o seu conteúdo.
    with open(caminho, "r", encoding="utf-8") as arquivo:
        cursor.execute(arquivo.read())
    print(f"Executado: {caminho}")


def main():
    conn = None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        cursor = conn.cursor()

        apagar_tabelas(cursor)
        executar_arquivo_sql(cursor, ARQUIVO_TABELAS)
        executar_arquivo_sql(cursor, ARQUIVO_DADOS)
        executar_arquivo_sql(cursor, ARQUIVO_TRIGGERS)

        conn.commit()
        print("Banco Criado.")
    except Exception as erro:
        print(f"Erro {erro}")
        if conn is not None:
            conn.rollback()
    finally:
        if conn is not None:
            conn.close()


if __name__ == "__main__":
    main()