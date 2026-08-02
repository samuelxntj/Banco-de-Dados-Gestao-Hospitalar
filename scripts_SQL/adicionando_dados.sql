

-- Adicionando dados para a tabela PESSOA
INSERT INTO PESSOA (nome, cpf, dt_nascimento, is_flamengo, is_paciente, is_profissional)
VALUES
('João Silva', '11111111111', '1990-05-14', TRUE, TRUE, FALSE),
('Gabriel Barbosa (Gabigol)', '22222222222', '1996-08-30', TRUE, TRUE, FALSE),
('Arthur Antunes Coimbra (Zico)', '33333333333', '1953-03-03', TRUE, TRUE, FALSE),
('Monkey D. Luffy', '44444444444', '1997-05-05', TRUE, TRUE, FALSE),
('Light Yagami', '55555555555', '1986-02-28', FALSE, TRUE, FALSE),

('Lucas Lima', '66666666666', '1996-03-10', TRUE, FALSE, TRUE),
('Fernanda Alves', '77777777777', '1995-08-22', TRUE, FALSE, TRUE),
('Rafael Mendes', '88888888888', '1994-11-30', TRUE, FALSE, TRUE),
('Beatriz Rocha', '99999999999', '1997-01-14', TRUE, FALSE, TRUE),
('Thiago Pereira', '10101010101', '1995-05-25', TRUE, FALSE, TRUE),

('Roberto Carlos', '12121212121', '1970-04-19', TRUE, FALSE, TRUE),
('Juliana Moraes', '13131313131', '1980-09-11', TRUE, FALSE, TRUE),
('Marcos Vinicius', '14141414141', '1975-12-01', TRUE, FALSE, TRUE),
('Camila Barros', '15151515151', '1982-07-08', TRUE, FALSE, TRUE),
('André Ribeiro', '16161616161', '1968-02-28', TRUE, FALSE, TRUE),

('Carlos Eduardo', '17171717171', '1980-05-10', TRUE, TRUE, TRUE),
('Marina Silva', '18181818181', '1996-12-01', TRUE, TRUE, TRUE),
('Fernando Souza', '19191919191', '1990-08-20', TRUE, TRUE, TRUE);


-- Adicionando dados para a tabela PACIENTE
INSERT INTO PACIENTE (id_pessoa, num_convenio, grupo_sanguineo, is_paciente_flag, is_profissional_flag)
VALUES
(1, 'UNIMED-001', 'O+', TRUE, FALSE),
(2, 'FLA-2019', 'O+', TRUE, FALSE),
(3, 'FLA-1981', 'O-', TRUE, FALSE),
(4, 'MUGIWARA-001', 'B+', TRUE, FALSE),
(5, 'KIRA-040', 'AB+', TRUE, FALSE),

(16, 'UNIMED-016', 'A+', TRUE, TRUE),
(17, 'AMIL-017', 'O+', TRUE, TRUE),
(18, 'SULAM-018', 'B-', TRUE, TRUE);


-- Adicionando dados para a tabela PROFISSIONAL
INSERT INTO PROFISSIONAL (id_pessoa, crm, dt_admissao, especialidade, is_paciente_flag, is_profissional_flag)
VALUES
(6, '12345-PB', '2025-01-10 08:00:00', 'Clínica Médica', FALSE, TRUE),
(7, '54321-PB', '2024-01-15 08:00:00', 'Cirurgia Geral', FALSE, TRUE),
(8, '98765-PB', '2023-01-20 08:00:00', 'Pediatria', FALSE, TRUE),
(9, '11223-PB', '2026-01-10 08:00:00', 'Ortopedia', FALSE, TRUE),
(10, '33445-PB', '2025-01-12 08:00:00', 'Cardiologia', FALSE, TRUE),

(11, '1001-PB', '2010-05-20 08:00:00', 'Clínica Médica', FALSE, TRUE),
(12, '2002-PB', '2015-08-15 08:00:00', 'Cirurgia Geral', FALSE, TRUE),
(13, '3003-PB', '2012-03-10 08:00:00', 'Pediatria', FALSE, TRUE),
(14, '4004-PB', '2018-11-20 08:00:00', 'Ortopedia', FALSE, TRUE),
(15, '5005-PB', '2005-09-05 08:00:00', 'Cardiologia', FALSE, TRUE),

(16, '6006-PB', '2015-02-01 08:00:00', 'Cardiologia', TRUE, TRUE),
(17, '13579-PB', '2025-03-01 08:00:00', 'Neurologia', TRUE, TRUE),
(18, '8008-PB', '2018-01-15 08:00:00', 'Psiquiatria', TRUE, TRUE);


-- Adicionando dados para a tabela RESIDENTE
INSERT INTO RESIDENTE (id_pessoa, dt_inicio, dt_fim, ano_residencia)
VALUES
(6, '2026-03-01 00:00:00', NULL, 'R1'),
(7, '2026-03-01 00:00:00', NULL, 'R2'),
(8, '2026-03-01 00:00:00', NULL, 'R3'),
(9, '2026-03-01 00:00:00', NULL, 'R1'),
(10, '2026-03-01 00:00:00', NULL, 'R2'),

(17, '2026-03-01 00:00:00', NULL, 'R2'),
(18, '2018-03-01 00:00:00', '2021-02-28 00:00:00', 'R3');



-- Adicionando dados para a tabela PRECEPTOR
INSERT INTO PRECEPTOR (id_pessoa, dt_inicio, dt_fim, titulacao)
VALUES
(11, '2015-01-01 00:00:00', NULL, 'Doutorado'),
(12, '2018-02-10 00:00:00', NULL, 'Mestrado'),
(13, '2014-06-01 00:00:00', NULL, 'Especialista'),
(14, '2020-01-15 00:00:00', NULL, 'Doutorado'),
(15, '2010-03-20 00:00:00', NULL, 'Mestrado'),

(16, '2015-02-01 00:00:00', NULL, 'MESTRADO'),
(18, '2021-03-01 00:00:00', NULL, 'Especialista');

-- Adicionando dados para a tabela TELEFONE
INSERT INTO TELEFONE (id_pessoa, num_telefone)
VALUES
(1, '+5583988881111'),
(2, '+5583981982019'),
(2, '+558332222019'),
(3, '+5583981981981'),
(4, '+5583988885656'),
(5, '+5583940404040'),
(6, '+5583988886666'),
(7, '+5583988887777'),
(8, '+5583988888888'),
(9, '+5583988889999'),
(10, '+5583999990000'),
(11, '+5583999991111'),
(11, '+558333331111'),
(12, '+5583999992222'),
(13, '+5583999993333'),
(14, '+5583999994444'),
(15, '+5583999995555'),
(16, '+5583999996666'),
(17, '+5583999997777'),
(18, '+5583999998888'),
(18, '+558333338888');


INSERT INTO ALERGIA (nome_alergia)
VALUES
('Vasco da Gama'),
('Gato'),
('Frutos do Mar'),
('Amendoim'),
('Cachorro'),
('Kairouseki'),
('Ficar sem Carne'),
('L');

INSERT INTO ALERGIA_PACIENTE (id_pessoa, id_alergia)
VALUES
-- João Silva
(1, 1), -- Vasco da Gama
(1, 3), -- Frutos do Mar

-- Gabriel Barbosa (Gabigol)
(2, 1), -- Vasco da Gama

-- Arthur Antunes Coimbra (Zico)
(3, 1), -- Vasco da Gama

-- Monkey D. Luffy
(4, 1), -- Vasco da Gama
(4, 6), -- Kairouseki
(4, 7), -- Ficar sem Carne

-- Light Yagami
(5, 5), -- Cachorro
(5, 8), -- L

-- Carlos Eduardo
(16, 1), -- Vasco da Gama
(16, 4), -- Amendoim

-- Marina Silva
(17, 1), -- Vasco da Gama
(17, 2), -- Gato

-- Fernando Souza
(18, 1), -- Vasco da Gama
(18, 4); -- Amendoim

-- =========================================================================
-- INSERÇÃO DOS DADOS FALTANTES PARA COMPLETAR OS REQUISITOS DA ETAPA 1
-- =========================================================================

-- Adicionando dados para a tabela UNIDADE
INSERT INTO UNIDADE (nome)
VALUES
('AMBULATORIO'),
('UTI'),
('PRONTO-SOCORRO'),
('ENFERMARIA');


-- Adicionando dados para a tabela PROCEDIMENTO
-- Cada procedimento possui código, nome e tempo médio de execução em minutos.
INSERT INTO PROCEDIMENTO (codigo, nome, tempo_medio_execucao, nivel_risco)
VALUES
('PROC-001', 'Coleta de Sangue', 15, 'BAIXO'),
('PROC-002', 'Sutura Simples (Costura)', 30, 'MEDIO'),
('PROC-003', 'Aplicação de Medicação IV', 10, 'BAIXO'),
('PROC-004', 'Ressonância Magnética (Alto Risco)', 45, 'ALTO'),
('PROC-005', 'Drenagem de Abscesso', 25, 'MEDIO'),
('PROC-006', 'Intubação Orotraqueal (Alto Risco)', 20, 'ALTO');


-- Adicionando dados para a tabela ATENDIMENTO
-- Os atendimentos ligam Pacientes, Residentes e Preceptores que os supervisionaram
INSERT INTO ATENDIMENTO (data_hora, duracao_minutos, id_paciente, id_residente, dt_inicio_residente, id_preceptor, dt_inicio_preceptor, id_unidade)
VALUES
('2026-07-01 10:00:00', 45, 1, 6, '2026-03-01 00:00:00', 11, '2015-01-01 00:00:00', 1),
('2026-07-01 11:30:00', 30, 2, 7, '2026-03-01 00:00:00', 12, '2018-02-10 00:00:00', 1),
('2026-07-02 09:00:00', 60, 3, 8, '2026-03-01 00:00:00', 13, '2014-06-01 00:00:00', 2),
('2026-07-02 14:00:00', 20, 4, 9, '2026-03-01 00:00:00', 14, '2020-01-15 00:00:00', 3),
('2026-07-03 08:30:00', 40, 5, 10, '2026-03-01 00:00:00', 15, '2010-03-20 00:00:00', 4),
('2026-07-03 16:00:00', 50, 3, 17, '2026-03-01 00:00:00', 16, '2015-02-01 00:00:00', 2),
('2026-07-04 10:30:00', 35, 17, 6, '2026-03-01 00:00:00', 11, '2015-01-01 00:00:00', 3),
('2026-07-04 11:00:00', 25, 18, 7, '2026-03-01 00:00:00', 12, '2018-02-10 00:00:00', 2),
('2026-07-05 15:00:00', 90, 1, 8, '2026-03-01 00:00:00', 13, '2014-06-01 00:00:00', 2),
('2026-07-05 17:30:00', 15, 2, 9, '2026-03-01 00:00:00', 14, '2020-01-15 00:00:00', 3),
('2026-07-06 09:15:00', 55, 3, 10, '2026-03-01 00:00:00', 15, '2010-03-20 00:00:00', 4),
('2026-07-06 14:45:00', 30, 4, 17, '2026-03-01 00:00:00', 16, '2015-02-01 00:00:00', 2),
('2026-07-08 09:00:00', 30, 2, 6, '2026-03-01 00:00:00', 11, '2015-01-01 00:00:00', 1),
('2026-07-09 10:00:00', 40, 3, 6, '2026-03-01 00:00:00', 11, '2015-01-01 00:00:00', 1),
('2026-07-10 11:00:00', 25, 4, 7, '2026-03-01 00:00:00', 11, '2015-01-01 00:00:00', 1),
('2026-07-11 14:00:00', 50, 1, 8, '2026-03-01 00:00:00', 11, '2015-01-01 00:00:00', 2),
('2026-07-12 09:00:00', 30, 1, 7, '2026-03-01 00:00:00', 12, '2018-02-10 00:00:00', 2),
('2026-07-13 10:30:00', 45, 2, 7, '2026-03-01 00:00:00', 12, '2018-02-10 00:00:00', 1),
('2026-07-14 14:00:00', 20, 3, 7, '2026-03-01 00:00:00', 12, '2018-02-10 00:00:00', 1),
('2026-07-15 16:15:00', 40, 4, 7, '2026-03-01 00:00:00', 12, '2018-02-10 00:00:00', 1),
('2026-07-16 08:00:00', 50, 5, 8, '2026-03-01 00:00:00', 13, '2014-06-01 00:00:00', 2),
('2026-07-17 09:30:00', 30, 16, 8, '2026-03-01 00:00:00', 13, '2014-06-01 00:00:00', 2),
('2026-07-18 11:00:00', 25, 17, 8, '2026-03-01 00:00:00', 13, '2014-06-01 00:00:00', 2),
('2026-07-19 13:45:00', 60, 18, 8, '2026-03-01 00:00:00', 13, '2014-06-01 00:00:00', 2),
('2026-07-20 10:00:00', 35, 1, 9, '2026-03-01 00:00:00', 14, '2020-01-15 00:00:00', 3),
('2026-07-21 14:30:00', 40, 2, 9, '2026-03-01 00:00:00', 14, '2020-01-15 00:00:00', 3),
('2026-07-22 16:00:00', 25, 3, 9, '2026-03-01 00:00:00', 14, '2020-01-15 00:00:00', 3);


-- Registra quais procedimentos foram executados em quais atendimentos.
INSERT INTO ATENDIMENTO_PROCEDIMENTO (id_atendimento, id_procedimento, qtd_executada, tempo_real_gasto, observacao_intercorrencias, dt_hora_inicio, is_faturado)
VALUES
(1, 1, 1, 12, 'Coleta rápida, sem intercorrências', '2026-07-01 10:05:00', FALSE),
(1, 2, 1, 35, 'Paciente nervoso, demorou mais que o previsto', '2026-07-01 10:20:00', FALSE),
(2, 3, 2, 15, 'Duas doses aplicadas com intervalo de 10 min', '2026-07-01 11:42:00', FALSE),
(3, 1, 1, 10, NULL, '2026-07-02 09:10:00', TRUE), -- Já faturado (não pode ser excluído)
(3, 5, 1, 30, 'Procedimento cirúrgico padrão realizado com sucesso', '2026-07-02 09:25:00', FALSE),
(4, 3, 1, 8, NULL, '2026-07-02 14:07:00', FALSE),
(5, 1, 2, 20, NULL, '2026-07-03 08:40:00', FALSE),
(6, 4, 1, 50, 'Procedimento de Alto Risco. Paciente estável', '2026-07-03 16:18:00', FALSE), -- Procedimento ALTO RISCO (id_procedimento = 4)
(7, 2, 1, 25, NULL, '2026-07-04 10:42:00', FALSE),
(8, 1, 1, 15, NULL, '2026-07-04 11:05:00', FALSE),
(9, 6, 1, 25, 'Procedimento de Alto Risco em caráter emergencial', '2026-07-05 15:15:00', FALSE), -- Procedimento ALTO RISCO (id_procedimento = 6)
(10, 3, 1, 10, NULL, '2026-07-05 17:34:00', FALSE),
(11, 1, 1, 15, 'Procedimento de rotina', '2026-07-06 09:22:00', FALSE),
(12, 2, 1, 30, NULL, '2026-07-06 15:00:00', FALSE),
(13, 3, 1, 10, NULL, '2026-07-08 09:08:00', FALSE),
(14, 1, 1, 15, NULL, '2026-07-09 10:12:00', FALSE),
(15, 1, 1, 15, 'Paciente tranquilo', '2026-07-10 11:06:00', FALSE),
(16, 2, 1, 30, NULL, '2026-07-11 14:14:00', FALSE),
(17, 3, 1, 10, NULL, '2026-07-12 09:09:00', FALSE),
(18, 1, 1, 15, NULL, '2026-07-13 10:48:00', FALSE),
(19, 1, 1, 15, NULL, '2026-07-14 14:04:00', FALSE),
(20, 2, 1, 30, 'Sutura simples sem complicações', '2026-07-15 16:26:00', FALSE),
(21, 3, 1, 10, NULL, '2026-07-16 08:07:00', FALSE);


-- Registra as escalas de plantão de cada residente e supervisor por unidade
INSERT INTO ESCALA_PLANTAO (dia_semana, turno, id_unidade, id_residente, dt_inicio_residente, id_preceptor, dt_inicio_preceptor)
VALUES
('SEGUNDA', 'MANHA', 1, 6, '2026-03-01 00:00:00', 11, '2015-01-01 00:00:00'),
('SEGUNDA', 'TARDE', 1, 7, '2026-03-01 00:00:00', 12, '2018-02-10 00:00:00'),
('TERCA', 'NOITE', 2, 8, '2026-03-01 00:00:00', 13, '2014-06-01 00:00:00'),
('QUARTA', 'MANHA', 3, 9, '2026-03-01 00:00:00', 14, '2020-01-15 00:00:00'),
('QUINTA', 'TARDE', 4, 10, '2026-03-01 00:00:00', 15, '2010-03-20 00:00:00'),
('SEXTA', 'NOITE', 2, 17, '2026-03-01 00:00:00', 16, '2015-02-01 00:00:00'),
('SABADO', 'MANHA', 3, 6, '2026-03-01 00:00:00', 11, '2015-01-01 00:00:00'),
('DOMINGO', 'NOITE', 2, 7, '2026-03-01 00:00:00', 12, '2018-02-10 00:00:00'),
('QUARTA', 'TARDE', 1, 6, '2026-03-01 00:00:00', 11, '2015-01-01 00:00:00'),
('QUINTA', 'MANHA', 2, 8, '2026-03-01 00:00:00', 13, '2014-06-01 00:00:00');
