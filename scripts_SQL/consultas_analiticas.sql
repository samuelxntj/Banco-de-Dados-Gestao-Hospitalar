


-- Ranking dos residentes por número de atendimentos realizados (mostrar nome e total)
SELECT p.nome, COUNT(a.id_residente) AS quantidade_atendimentos
FROM RESIDENTE r
INNER JOIN PESSOA p ON p.id_pessoa = r.id_pessoa
LEFT JOIN ATENDIMENTO a
ON a.id_residente = p.id_pessoa
GROUP BY p.nome
ORDER BY quantidade_atendimentos DESC;


-- Listar os preceptores que supervisionaram mais de 5 atendimentos em um determinado mês
SELECT p.nome, COUNT(a.id_preceptor) AS quantidade_atendimentos
FROM PESSOA p
INNER JOIN ATENDIMENTO a
ON a.id_preceptor = p.id_pessoa
WHERE EXTRACT(MONTH FROM a.data_hora) = 7 -- Julho
    AND EXTRACT(YEAR FROM a.data_hora) = 2026
GROUP BY p.nome
HAVING COUNT(a.id_preceptor) > 5
ORDER BY quantidade_atendimentos DESC;


-- Para cada unidade, mostrar a quantidade de plantões escalados por residente.
SELECT u.nome AS unidade, p.nome AS residente, COUNT(*) AS quantidade_plantoes
FROM ESCALA_PLANTAO e
INNER JOIN UNIDADE u ON u.id_unidade = e.id_unidade
INNER JOIN PESSOA p ON p.id_pessoa = e.id_residente
GROUP BY u.nome, p.nome
ORDER BY u.nome, quantidade_plantoes DESC, residente;


-- Listar pacientes que nunca realizaram nenhum procedimento de nível de risco 'ALTO'
SELECT p.nome
FROM PACIENTE pac
INNER JOIN PESSOA p ON p.id_pessoa = pac.id_pessoa
WHERE pac.id_pessoa NOT IN (
    SELECT a.id_paciente
    FROM ATENDIMENTO a
    INNER JOIN ATENDIMENTO_PROCEDIMENTO ap ON ap.id_atendimento = a.id_atendimento
    INNER JOIN PROCEDIMENTO pr ON pr.id_procedimento = ap.id_procedimento
    WHERE pr.nivel_risco = 'ALTO'
)
ORDER BY p.nome;