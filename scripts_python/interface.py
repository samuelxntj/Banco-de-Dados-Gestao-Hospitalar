import streamlit as st
import psycopg2
import pandas as pd


from sgbd import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, TABELAS
from sgbd import apagar_tabelas, executar_arquivo_sql, ARQUIVO_TABELAS, ARQUIVO_DADOS
from consultas import separar_comandos, ARQUIVOS_CONSULTAS


# Configuração da página e conexão com o banco
st.set_page_config(page_title="Gestão Hospitalar", layout="wide", page_icon="🏥")

# cache para não abrir uma nova conexão a cada clique na interface
@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )

try:
    conn = get_connection()
except Exception as e:
    st.error(f"Erro ao conectar no banco de dados: {e}")
    st.stop()


# Funções auxiliares reaproveitadas pelas telas

def executar_e_exibir(conn, sql, bloco_unico=False):
    # Executa o SQL informado e mostra na tela o resultado de cada comando.
    # Com bloco_unico=True o texto inteiro vai num único execute(), o que é
    # necessário para CREATE FUNCTION/PROCEDURE, onde os ';' de dentro do
    # corpo ($$ ... $$) não podem ser usados para separar comandos.
    comandos = [sql] if bloco_unico else separar_comandos(sql)

    if not comandos:
        st.warning("Nenhum comando SQL para executar.")
        return

    try:
        cursor = conn.cursor()
        for numero, comando in enumerate(comandos, 1):
            if len(comandos) > 1:
                st.markdown(f"**[{numero}] {comando.splitlines()[0]}**")

            cursor.execute(comando)

            if cursor.description is not None:  # É um SELECT
                colunas = [desc[0] for desc in cursor.description]
                dados = cursor.fetchall()
                df = pd.DataFrame(dados, columns=colunas)

                st.dataframe(df, use_container_width=True)
                st.success(f"Consulta retornou {len(df)} linha(s).")
            else:  # É um INSERT / UPDATE / DELETE / DDL
                st.success(f"Sucesso! {cursor.rowcount} linha(s) afetada(s).")
        conn.commit()
    except Exception as e:
        conn.rollback()  # Essencial para não travar o banco em caso de erro no SQL
        st.error(f"Erro na transação: {e}")


def tela_consultas(conn, caminho_arquivo, titulo):
    # Monta uma tela a partir de um arquivo .sql: a pessoa escolhe uma consulta,
    # que aparece já preenchida num editor, pode alterá-la e então executá-la.
    st.header(titulo)

    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            sql = arquivo.read()
    except FileNotFoundError:
        st.warning(f"Arquivo '{caminho_arquivo}' não encontrado.")
        return

    comandos = separar_comandos(sql)

    opcoes_comandos = {}
    for i, cmd in enumerate(comandos, 1):
        titulo_cmd = cmd.splitlines()[0]  # Pega o comentário
        opcoes_comandos[f"[{i}] {titulo_cmd}"] = cmd

    selecao = st.selectbox("Escolha uma consulta para rodar:", list(opcoes_comandos.keys()))
    comando_sql = opcoes_comandos[selecao]

    # O SQL do arquivo entra como texto inicial, mas fica editável. A key por
    # arquivo + consulta faz o Streamlit guardar a edição de cada uma
    # separadamente, então trocar de consulta e voltar não perde o que foi escrito.
    chave = f"editor_{caminho_arquivo}_{selecao}"

    # O "Restaurar" da execução anterior é aplicado aqui, antes de criar o campo:
    # apagar a chave faz o text_area voltar ao texto original do arquivo.
    if st.session_state.get("restaurar_editor") == chave:
        st.session_state.pop(chave, None)
        st.session_state.pop("restaurar_editor", None)

    sql_editavel = st.text_area(
        "SQL (edite à vontade antes de executar):",
        value=comando_sql,
        key=chave,
        height=300,
    )

    coluna_executar, coluna_restaurar = st.columns([1, 1])

    with coluna_executar:
        executar = st.button("Executar Script", key=f"btn_exec_{chave}")

    with coluna_restaurar:
        if st.button("Restaurar consulta original", key=f"btn_reset_{chave}"):
            st.session_state["restaurar_editor"] = chave
            st.rerun()

    if executar:
        executar_e_exibir(conn, sql_editavel)


# Interface Principal (Menu Lateral)
st.sidebar.title("🏥 Gestão Hospitalar")
menu = [
    "Visualizar Tabelas",
    "Executar CRUDs e Consultas Básicas",
    "Executar Consultas Analíticas",
    "SQL Livre",
    "RESETAR DATABASE",
]
escolha = st.sidebar.radio("Navegação:", menu)

# Tela 1: Visualizar as Tabelas Livres
if escolha == "Visualizar Tabelas":
    st.header("🔍 Explorar Tabelas do Banco")

    # Usa a lista TABELAS que você já definiu no sgbd.py
    tabela_selecionada = st.selectbox("Selecione uma tabela:", TABELAS)

    if st.button("Carregar Dados"):
        executar_e_exibir(conn, f"SELECT * FROM {tabela_selecionada};")

# Tela 2: Rodar o script CRUD_Consultas.sql dinamicamente
elif escolha == "Executar CRUDs e Consultas Básicas":
    tela_consultas(conn, ARQUIVOS_CONSULTAS[0], "📝 CRUDs e Consultas Básicas")


# Tela 3: Rodar o script consultas_analiticas.sql dinamicamente
elif escolha == "Executar Consultas Analíticas":
    tela_consultas(conn, ARQUIVOS_CONSULTAS[1], "📊 Consultas Analíticas")


# Tela 4: Escrever e rodar qualquer SQL
elif escolha == "SQL Livre":
    st.header("⌨️ SQL Livre")
    st.caption(
        f"Os comandos rodam direto no banco '{DB_NAME}'. Se algo der errado, "
        "a tela 'RESETAR DATABASE' recria tudo do zero."
    )

    sql_livre = st.text_area(
        "Escreva o SQL (SELECT, INSERT, UPDATE, DELETE, DDL...):",
        key="editor_livre",
        height=300,
        placeholder="SELECT * FROM PESSOA;",
    )

    bloco_unico = st.checkbox(
        "Executar como bloco único",
        help="Marque para colar comandos com ';' internos, como "
             "CREATE FUNCTION ... $$ ... $$ LANGUAGE plpgsql;",
    )

    if st.button("Executar", type="primary"):
        if sql_livre.strip():
            executar_e_exibir(conn, sql_livre, bloco_unico=bloco_unico)
        else:
            st.warning("Escreva um comando SQL antes de executar.")


# Tela 5: Resetar o banco de dados via UI
elif escolha == "RESETAR DATABASE":
    st.header("⚠️ Administração")
    st.write("Aqui você pode recriar o banco de dados do zero (Drop, Create e Insert).")

    if st.button("Resetar e Popular Banco de Dados", type="primary"):
        with st.spinner("Executando scripts..."):
            try:
                cursor = conn.cursor()
                apagar_tabelas(cursor)
                executar_arquivo_sql(cursor, ARQUIVO_TABELAS)
                executar_arquivo_sql(cursor, ARQUIVO_DADOS)
                conn.commit()
                st.success("Banco de dados resetado e populado com sucesso!")
                st.balloons()  # Animação do Streamlit para sucesso
            except Exception as e:
                conn.rollback()
                st.error(f"Erro ao resetar o banco: {e}")
