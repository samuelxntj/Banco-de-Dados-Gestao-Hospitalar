from datetime import datetime, date
from sqlalchemy import select, func, delete, update, extract, not_, case
from sqlalchemy.orm import aliased, selectinload
from bd import SessionLocal
from models import (
    Pessoa, Paciente, Profissional, Residente, Preceptor,
    Unidade, Procedimento, Atendimento, AtendimentoProcedimento,
    EscalaPlantao
)

def executar_todas_consultas_orm():
    with SessionLocal() as session:
        try:
            print("1. CONSULTAS DO CRUD BÁSICO DA ETAPA 1 VIA ORM DSL")

            # C1: Inserir um novo atendimento via ORM ---
            # Busca as referências dos objetos necessários via DSL
            pacient_light = session.scalars(
                select(Paciente).join(Pessoa).where(Pessoa.nome == "Light Yagami", Pessoa.dt_nascimento == date(1986, 2, 28))
            ).first()

            residente_lucas = session.scalars(
                select(Residente).join(Profissional).where(Profissional.crm == "11223-PB", Residente.dt_fim.is_(None))
            ).first()

            preceptor_camila = session.scalars(
                select(Preceptor).join(Profissional).where(Profissional.crm == "4004-PB", Preceptor.dt_fim.is_(None))
            ).first()

            unidade_amb = session.scalars(
                select(Unidade).where(Unidade.nome == "AMBULATORIO")
            ).first()

            if pacient_light and residente_lucas and preceptor_camila and unidade_amb:
                novo_atendimento = Atendimento(
                    data_hora=datetime(2026, 7, 7, 8, 30, 0),
                    duracao_minutos=45,
                    id_paciente=pacient_light.id_pessoa,
                    id_residente=residente_lucas.id_pessoa,
                    dt_inicio_residente=residente_lucas.dt_inicio,
                    id_preceptor=preceptor_camila.id_pessoa,
                    dt_inicio_preceptor=preceptor_camila.dt_inicio,
                    id_unidade=unidade_amb.id_unidade
                )
                session.add(novo_atendimento)
                session.flush() # Atribui o ID na sessão sem efetivar a transação
                print(f"[INSERT] Novo atendimento inserido via ORM ID: {novo_atendimento.id_atendimento}")


            # C2: Listar atendimentos do paciente 'Light Yagami' ---
            stmt_atend_light = (
                select(Atendimento)
                .join(Paciente, Atendimento.id_paciente == Paciente.id_pessoa)
                .join(Pessoa, Paciente.id_pessoa == Pessoa.id_pessoa)
                .where(Pessoa.nome == "Light Yagami")
                .order_by(Atendimento.data_hora.asc())
            )
            atendimentos_light = session.scalars(stmt_atend_light).all()
            print(f"[SELECT] Total de atendimentos de Light Yagami: {len(atendimentos_light)}")


            # C3: Listar os procedimentos realizados nos atendimentos do paciente ---
            stmt_procs_light = (
                select(AtendimentoProcedimento)
                .join(Atendimento, AtendimentoProcedimento.id_atendimento == Atendimento.id_atendimento)
                .join(Paciente, Atendimento.id_paciente == Paciente.id_pessoa)
                .join(Pessoa, Paciente.id_pessoa == Pessoa.id_pessoa)
                .where(Pessoa.nome == "Light Yagami")
            )
            procs_light = session.scalars(stmt_procs_light).all()
            print(f"[SELECT] Procedimentos do paciente Light Yagami: {len(procs_light)} encontrado(s)")


            # C4: Atualizar o convênio de um paciente
            stmt_upd = (
                update(Paciente)
                .where(Paciente.id_pessoa == select(Pessoa.id_pessoa).where(Pessoa.nome == "Light Yagami").scalar_subquery())
                .values(num_convenio="KIRA-999")
            )
            session.execute(stmt_upd)
            print("[UPDATE] Convênio de Light Yagami atualizado para 'KIRA-999'")


            # C5: Remover um procedimento realizado não faturado
            subq_proc = select(Procedimento.id_procedimento).where(Procedimento.codigo == "PROC-001").scalar_subquery()
            if pacient_light:
                stmt_del = (
                    delete(AtendimentoProcedimento)
                    .where(
                        AtendimentoProcedimento.id_procedimento == subq_proc,
                        AtendimentoProcedimento.is_faturado == False,
                        AtendimentoProcedimento.id_atendimento.in_(
                            select(Atendimento.id_atendimento).where(
                                Atendimento.id_paciente == pacient_light.id_pessoa,
                                Atendimento.data_hora == datetime(2026, 7, 7, 8, 30, 0)
                            )
                        )
                    )
                )
                res_del = session.execute(stmt_del)
                print(f"[DELETE] Expurgo de procedimento efetuado com sucesso. Linhas afetadas: {res_del.rowcount}")


            # C6: Tempo médio de duração por residente
            stmt_avg_residente = (
                select(
                    Pessoa.nome.label("nome_residente"),
                    func.round(func.avg(Atendimento.duracao_minutos), 2).label("media_duracao_minutos")
                )
                .select_from(Residente)
                .join(Pessoa, Residente.id_pessoa == Pessoa.id_pessoa)
                .outerjoin(Atendimento, (Atendimento.id_residente == Residente.id_pessoa) & (Atendimento.dt_inicio_residente == Residente.dt_inicio))
                .group_by(Pessoa.id_pessoa, Pessoa.nome)
                .order_by(func.avg(Atendimento.duracao_minutos).desc().nullslast())
            )
            print("\n[SELECT AGGREGATE] Tempo médio por Residente:")
            for row in session.execute(stmt_avg_residente).all():
                print(f"  - Residente: {row.nome_residente} | Média: {row.media_duracao_minutos} min")


            print("\n")
            print("2. CONSULTAS ANALÍTICAS E RELATÓRIOS DA ETAPA 1 VIA ORM")

            # Q1: Ranking dos residentes por número de atendimentos
            stmt_rank_residente = (
                select(
                    Pessoa.nome,
                    func.count(Atendimento.id_residente).label("quantidade_atendimentos")
                )
                .select_from(Residente)
                .join(Pessoa, Residente.id_pessoa == Pessoa.id_pessoa)
                .outerjoin(Atendimento, Atendimento.id_residente == Pessoa.id_pessoa)
                .group_by(Pessoa.nome)
                .order_by(func.count(Atendimento.id_residente).desc())
            )
            print("\n[ANALÍTICA 1] Ranking de Residentes:")
            for row in session.execute(stmt_rank_residente).all():
                print(f"  - {row.nome}: {row.quantidade_atendimentos} atendimentos")


            # Q2: Preceptores com mais de 5 atendimentos em Julho/2026
            stmt_preceptores_top = (
                select(
                    Pessoa.nome,
                    func.count(Atendimento.id_preceptor).label("quantidade_atendimentos")
                )
                .join(Atendimento, Atendimento.id_preceptor == Pessoa.id_pessoa)
                .where(
                    extract("month", Atendimento.data_hora) == 7,
                    extract("year", Atendimento.data_hora) == 2026
                )
                .group_by(Pessoa.nome)
                .having(func.count(Atendimento.id_preceptor) > 5)
                .order_by(func.count(Atendimento.id_preceptor).desc())
            )
            print("\n[ANALÍTICA 2] Preceptores com > 5 atendimentos em 07/2026:")
            for row in session.execute(stmt_preceptores_top).all():
                print(f"  - {row.nome}: {row.quantidade_atendimentos} atendimentos")


            # Q3: Quantidade de plantões escalados por residente por unidade
            stmt_plantoes = (
                select(
                    Unidade.nome.label("unidade"),
                    Pessoa.nome.label("residente"),
                    func.count(EscalaPlantao.id_escala).label("quantidade_plantoes")
                )
                .join(Unidade, Unidade.id_unidade == EscalaPlantao.id_unidade)
                .join(Pessoa, Pessoa.id_pessoa == EscalaPlantao.id_residente)
                .group_by(Unidade.nome, Pessoa.nome)
                .order_by(Unidade.nome, func.count(EscalaPlantao.id_escala).desc(), Pessoa.nome)
            )
            print("\n[ANALÍTICA 3] Plantões por Unidade/Residente:")
            for row in session.execute(stmt_plantoes).all():
                print(f"  - Unidade: {row.unidade} | Residente: {row.residente} | Plantões: {row.quantidade_plantoes}")


            # Q4: Pacientes que NUNCA realizaram procedimentos de risco 'ALTO'
            subq_alto_risco = (
                select(Atendimento.id_paciente)
                .join(AtendimentoProcedimento, AtendimentoProcedimento.id_atendimento == Atendimento.id_atendimento)
                .join(Procedimento, Procedimento.id_procedimento == AtendimentoProcedimento.id_procedimento)
                .where(Procedimento.nivel_risco == "ALTO")
                .scalar_subquery()
            )

            stmt_pacientes_seguros = (
                select(Pessoa.nome)
                .join(Paciente, Paciente.id_pessoa == Pessoa.id_pessoa)
                .where(not_(Paciente.id_pessoa.in_(subq_alto_risco)))
                .order_by(Pessoa.nome)
            )
            print("\n[ANALÍTICA 4] Pacientes sem procedimentos de risco ALTO:")
            for row in session.execute(stmt_pacientes_seguros).all():
                print(f"  - {row.nome}")

            print("\n")
            print("3. CONSULTAS AVANÇADAS VIA ORM")

            # Demonstração de lazy loading vs eager loading
            atendimento_exemplo = session.scalar(select(Atendimento).where(Atendimento.id_atendimento == 1))
            print("[LAZY] Lista de procedimentos carregada sob demanda:")
            print(f"  - Atendimento {atendimento_exemplo.id_atendimento}: {len(atendimento_exemplo.procedimentos_associados)} procedimento(s)")

            atendimento_eager = session.scalar(
                select(Atendimento)
                .options(
                    selectinload(Atendimento.procedimentos_associados)
                    .selectinload(AtendimentoProcedimento.procedimento)
                )
                .where(Atendimento.id_atendimento == 1)
            )
            print("[EAGER] Lista de procedimentos carregada com selectinload:")
            print(f"  - Atendimento {atendimento_eager.id_atendimento}: {len(atendimento_eager.procedimentos_associados)} procedimento(s)")

            # Q5: Preceptores que supervisionaram residentes que atenderam pacientes flamenguistas
            PessoaPaciente = aliased(Pessoa)
            stmt_preceptores_flamenguistas = (
                select(Pessoa.nome.label("preceptor"))
                .join(Preceptor, Preceptor.id_pessoa == Pessoa.id_pessoa)
                .join(Atendimento, Atendimento.id_preceptor == Preceptor.id_pessoa)
                .join(Paciente, Atendimento.id_paciente == Paciente.id_pessoa)
                .join(PessoaPaciente, Paciente.id_pessoa == PessoaPaciente.id_pessoa)
                .where(PessoaPaciente.is_flamengo.is_(True))
                .distinct()
                .order_by(Pessoa.nome)
            )
            print("\n[AVANÇADA 1] Preceptores que supervisionaram atendimentos de pacientes flamenguistas:")
            for row in session.execute(stmt_preceptores_flamenguistas).all():
                print(f"  - {row.preceptor}")

            # Q6: Último atendimento de cada paciente com residente, preceptor e procedimentos
            PessoaResidente = aliased(Pessoa)
            PessoaPreceptor = aliased(Pessoa)

            subq_ultimo_atendimento = (
                select(
                    Atendimento.id_paciente.label("id_paciente"),
                    func.max(Atendimento.data_hora).label("ultima_data")
                )
                .group_by(Atendimento.id_paciente)
                .subquery()
            )

            stmt_ultimo_atendimento = (
                select(
                    Pessoa.nome.label("paciente"),
                    Atendimento.data_hora,
                    PessoaResidente.nome.label("residente"),
                    PessoaPreceptor.nome.label("preceptor")
                )
                .join(Paciente, Paciente.id_pessoa == Pessoa.id_pessoa)
                .join(subq_ultimo_atendimento, subq_ultimo_atendimento.c.id_paciente == Paciente.id_pessoa)
                .join(Atendimento, (Atendimento.id_paciente == subq_ultimo_atendimento.c.id_paciente) & (Atendimento.data_hora == subq_ultimo_atendimento.c.ultima_data))
                .join(Residente, (Residente.id_pessoa == Atendimento.id_residente) & (Residente.dt_inicio == Atendimento.dt_inicio_residente))
                .join(PessoaResidente, PessoaResidente.id_pessoa == Residente.id_pessoa)
                .join(Preceptor, (Preceptor.id_pessoa == Atendimento.id_preceptor) & (Preceptor.dt_inicio == Atendimento.dt_inicio_preceptor))
                .join(PessoaPreceptor, PessoaPreceptor.id_pessoa == Preceptor.id_pessoa)
                .order_by(Pessoa.nome)
            )

            print("\n[AVANÇADA 2] Último atendimento de cada paciente:")
            ultimo_atendimentos = session.execute(stmt_ultimo_atendimento).all()
            for row in ultimo_atendimentos:
                atendimento_obj = session.scalar(
                    select(Atendimento)
                    .where(
                        Atendimento.id_paciente == select(Paciente.id_pessoa)
                        .where(Pessoa.nome == row.paciente)
                        .scalar_subquery(),
                        Atendimento.data_hora == row.data_hora,
                    )
                )
                procedimentos = [
                    f"{ap.procedimento.nome} ({ap.qtd_executada}x)"
                    for ap in atendimento_obj.procedimentos_associados
                ] if atendimento_obj else []
                print(f"  - Paciente: {row.paciente} | Data: {row.data_hora} | Residente: {row.residente} | Preceptor: {row.preceptor} | Procedimentos: {procedimentos}")

            # Q7: Percentual de procedimentos de alto risco por residente
            stmt_percentual_alto_risco = (
                select(
                    Pessoa.nome.label("residente"),
                    func.count(AtendimentoProcedimento.id_procedimento).label("total_procedimentos"),
                    func.sum(case((Procedimento.nivel_risco == "ALTO"), 1, else_=0)).label("procedimentos_alto_risco")
                )
                .select_from(Residente)
                .join(Pessoa, Pessoa.id_pessoa == Residente.id_pessoa)
                .join(Atendimento, (Atendimento.id_residente == Residente.id_pessoa) & (Atendimento.dt_inicio_residente == Residente.dt_inicio))
                .join(AtendimentoProcedimento, AtendimentoProcedimento.id_atendimento == Atendimento.id_atendimento)
                .join(Procedimento, Procedimento.id_procedimento == AtendimentoProcedimento.id_procedimento)
                .group_by(Pessoa.id_pessoa, Pessoa.nome)
                .order_by(Pessoa.nome)
            )
            print("\n[AVANÇADA 3] Percentual de procedimentos de alto risco por residente:")
            for row in session.execute(stmt_percentual_alto_risco).all():
                percentual = round((row.procedimentos_alto_risco / row.total_procedimentos) * 100, 2) if row.total_procedimentos else 0.0
                print(f"  - {row.residente}: {percentual}% ({row.procedimentos_alto_risco}/{row.total_procedimentos})")

            # Efetiva as transações no banco
            session.commit()
            print("\nTodas as 10 consultas executadas e validadas via ORM com sucesso!")

        except Exception as e:
            session.rollback()
            print(f"Erro na execução das consultas em ORM: {e}")

if __name__ == "__main__":
    executar_todas_consultas_orm()