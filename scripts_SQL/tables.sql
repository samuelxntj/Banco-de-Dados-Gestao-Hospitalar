-- ETAPA 1: CRIAÇÃO DA HIERARQUIA DE TABELAS (PESSOA -> SUBTIPOS)

-- 1. TABELA PAI: PESSOA
CREATE TABLE PESSOA (
    id_pessoa SERIAL,
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(11) NOT NULL,
    dt_nascimento DATE NOT NULL,
    is_flamengo BOOLEAN NOT NULL DEFAULT FALSE,
    
    -- Flags de controle para gerenciar a especialização (Herança)
    is_paciente BOOLEAN NOT NULL DEFAULT FALSE,
    is_profissional BOOLEAN NOT NULL DEFAULT FALSE,
    
    CONSTRAINT PK_PESSOA PRIMARY KEY (id_pessoa),
    CONSTRAINT UN_PESSOA_CPF UNIQUE (cpf),
    
    -- Uma restrição UNIQUE composta permite que as tabelas filhas validem as flags por FK
    CONSTRAINT UN_PESSOA_HERANCA UNIQUE (id_pessoa, is_paciente, is_profissional),
    
    -- Restrição de Especialização Total: Uma pessoa DEVE ser pelo menos um dos dois
    CONSTRAINT CK_PESSOA_ESPECIALIZACAO CHECK (is_paciente = TRUE OR is_profissional = TRUE)
);

-- 2. SUBTIPO NÍVEL 1: PACIENTE
CREATE TABLE PACIENTE (
    id_pessoa INT,
    num_convenio VARCHAR(20) NOT NULL,
    grupo_sanguineo VARCHAR(3) NOT NULL,
    
    -- Esta flag garante que a linha é de um paciente;
    -- a outra flag é usada apenas para alinhar a FK com a tabela PESSOA.
    is_paciente_flag BOOLEAN NOT NULL DEFAULT TRUE CHECK (is_paciente_flag = TRUE),
    is_profissional_flag BOOLEAN NOT NULL,
    
    CONSTRAINT PK_PACIENTE PRIMARY KEY (id_pessoa),
    CONSTRAINT UN_PACIENTE_CONVENIO UNIQUE (num_convenio),
    
    CONSTRAINT FK_PACIENTE_PESSOA FOREIGN KEY (id_pessoa, is_paciente_flag, is_profissional_flag) 
        REFERENCES PESSOA(id_pessoa, is_paciente, is_profissional) ON DELETE CASCADE
);

-- 3. SUBTIPO NÍVEL 1: PROFISSIONAL
CREATE TABLE PROFISSIONAL (
    id_pessoa INT,
    crm VARCHAR(100) NOT NULL,
    dt_admissao TIMESTAMP NOT NULL,
    especialidade VARCHAR(100) NOT NULL,
    
    is_paciente_flag BOOLEAN NOT NULL,
    is_profissional_flag BOOLEAN NOT NULL DEFAULT TRUE CHECK (is_profissional_flag = TRUE),
    
    CONSTRAINT PK_PROFISSIONAL PRIMARY KEY (id_pessoa),
    CONSTRAINT UN_PROFISSIONAL_CRM UNIQUE (crm),
    
    CONSTRAINT FK_PROFISSIONAL_PESSOA FOREIGN KEY (id_pessoa, is_paciente_flag, is_profissional_flag) 
        REFERENCES PESSOA(id_pessoa, is_paciente, is_profissional) ON DELETE CASCADE
);

-- 4. SUBTIPO NÍVEL 2: RESIDENTE (Com Chave Composta para Histórico)
CREATE TABLE RESIDENTE (
    id_pessoa INT,
    dt_inicio TIMESTAMP NOT NULL,
    dt_fim TIMESTAMP,
    ano_residencia VARCHAR(2) NOT NULL,
    
    CONSTRAINT PK_RESIDENTE PRIMARY KEY (id_pessoa, dt_inicio),
    
    CONSTRAINT FK_RESIDENTE_PROFISSIONAL FOREIGN KEY (id_pessoa) 
        REFERENCES PROFISSIONAL(id_pessoa) ON DELETE CASCADE,
        
    CONSTRAINT CK_ANO_RESIDENCIA CHECK (ano_residencia IN ('R1', 'R2', 'R3')),
    -- Garante coerência temporal simples nas datas do histórico
    CONSTRAINT CK_RESIDENTE_DATAS CHECK (dt_fim IS NULL OR dt_fim >= dt_inicio)
);

-- 5. SUBTIPO NÍVEL 2: PRECEPTOR (Com Chave Composta para Histórico)
CREATE TABLE PRECEPTOR (
    id_pessoa INT,
    dt_inicio TIMESTAMP NOT NULL,
    dt_fim TIMESTAMP,
    titulacao VARCHAR(20) NOT NULL,
    
    CONSTRAINT PK_PRECEPTOR PRIMARY KEY (id_pessoa, dt_inicio),
    
    CONSTRAINT FK_PRECEPTOR_PROFISSIONAL FOREIGN KEY (id_pessoa) 
        REFERENCES PROFISSIONAL(id_pessoa) ON DELETE CASCADE,
        
    CONSTRAINT CK_PRECEPTOR_DATAS CHECK (dt_fim IS NULL OR dt_fim >= dt_inicio)
);



-- TABELA UNIDADE:
CREATE TABLE UNIDADE(
    id_unidade SERIAL,
    nome VARCHAR(14), -- Faltava uma vírgula.

    CONSTRAINT pk_unidade PRIMARY KEY (id_unidade),
    CONSTRAINT  ck_nome CHECK (nome IN ('ENFERMARIA', 'UTI', 'PRONTO-SOCORRO', 'AMBULATORIO'))
);

-- TABELA PROCEDIMENTO:
CREATE TABLE PROCEDIMENTO(
    id_procedimento SERIAL,
    codigo VARCHAR(20) NOT NULL UNIQUE,
    nome VARCHAR(100) NOT NULL,
    tempo_medio_execucao INT,
    nivel_risco VARCHAR(5) NOT NULL DEFAULT 'BAIXO',

    CONSTRAINT pk_procedimento PRIMARY KEY (id_procedimento),
    CONSTRAINT ck_nivel_risco CHECK (nivel_risco IN ('ALTO', 'MEDIO', 'BAIXO'))
);



-- TABELAS RESULTANTES DA NORMALIZAÇÃO (TRATAMENTO DOS MULTIVALORADOS NA 1FN)

-- NORMALIZAÇÃO DE PESSOA: TELEFONE
-- O atributo "telefone" era multivalorado no MER (uma pessoa pode ter vários números),
-- o que violava a 1FN. Cada número vira uma linha própria.
CREATE TABLE TELEFONE (
    id_pessoa INT,
    num_telefone VARCHAR(20),
    CONSTRAINT PK_TELEFONE PRIMARY KEY (id_pessoa, num_telefone),
    CONSTRAINT FK_TELEFONE_PESSOA FOREIGN KEY (id_pessoa)
        REFERENCES PESSOA(id_pessoa) ON DELETE CASCADE
);

-- NORMALIZAÇÃO DE PACIENTE (parte 1): ALERGIA
-- Catálogo de alergias. O atributo "alergias" era multivalorado em PACIENTE e violava a 1FN.
CREATE TABLE ALERGIA (
    id_alergia SERIAL,
    nome_alergia VARCHAR(100) NOT NULL,

    CONSTRAINT PK_ALERGIA PRIMARY KEY (id_alergia),
    CONSTRAINT UN_ALERGIA_NOME UNIQUE (nome_alergia)
);

-- NORMALIZAÇÃO DE PACIENTE (parte 2): ALERGIA_PACIENTE
-- Tabela de junção: a relação entre PACIENTE e ALERGIA é N:N
CREATE TABLE ALERGIA_PACIENTE (
    id_pessoa INT,
    id_alergia INT,

    CONSTRAINT PK_ALERGIA_PACIENTE PRIMARY KEY (id_pessoa, id_alergia),
    CONSTRAINT FK_ALERGIA_PACIENTE_PACIENTE FOREIGN KEY (id_pessoa)
        REFERENCES PACIENTE(id_pessoa) ON DELETE CASCADE,
    CONSTRAINT FK_ALERGIA_PACIENTE_ALERGIA FOREIGN KEY (id_alergia)
        REFERENCES ALERGIA(id_alergia) ON DELETE CASCADE
);



-- TABELAS DE OPERAÇÃO E RELACIONAMENTOS (COM FKs COMPOSTAS DO HISTÓRICO)

-- TABELA ATENDIMENTO
-- Relações N:1 com PACIENTE, RESIDENTE e PRECEPTOR: um atendimento tem exatamente
-- um paciente, um residente e um preceptor, mas cada um deles pode ter vários atendimentos.
CREATE TABLE ATENDIMENTO (
    id_atendimento SERIAL,
    data_hora TIMESTAMP NOT NULL,
    duracao_minutos INT NOT NULL,
    id_paciente INT NOT NULL,

    id_residente INT NOT NULL,
    dt_inicio_residente TIMESTAMP NOT NULL,

    id_preceptor INT NOT NULL,
    dt_inicio_preceptor TIMESTAMP NOT NULL,

    id_unidade INT NOT NULL,

    CONSTRAINT PK_ATENDIMENTO PRIMARY KEY (id_atendimento),
    CONSTRAINT FK_ATENDIMENTO_PACIENTE FOREIGN KEY (id_paciente)
        REFERENCES PACIENTE(id_pessoa) ON DELETE RESTRICT,

    CONSTRAINT FK_ATENDIMENTO_RESIDENTE FOREIGN KEY (id_residente, dt_inicio_residente)
        REFERENCES RESIDENTE(id_pessoa, dt_inicio) ON DELETE RESTRICT,
    CONSTRAINT FK_ATENDIMENTO_PRECEPTOR FOREIGN KEY (id_preceptor, dt_inicio_preceptor)
        REFERENCES PRECEPTOR(id_pessoa, dt_inicio) ON DELETE RESTRICT,

    CONSTRAINT FK_ATENDIMENTO_UNIDADE FOREIGN KEY (id_unidade)
        REFERENCES UNIDADE(id_unidade) ON DELETE RESTRICT,

    CONSTRAINT CK_ATENDIMENTO_DURACAO CHECK (duracao_minutos > 0),

    -- Uma mesma pessoa não pode ocupar dois papéis no mesmo atendimento:
    CONSTRAINT CK_ATENDIMENTO_PAPEIS CHECK (
        id_residente <> id_preceptor
        AND id_paciente <> id_residente
        AND id_paciente <> id_preceptor
    )
);

-- TABELA ATENDIMENTO_PROCEDIMENTO (o "procedimento realizado")
-- A relação entre ATENDIMENTO e PROCEDIMENTO é N:N: um atendimento pode ter vários
-- procedimentos e um procedimento pode ocorrer em vários atendimentos.
CREATE TABLE ATENDIMENTO_PROCEDIMENTO (
    id_atendimento INT,
    id_procedimento INT,
    qtd_executada INT NOT NULL DEFAULT 1,
    tempo_real_gasto INT NOT NULL,
    observacao_intercorrencias VARCHAR(255),

    dt_hora_inicio TIMESTAMP NOT NULL,

    -- Flag de faturamento: um procedimento realizado só pode ser removido enquanto não faturado
    is_faturado BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT PK_ATENDIMENTO_PROCEDIMENTO PRIMARY KEY (id_atendimento, id_procedimento),
    CONSTRAINT FK_ATEND_PROC_ATENDIMENTO FOREIGN KEY (id_atendimento)
        REFERENCES ATENDIMENTO(id_atendimento) ON DELETE CASCADE,
    CONSTRAINT FK_ATEND_PROC_PROCEDIMENTO FOREIGN KEY (id_procedimento)
        REFERENCES PROCEDIMENTO(id_procedimento) ON DELETE RESTRICT,

    CONSTRAINT CK_ATEND_PROC_QTD CHECK (qtd_executada > 0),
    CONSTRAINT CK_ATEND_PROC_TEMPO CHECK (tempo_real_gasto >= 0)
);

-- TABELA ESCALA_PLANTAO
-- Define o plantão: uma unidade, um dia da semana, um turno, um residente e o preceptor que o supervisiona..
CREATE TABLE ESCALA_PLANTAO (
    id_escala SERIAL,
    dia_semana VARCHAR(8) NOT NULL,
    turno VARCHAR(6) NOT NULL,
    id_unidade INT NOT NULL,

    id_residente INT NOT NULL,
    dt_inicio_residente TIMESTAMP NOT NULL,
    id_preceptor INT NOT NULL,
    dt_inicio_preceptor TIMESTAMP NOT NULL,

    CONSTRAINT PK_ESCALA_PLANTAO PRIMARY KEY (id_escala),
    CONSTRAINT FK_ESCALA_UNIDADE FOREIGN KEY (id_unidade)
        REFERENCES UNIDADE(id_unidade) ON DELETE RESTRICT,
    CONSTRAINT FK_ESCALA_RESIDENTE FOREIGN KEY (id_residente, dt_inicio_residente)
        REFERENCES RESIDENTE(id_pessoa, dt_inicio) ON DELETE RESTRICT,
    CONSTRAINT FK_ESCALA_PRECEPTOR FOREIGN KEY (id_preceptor, dt_inicio_preceptor)
        REFERENCES PRECEPTOR(id_pessoa, dt_inicio) ON DELETE RESTRICT,

    -- Não pode haver o mesmo residente no mesmo local/dia/turno
    -- com dois preceptores distintos. O UNIQUE usa id_residente (a pessoa), e não o período,
    -- para não enfraquecer a restrição.
    CONSTRAINT UN_ESCALA_RESIDENTE UNIQUE (id_unidade, dia_semana, turno, id_residente),
    CONSTRAINT CK_ESCALA_DIA CHECK (dia_semana IN ('SEGUNDA', 'TERCA', 'QUARTA', 'QUINTA', 'SEXTA', 'SABADO', 'DOMINGO')),
    CONSTRAINT CK_ESCALA_TURNO CHECK (turno IN ('MANHA', 'TARDE', 'NOITE')),
    CONSTRAINT CK_ESCALA_PAPEIS CHECK (id_residente <> id_preceptor)
);

