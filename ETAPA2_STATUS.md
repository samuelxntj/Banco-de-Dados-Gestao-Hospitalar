# Etapa 2 — Onde estamos

Mapa do que o enunciado (PDF) pede na Etapa 2 e do que já existe no repositório.
Levantado por varredura em todo o projeto por `trigger`, `procedure`, `create view`,
`vw_`, `sp_`, `internac` e `auditoria` — que não retornou nenhuma ocorrência.

**Stack escolhida:** Python + PostgreSQL, ORM SQLAlchemy.

## Situação por requisito

| # | Requisito | Pontos | Status | Onde fazer |
|---|---|---|---|---|
| 1 | Stored Procedures: `sp_registrar_atendimento_completo`, `sp_calcular_tempo_medio_espera`, `sp_reajustar_escala` | 1,5 | ❌ não iniciado | criar `scripts_SQL/procedures.sql` |
| 2 | Triggers: `trg_check_sobreposicao_escala`, `trg_audita_atendimento`, `trg_atualiza_media_procedimentos` | 1,5 | ❌ não iniciado | criar `scripts_SQL/triggers.sql` |
| 3 | Views: `vw_pacientes_internados`, `vw_residentes_sem_supervisor`, `vw_estatisticas_atendimentos_mensal` | 1,0 | ❌ não iniciado | criar `scripts_SQL/views.sql` |
| 4 | ORM: mapeamento, sessões/transações, DSL, lazy vs eager | 2,0 | 🟡 parcial | `models.py`, `bd.py`, `consultas_orm.py` |
| 5 | 3 consultas avançadas via ORM | 1,0 | ❌ não iniciado | criar `scripts_python/consultas_avancadas_orm.py` |
| 6 | Concorrência: 2 transações disputando a mesma escala, com lock | 1,0 | ❌ não iniciado | criar `scripts_python/teste_concorrencia.py` |
| 7 | Entrega: commits separados por etapa, vídeo de 8 min, relatório de 2 páginas | +1 extra | ❌ não iniciado | — |

## Detalhamento

### 1. Stored Procedures (1,5 pt)

- `sp_registrar_atendimento_completo` — recebe os dados do atendimento **mais** uma lista
  de procedimentos realizados (JSON ou tabela temporária) e insere tudo dentro de uma
  transação: se qualquer procedimento falhar, tudo é revertido.
- `sp_calcular_tempo_medio_espera` — para cada unidade, o tempo médio entre a chegada do
  paciente (`ATENDIMENTO.data_hora`) e o início do primeiro procedimento.
  ⚠️ Hoje `ATENDIMENTO_PROCEDIMENTO` **não guarda o horário de início** do procedimento —
  só `tempo_real_gasto`. É preciso decidir se entra uma coluna `data_hora_inicio` ou se o
  cálculo será derivado de outra forma.
- `sp_reajustar_escala` — recebe um `id_residente` e move todas as escalas dele de um
  dia/turno para outro, desde que não gere conflito com `UN_ESCALA_RESIDENTE`.

### 2. Triggers (1,5 pt)

- `trg_check_sobreposicao_escala` — BEFORE INSERT/UPDATE em `ESCALA_PLANTAO`. Impede o
  mesmo residente escalado no mesmo dia/turno em **duas unidades diferentes**.
  (Note que a `UNIQUE` atual inclui `id_unidade`, então ela *permite* esse caso — a
  trigger é justamente o que fecha essa brecha.)
- `trg_audita_atendimento` — AFTER INSERT/UPDATE/DELETE em `ATENDIMENTO`, gravando em
  `AUDITORIA_ATENDIMENTO`.
- `trg_atualiza_media_procedimentos` — AFTER INSERT em `ATENDIMENTO_PROCEDIMENTO`,
  atualizando a coluna `media_tempo_procedimento` de `PROCEDIMENTO`.

### 3. Views (1,0 pt)

- `vw_pacientes_internados` — pacientes com `data_hora_saida IS NULL` na internação mais
  recente. **Depende da tabela `INTERNACAO`** (ver pré-requisitos abaixo).
- `vw_residentes_sem_supervisor` — residentes escalados em algum plantão cujo preceptor
  não tem titulação de doutor (ou não possui supervisão ativa).
- `vw_estatisticas_atendimentos_mensal` — agregação por mês e por unidade: total de
  atendimentos, média de duração, procedimentos mais comuns.
  ⚠️ `ATENDIMENTO` **não tem `id_unidade`**; a unidade só aparece em `ESCALA_PLANTAO`.
  É preciso decidir como ligar atendimento → unidade (coluna nova em `ATENDIMENTO` ou
  join pela escala do residente).

### 4. ORM (2,0 pts) — parcial

Já feito:
- `scripts_python/models.py` — todas as entidades mapeadas em SQLAlchemy 2.0
  (`DeclarativeBase` + `Mapped`), incluindo as FKs compostas do histórico de
  residente/preceptor e os relacionamentos.
- `scripts_python/bd.py` — `engine` e `SessionLocal` (fábrica de sessões).
- `scripts_python/testar_bd.py` — teste de conexão.
- `scripts_python/consultas_orm.py` — demonstra consulta via DSL, update dentro de
  transação, **lazy loading** e **eager loading** (`selectinload`), e uma agregação
  (`func.avg` + `func.round`).

Falta:
- **Reimplementar via ORM as 6 operações CRUD da Etapa 1** (hoje só existem em SQL puro
  em `scripts_SQL/CRUD_Consultas.sql`):
  1. inserir um novo atendimento (verificando paciente, residente e preceptor);
  2. listar todos os atendimentos de um paciente, ordenados por data;
  3. listar os procedimentos realizados em um atendimento;
  4. atualizar os dados de um paciente;
  5. remover um procedimento realizado apenas se `is_faturado = FALSE`;
  6. tempo médio de duração dos atendimentos por residente.
- Reimplementar também as 4 consultas analíticas da Etapa 1 via ORM.

### 5. Consultas avançadas com ORM (1,0 pt)

- Preceptores que supervisionaram residentes que atenderam pacientes flamenguistas
  (`is_flamengo = TRUE`).
- Para cada paciente, o último atendimento (data_hora, residente, preceptor e lista de
  procedimentos).
- Percentual de procedimentos de alto risco realizados por cada residente.

### 6. Concorrência e transações (1,0 pt)

- Simular duas transações concorrentes tentando escalar o **mesmo residente** para o
  mesmo dia/turno/unidade.
- Usar lock otimista ou pessimista (ex.: `with_for_update()` do SQLAlchemy, ou uma coluna
  de versão) para evitar a inconsistência.
- Demonstrar com código e **logs** — vale imprimir os timestamps de cada thread/sessão.

## Pré-requisitos de schema

Precisam entrar em `scripts_SQL/tables.sql` (e no `models.py`, e ganhar dados em
`adicionando_dados.sql`) **antes** dos itens 2 e 3:

1. **Tabela `INTERNACAO`** — decisão tomada: criar. O PDF cita internações no contexto do
   sistema, mas a omitiu no modelo relacional da Etapa 1, e `vw_pacientes_internados`
   depende dela. Estrutura acordada:
   ```
   INTERNACAO (
       id_internacao      SERIAL PRIMARY KEY,
       id_paciente        INT NOT NULL → PACIENTE(id_pessoa),
       id_unidade         INT NOT NULL → UNIDADE(id_unidade),
       data_hora_entrada  TIMESTAMP NOT NULL,
       data_hora_saida    TIMESTAMP NULL,
       CHECK (data_hora_saida IS NULL OR data_hora_saida >= data_hora_entrada)
   )
   ```
2. **Coluna `media_tempo_procedimento`** em `PROCEDIMENTO` — exigida por
   `trg_atualiza_media_procedimentos`.
3. **Tabela `AUDITORIA_ATENDIMENTO`** — exigida por `trg_audita_atendimento`:
   `id_auditoria, id_atendimento, operacao, usuario, data_hora, dados_antigos JSONB,
   dados_novos JSONB`.

## Dívida técnica

Divergências entre `scripts_python/models.py` e `scripts_SQL/tables.sql`. **Não quebram a
execução**, porque o schema é criado pelo `tables.sql` e não por `Base.metadata.create_all`,
mas convém alinhar junto com o item 4:

- `UNIDADE.nome`: `String(100)` no ORM vs `VARCHAR(14)` no SQL;
- `ATENDIMENTO_PROCEDIMENTO.observacao_intercorrencias`: `Text` vs `VARCHAR(255)`;
- `ESCALA_PLANTAO.dia_semana`: `String(15)` vs `VARCHAR(8)`;
- `PROCEDIMENTO.nivel_risco`: `String(10)` vs `VARCHAR(5)`;
- `CHECK` presentes no SQL e ausentes no ORM: `CK_ATENDIMENTO_PAPEIS`,
  `CK_ESCALA_PAPEIS`, `CK_ATENDIMENTO_DURACAO`, `ck_nome` (UNIDADE) e `ck_nivel_risco`.

Já corrigido: `Procedimento.tempo_medio_exec_min` → `tempo_medio_execucao`, que era o nome
real da coluna no banco (o mapeamento antigo quebrava qualquer consulta ORM sobre
`PROCEDIMENTO`).
