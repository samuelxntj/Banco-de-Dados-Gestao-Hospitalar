from datetime import datetime

from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from bd import SessionLocal


"""
Sobre registrar_atendimento_completo(): recebe dados do atendimento + lista de 
procedimentos realizados (como JSON ou tabela temporária) e insere tudo dentro de 
uma transação (se qualquer procedimento falhar, tudo é revertido).
"""
def registrar_atendimento_completo(
    data_hora,
    duracao_minutos,
    id_paciente,
    id_residente,
    dt_inicio_residente,
    id_preceptor,
    dt_inicio_preceptor,
    id_unidade,
    procedimentos,
):
    try:
        with SessionLocal() as session:

            # se falhar, a transação é revertida automaticamente
            with session.begin():
                resultado = session.execute(
                    text("""
                        INSERT INTO atendimento (
                            data_hora,
                            duracao_minutos,
                            id_paciente,
                            id_residente,
                            dt_inicio_residente,
                            id_preceptor,
                            dt_inicio_preceptor,
                            id_unidade
                        )
                        VALUES (
                            :data_hora,
                            :duracao_minutos,
                            :id_paciente,
                            :id_residente,
                            :dt_inicio_residente,
                            :id_preceptor,
                            :dt_inicio_preceptor,
                            :id_unidade
                        )
                        RETURNING id_atendimento
                    """),
                    {
                        "data_hora": data_hora,
                        "duracao_minutos": duracao_minutos,
                        "id_paciente": id_paciente,
                        "id_residente": id_residente,
                        "dt_inicio_residente": dt_inicio_residente,
                        "id_preceptor": id_preceptor,
                        "dt_inicio_preceptor": dt_inicio_preceptor,
                        "id_unidade": id_unidade,
                    },
                )

                id_atendimento = resultado.scalar_one()

                for procedimento in procedimentos:
                    session.execute(
                        text("""
                            INSERT INTO atendimento_procedimento (
                                id_atendimento,
                                id_procedimento,
                                qtd_executada,
                                tempo_real_gasto,
                                observacao_intercorrencias,
                                dt_hora_inicio,
                                is_faturado
                            )
                            VALUES (
                                :id_atendimento,
                                :id_procedimento,
                                :qtd_executada,
                                :tempo_real_gasto,
                                :observacao_intercorrencias,
                                :dt_hora_inicio,
                                :is_faturado
                            )
                        """),
                        {
                            "id_atendimento": id_atendimento,
                            "id_procedimento": procedimento["id_procedimento"],
                            "qtd_executada": procedimento.get("qtd_executada", 1),
                            "tempo_real_gasto": procedimento["tempo_real_gasto"],
                            "observacao_intercorrencias": procedimento.get("observacao_intercorrencias"),
                            "dt_hora_inicio": procedimento["dt_hora_inicio"],
                            "is_faturado": procedimento.get("is_faturado", False),
                        },
                    )

        return id_atendimento

    except SQLAlchemyError as erro:
        raise RuntimeError("Não foi possível registrar o atendimento completo.") from erro


"""
Sobre calcular_tempo_medio_espera(): calcula, para cada unidade, o tempo médio 
entre a chegada do paciente (data_hora do atendimento) e o início do primeiro 
procedimento.
"""


def calcular_tempo_medio_espera():
    try:
        with SessionLocal() as session:
            result = session.execute(text("""
                WITH primeiro_procedimento AS (
                    SELECT a.id_atendimento, a.data_hora, a.id_unidade, MIN(ap.dt_hora_inicio) AS dt_hora_primeiro_procedimento
                    FROM atendimento a
                    INNER JOIN atendimento_procedimento ap ON a.id_atendimento = ap.id_atendimento
                    GROUP BY a.id_atendimento, a.data_hora, a.id_unidade
                )

                SELECT u.nome AS unidade, AVG(EXTRACT(EPOCH FROM (pp.dt_hora_primeiro_procedimento - pp.data_hora)) / 60) AS tempo_medio_espera_minutos
                FROM primeiro_procedimento pp
                INNER JOIN unidade u ON pp.id_unidade = u.id_unidade
                GROUP BY u.nome;
            """))

        return result.fetchall()

    except SQLAlchemyError as erro:
        raise RuntimeError("Não foi possível calcular o tempo médio de espera.") from erro



"""
Sobre reajustar_escala():  recebe um id_residente, muda todas as suas escalas de um 
dia/turno para outro, desde que não gere conflito (mesmo 
unidade+dia+turno+residente).
"""

""" |================= AINDA FAZENDO =================|
def reajustar_escala(id_residente, dia_atual, turno_atual, novo_dia, novo_turno):
    try:
        pass


    except SQLAlchemyError as erro:
        raise RuntimeError("Não foi possível reajustar a escala.") from erro 
"""