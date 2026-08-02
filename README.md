# Sistema de Gestão Hospitalar Dra. Yuska Maritan Brito


**Contexto**:
O Hospital Universitário Dra. Yuska Maritan Brito precisa de um sistema para gerenciar atendimentos, profissionais, pacientes, procedimentos, internações e escalas de plantão.

**Especificações do Sistema:** O sistema deve cadastrar Pessoas. Toda pessoa possui nome, CPF, data de nascimento, is_flamengo e telefone. Uma pessoa pode ser Paciente (com atributos: número do convênio, alergias, grupo sanguíneo) ou Profissional (com atributos: CRM, data de admissão, especialidade). Um Profissional pode ser Preceptor (médico responsável) ou Residente (médico em formação). Um residente possui um atributo "ano_residencia" (R1, R2, R3). Um preceptor possui um atributo "titulacao" (mestre, doutor, etc.). Um profissional pode atuar como preceptor em um determinado período e como residente em outro (histórico), mas em um dado momento ele ocupa apenas um papel no sistema.

Um Atendimento ocorre em uma data e horário específicos, com duração registrada em minutos. Em cada atendimento, há exatamente um paciente, um residente (que realiza o atendimento sob supervisão) e um preceptor (que supervisiona aquele atendimento específico). Durante um atendimento, podem ser realizados um ou mais procedimentos (ex: sutura, coleta de sangue, aplicação de medicação). Cada procedimento possui um código, nome e tempo médio de execução. Para cada procedimento realizado em um atendimento, registra-se a quantidade executada, o tempo real gasto e uma observação sobre intercorrências.

O hospital possui Unidades (Enfermaria, UTI, Pronto-Socorro, Ambulatório). Os residentes e preceptores se organizam em Escalas de Plantão. Em uma escala, define-se: uma unidade, um dia da semana (segunda a domingo), um turno (manhã, tarde, noite), um residente e um preceptor responsável pela supervisão naquele plantão. Uma combinação de unidade, dia, turno, residente e preceptor é única (não pode haver o mesmo residente no mesmo local/dia/turno com dois preceptores distintos). O mesmo preceptor pode supervisionar vários residentes no mesmo plantão (desde que em unidades ou turnos diferentes), mas para cada residente registra-se um único preceptor supervisor por plantão.

> **Etapa 2:** o mapa do que já está pronto e do que falta está em
> [`ETAPA2_STATUS.md`](ETAPA2_STATUS.md).

## Como executar o SGBD

Os scripts Python ficam em `scripts_python/` e os arquivos SQL em `scripts_SQL/`.
O script `scripts_python/sgbd.py` conecta ao PostgreSQL, cria as tabelas
(`scripts_SQL/tables.sql`) e insere os dados (`scripts_SQL/adicionando_dados.sql`).
Ele apaga (DROP) as tabelas antes de recriá-las, então pode ser executado quantas
vezes forem necessárias — sempre partindo do zero.

> **Importante:** rode os scripts a partir da **raiz do projeto** (ex.:
> `python scripts_python/sgbd.py`), pois eles abrem os arquivos `.sql` por caminho
> relativo (`scripts_SQL/...`).

**Pré-requisitos:** Python 3 e PostgreSQL instalados.

### 1. Instalar o PostgreSQL

**Windows**
1. Baixe o instalador em <https://www.postgresql.org/download/windows/> (EnterpriseDB).
2. Execute o instalador. Durante a instalação, defina uma **senha para o usuário `postgres`**
   (anote-a) e mantenha a porta padrão **5432**.
3. O instalador já inclui o **pgAdmin** (interface gráfica) e o **SQL Shell (psql)**.

**Linux (Ubuntu/Debian)**
```bash
sudo apt update
sudo apt install -y postgresql
```
O serviço inicia automaticamente na porta **5432**. Para iniciá-lo manualmente, se preciso:
`sudo service postgresql start`.

### 2. Criar o usuário e o banco de dados

Abra o `psql` como administrador:
- **Windows:** abra o **SQL Shell (psql)** pelo menu Iniciar e faça login como `postgres`.
- **Linux:** `sudo -u postgres psql`

Dentro do `psql`, rode:
```sql
CREATE USER hospital WITH PASSWORD 'hospital' CREATEDB;
CREATE DATABASE gestao_hospitalar OWNER hospital;
\q
```

### 3. Preparar o ambiente Python

Na pasta do projeto:
```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
#   Windows:        venv\Scripts\activate
#   Linux/macOS:    source venv/bin/activate

# Instalar a dependência (driver do PostgreSQL)
pip install -r requirements.txt
```

### 4. Conferir as credenciais em `scripts_python/sgbd.py`

No topo do arquivo `scripts_python/sgbd.py`, ajuste as constantes conforme a sua instalação:
```python
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "gestao_hospitalar"
DB_USER = "hospital"
DB_PASSWORD = "hospital"
```

### 5. Executar

A partir da raiz do projeto:
```bash
python scripts_python/sgbd.py
```
Se tudo der certo, aparece: `Banco Criado.`

### 6. Executar as consultas (CRUD + analíticas)

O script `scripts_python/consultas.py` roda, em sequência, os comandos de
`scripts_SQL/CRUD_Consultas.sql` (INSERT, SELECT, UPDATE, DELETE e uma consulta de
média) e de `scripts_SQL/consultas_analiticas.sql` (as 4 consultas analíticas: ranking
de residentes, preceptores com mais de 5 atendimentos no mês, plantões por
unidade/residente e pacientes sem procedimento de risco 'ALTO'), **mostrando na tela**
o resultado de cada um. Reutiliza as mesmas credenciais definidas no `sgbd.py`.

Rode **depois** do `sgbd.py` (que cria e popula o banco), a partir da raiz do projeto:
```bash
python scripts_python/consultas.py
```
Observações:
- Como o CRUD insere um atendimento fixo, para rodar o `consultas.py` novamente basta
  rodar o `sgbd.py` antes, recriando o banco do zero.
- As consultas analíticas rodam **depois** das operações de CRUD, então seus números já
  refletem o atendimento inserido pelo CRUD.

### 7. Interface web (Streamlit)

Além dos scripts de linha de comando, há uma interface gráfica em Streamlit
(`scripts_python/interface.py`) que permite, pelo navegador:

- **Visualizar Tabelas** — escolher uma tabela e ver seu conteúdo;
- **Executar CRUDs e Consultas Básicas** — rodar, uma a uma, as consultas do `CRUD_Consultas.sql`;
- **Executar Consultas Analíticas** — rodar as 4 consultas do `consultas_analiticas.sql`;
- **SQL Livre** — escrever e executar qualquer comando SQL;
- **RESETAR DATABASE** — recriar e popular o banco do zero (DROP + CREATE + INSERT).

Nas telas de **CRUDs** e de **Consultas Analíticas**, a consulta escolhida aparece já
preenchida num editor de texto e **pode ser alterada antes de executar** — dá para trocar
um nome, um filtro ou reescrever a consulta inteira. Cada consulta guarda a sua própria
edição, então trocar de consulta e voltar não perde o que foi escrito; o botão
**"Restaurar consulta original"** traz de volta o texto do arquivo `.sql`.

Na tela **SQL Livre**, o editor começa em branco e aceita qualquer comando (`SELECT`,
`INSERT`, `UPDATE`, `DELETE`, DDL). Por padrão, vários comandos separados por `;` são
executados em sequência e o resultado de cada um é exibido. Marque
**"Executar como bloco único"** para mandar o texto inteiro de uma vez — necessário para
comandos que têm `;` dentro do corpo, como `CREATE FUNCTION ... $$ ... $$ LANGUAGE plpgsql;`.

A interface depende do `streamlit` e do `pandas` (já incluídos no `requirements.txt`) e usa
as mesmas credenciais definidas no `sgbd.py`. Rode a partir da raiz do projeto:
```bash
streamlit run scripts_python/interface.py
```
A aplicação abre no navegador (por padrão em <http://localhost:8501>).

> **Observação:** na tela "CRUDs e Consultas Básicas", os comandos formam uma sequência —
> execute-os na ordem em que aparecem (ex.: inserir o atendimento antes de registrar os
> procedimentos dele), senão alguns comandos falham por dependência de dados.

