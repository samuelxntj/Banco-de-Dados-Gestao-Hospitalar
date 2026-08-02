import psycopg2

conn = psycopg2.connect(host='localhost', port='5432', dbname='gestao_hospitalar', user='hospital', password='hospital')
cur = conn.cursor()

try:
    cur.execute('BEGIN')

    try:
        cur.execute("""
            INSERT INTO ESCALA_PLANTAO (
                dia_semana, turno, id_unidade, id_residente, dt_inicio_residente, id_preceptor, dt_inicio_preceptor
            )
            VALUES ('SEGUNDA', 'MANHA', 2, 6, '2026-03-01 00:00:00', 11, '2015-01-01 00:00:00')
        """)
    except Exception as e:
        print('sobreposicao_ok', type(e).__name__, str(e))
    else:
        print('sobreposicao_erro', 'inserção permitida')

    cur.execute("""
        INSERT INTO ATENDIMENTO (
            data_hora, duracao_minutos, id_paciente, id_residente,
            dt_inicio_residente, id_preceptor, dt_inicio_preceptor, id_unidade
        )
        VALUES ('2026-08-02 12:00:00', 20, 1, 6, '2026-03-01 00:00:00', 11, '2015-01-01 00:00:00', 1)
        RETURNING id_atendimento
    """)
    atendimento_id = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM AUDITORIA_ATENDIMENTO WHERE id_atendimento = %s", (atendimento_id,))
    print('auditoria_count', cur.fetchone()[0])

    cur.execute("""
        INSERT INTO ATENDIMENTO_PROCEDIMENTO (
            id_atendimento, id_procedimento, qtd_executada, tempo_real_gasto,
            observacao_intercorrencias, dt_hora_inicio, is_faturado
        )
        VALUES (%s, 1, 1, 18, 'teste trigger', '2026-08-02 12:05:00', FALSE)
    """, (atendimento_id,))
    cur.execute("SELECT media_tempo_procedimento FROM PROCEDIMENTO WHERE id_procedimento = 1")
    print('media_procedimento', cur.fetchone()[0])
finally:
    cur.execute('ROLLBACK')
    conn.close()
