
-- Inserir um novo atendimento (verificando se paciente, residente, preceptor existem)
INSERT INTO ATENDIMENTO (
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
    TIMESTAMP '2026-07-07 08:30:00',
    45,
    (
      SELECT pa.id_pessoa
      FROM PACIENTE pa
      INNER JOIN PESSOA pes ON pes.id_pessoa = pa.id_pessoa
      WHERE pes.nome = 'Light Yagami' AND pes.dt_nascimento = DATE '1986-02-28'
    ),
    (
      SELECT re.id_pessoa
      FROM RESIDENTE re
      INNER JOIN PROFISSIONAL pro ON pro.id_pessoa = re.id_pessoa
      WHERE pro.crm = '11223-PB' AND re.dt_fim IS NULL
    ),
    (
      SELECT re.dt_inicio
      FROM RESIDENTE re
      INNER JOIN PROFISSIONAL pro ON pro.id_pessoa = re.id_pessoa
      WHERE pro.crm = '11223-PB' AND re.dt_fim IS NULL
    ),
    (
      SELECT pr.id_pessoa
      FROM PRECEPTOR pr
      INNER JOIN PROFISSIONAL pro ON pro.id_pessoa = pr.id_pessoa
      WHERE pro.crm = '4004-PB' AND pr.dt_fim IS NULL
    ),
    (
      SELECT pr.dt_inicio
      FROM PRECEPTOR pr
      INNER JOIN PROFISSIONAL pro ON pro.id_pessoa = pr.id_pessoa
      WHERE pro.crm = '4004-PB' AND pr.dt_fim IS NULL
    ),
    (
      SELECT u.id_unidade
      FROM UNIDADE u
      WHERE u.nome = 'AMBULATORIO'
    )
);


-- O atendimento é criado acima, então seus procedimentos precisam ser inseridos aqui.
SELECT
    atendimento.id_atendimento,
    atendimento.data_hora,
    atendimento.duracao_minutos,
    pessoa_paciente.nome AS paciente,
    pessoa_residente.nome AS residente,
    pessoa_preceptor.nome AS preceptor
FROM ATENDIMENTO atendimento
INNER JOIN PESSOA pessoa_paciente ON pessoa_paciente.id_pessoa = atendimento.id_paciente
INNER JOIN PESSOA pessoa_residente ON pessoa_residente.id_pessoa = atendimento.id_residente
INNER JOIN PESSOA pessoa_preceptor ON pessoa_preceptor.id_pessoa = atendimento.id_preceptor
WHERE pessoa_paciente.nome = 'Light Yagami' AND pessoa_paciente.dt_nascimento = DATE '1986-02-28' AND atendimento.data_hora = TIMESTAMP '2026-07-07 08:30:00';



-- Listar todos os atendimentos de um paciente específico,
SELECT a.id_atendimento, pes_pa.nome AS paciente, a.data_hora, a.duracao_minutos, pes_re.nome AS residente, pes_pr.nome AS preceptor
FROM PACIENTE pa
INNER JOIN PESSOA pes_pa ON pes_pa.id_pessoa = pa.id_pessoa
LEFT JOIN ATENDIMENTO a ON a.id_paciente = pa.id_pessoa
LEFT JOIN PESSOA pes_re ON pes_re.id_pessoa = a.id_residente
LEFT JOIN PESSOA pes_pr ON pes_pr.id_pessoa = a.id_preceptor
WHERE pes_pa.nome = 'Light Yagami'
ORDER BY a.data_hora ASC;



-- Listar os procedimentos realizados em um atendimento.
SELECT a.id_atendimento, a.data_hora, pes_pa.nome AS paciente, pro.codigo, pro.nome AS procedimento, a_pro.qtd_executada, a_pro.tempo_real_gasto, a_pro.is_faturado
FROM ATENDIMENTO a
INNER JOIN PACIENTE pa ON pa.id_pessoa = a.id_paciente
LEFT JOIN PESSOA pes_pa ON pes_pa.id_pessoa = pa.id_pessoa
LEFT JOIN ATENDIMENTO_PROCEDIMENTO a_pro ON a_pro.id_atendimento = a.id_atendimento
LEFT JOIN PROCEDIMENTO pro ON pro.id_procedimento = a_pro.id_procedimento
WHERE pes_pa.nome = 'Light Yagami';



-- Atualizar os dados de um paciente (atualizando o convênio)
UPDATE PACIENTE pa
SET num_convenio = 'KIRA-999'
FROM PESSOA pes
WHERE pa.id_pessoa = pes.id_pessoa
AND pes.nome = 'Light Yagami';


-- Remover um procedimento realizado (não faturado) (Coleta de sangue do atendimento criado acima)
WITH procedimento_para_remover AS (
    SELECT
        realizado.id_atendimento,
        realizado.id_procedimento,
        procedimento.codigo,
        procedimento.nome
    FROM ATENDIMENTO_PROCEDIMENTO realizado
    INNER JOIN ATENDIMENTO atendimento
        ON atendimento.id_atendimento = realizado.id_atendimento
    INNER JOIN PESSOA pessoa_paciente
        ON pessoa_paciente.id_pessoa = atendimento.id_paciente
    INNER JOIN PROCEDIMENTO procedimento
        ON procedimento.id_procedimento = realizado.id_procedimento
    WHERE pessoa_paciente.nome = 'Light Yagami'
      AND pessoa_paciente.dt_nascimento = DATE '1986-02-28'
      AND atendimento.data_hora = TIMESTAMP '2026-07-07 08:30:00'
      AND procedimento.codigo = 'PROC-001'
      AND realizado.is_faturado = FALSE
)
DELETE FROM ATENDIMENTO_PROCEDIMENTO at_pro
USING procedimento_para_remover alvo
WHERE alvo.id_atendimento = at_pro.id_atendimento AND alvo.id_procedimento = at_pro.id_procedimento
RETURNING at_pro.id_atendimento, alvo.codigo, alvo.nome;



-- Calcular o tempo médio de duração dos atendimentos por residente
SELECT pes.nome AS nome_residente, ROUND(AVG(a.duracao_minutos), 2) AS media_duracao_minutos
FROM RESIDENTE re
INNER JOIN PESSOA pes ON pes.id_pessoa = re.id_pessoa
LEFT JOIN ATENDIMENTO a ON a.id_residente = re.id_pessoa AND a.dt_inicio_residente = re.dt_inicio
GROUP BY pes.id_pessoa, pes.nome
ORDER BY media_duracao_minutos DESC;
