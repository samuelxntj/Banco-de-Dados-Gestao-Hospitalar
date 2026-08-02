# scripts_python/consultas_orm.py
# scripts_python/consultas_orm.py
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

# Importa a fábrica de sessões criada em bd.py
from bd import SessionLocal
# Importa as classes mapeadas do modelo ORM
from models import Pessoa, Paciente, Atendimento, Residente


def testar_consultas_orm():
    try:
        # Cria uma sessão ORM para conversar com o banco
        session = SessionLocal()
        try:
            # Busca simples usando a DSL do SQLAlchemy (sem escrever SQL puro)
            print("\n--- 1. Buscando Paciente via ORM DSL (sem SQL cru) ---")
            stmt = select(Paciente).filter(Paciente.id_pessoa == 5)
            paciente = session.scalar(stmt)
            if paciente:
                # Acesso a atributos relacionados, por exemplo pessoa.nome
                print(f"Paciente: {paciente.pessoa.nome} | Convênio: {paciente.num_convenio}")

            # Atualização de dados dentro de uma transação ORM
            print("\n--- 2. Atualizando Convênio via transação ORM ---")
            if paciente:
                paciente.num_convenio = "KIRA-999"
                session.commit()  # confirma a alteração no banco
                print("Convênio atualizado via ORM com sucesso!")

            # Exemplo de lazy loading: o relacionamento é carregado quando acessado
            print("\n--- 3. Exemplo de lazy loading (acesso posterior à consulta) ---")
            stmt_lazy = select(Paciente).filter(Paciente.id_pessoa == 5)
            paciente_lazy = session.scalar(stmt_lazy)
            if paciente_lazy is not None:
                print(f"Lazy loading: {paciente_lazy.pessoa.nome}")

            # Exemplo de eager loading: carrega os relacionamentos logo na consulta
            print("\n--- 4. Exemplo de eager loading com selectinload ---")
            stmt_eager = (
                select(Paciente)
                .filter(Paciente.id_pessoa == 5)
                .options(selectinload(Paciente.pessoa), selectinload(Paciente.atendimentos))
            )
            paciente_eager = session.scalar(stmt_eager)
            if paciente_eager is not None:
                print(
                    f"Eager loading: {paciente_eager.pessoa.nome} | "
                    f"atendimentos={len(paciente_eager.atendimentos)}"
                )

            # Consulta agregada usando funções do SQLAlchemy, como AVG e ROUND
            print("\n--- 5. Média de duração por residente via ORM DSL ---")
            stmt_media = (
                select(
                    Pessoa.nome,
                    func.round(func.avg(Atendimento.duracao_minutos), 2).label("media_duracao")
                )
                .join(Residente, Atendimento.id_residente == Residente.id_pessoa)
                .join(Pessoa, Residente.id_pessoa == Pessoa.id_pessoa)
                .group_by(Residente.id_pessoa, Pessoa.nome)
            )
            resultados = session.execute(stmt_media).all()
            for nome, media in resultados:
                print(f"Residente: {nome} | Média: {media} min")
        finally:
            # Fecha a sessão ao final para liberar recursos e evitar problemas de transação
            session.close()

    except Exception as erro:
        # Captura qualquer erro de conexão, consulta ou transação
        print(f"Erro ao executar consultas ORM: {erro}")


if __name__ == "__main__":
    testar_consultas_orm()