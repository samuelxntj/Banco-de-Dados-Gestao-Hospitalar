from datetime import datetime, date
from typing import List, Optional

from sqlalchemy import (
    String, Integer, Boolean, Date, DateTime, Numeric, Text,
    ForeignKey, ForeignKeyConstraint, CheckConstraint, UniqueConstraint, PrimaryKeyConstraint
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

# Classe Base Declarativa do SQLAlchemy 2.0
class Base(DeclarativeBase):
    pass


# HIERARQUIA DE PESSOAS (Joined Table Inheritance)

class Pessoa(Base):
    __tablename__ = "pessoa"

    id_pessoa: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    dt_nascimento: Mapped[date] = mapped_column(Date, nullable=False)
    is_flamengo: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Flags de controle de especialização (Herança)
    is_paciente: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    is_profissional: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    __table_args__ = (
        UniqueConstraint("id_pessoa", "is_paciente", "is_profissional", name="un_pessoa_heranca"),
        CheckConstraint("is_paciente = TRUE OR is_profissional = TRUE", name="ck_pessoa_especializacao"),
    )

    # Relacionamentos
    telefones: Mapped[List["Telefone"]] = relationship(back_populates="pessoa", cascade="all, delete-orphan")
    paciente: Mapped[Optional["Paciente"]] = relationship(back_populates="pessoa", uselist=False)
    profissional: Mapped[Optional["Profissional"]] = relationship(back_populates="pessoa", uselist=False)


class Paciente(Base):
    __tablename__ = "paciente"

    id_pessoa: Mapped[int] = mapped_column(Integer, primary_key=True)
    num_convenio: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    grupo_sanguineo: Mapped[str] = mapped_column(String(3), nullable=False)

    # Flags para alinhar com a FK Composta da tabela Pessoa
    is_paciente_flag: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    is_profissional_flag: Mapped[bool] = mapped_column(Boolean, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ["id_pessoa", "is_paciente_flag", "is_profissional_flag"],
            ["pessoa.id_pessoa", "pessoa.is_paciente", "pessoa.is_profissional"],
            ondelete="CASCADE",
            name="fk_paciente_pessoa"
        ),
        CheckConstraint("is_paciente_flag = TRUE", name="ck_paciente_flag_true"),
    )

    # Relacionamentos
    pessoa: Mapped["Pessoa"] = relationship(back_populates="paciente")
    atendimentos: Mapped[List["Atendimento"]] = relationship(back_populates="paciente")
    alergias_paciente: Mapped[List["AlergiaPaciente"]] = relationship(back_populates="paciente", cascade="all, delete-orphan")


class Profissional(Base):
    __tablename__ = "profissional"

    id_pessoa: Mapped[int] = mapped_column(Integer, primary_key=True)
    crm: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    dt_admissao: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    especialidade: Mapped[str] = mapped_column(String(100), nullable=False)

    is_paciente_flag: Mapped[bool] = mapped_column(Boolean, nullable=False)
    is_profissional_flag: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ["id_pessoa", "is_paciente_flag", "is_profissional_flag"],
            ["pessoa.id_pessoa", "pessoa.is_paciente", "pessoa.is_profissional"],
            ondelete="CASCADE",
            name="fk_profissional_pessoa"
        ),
        CheckConstraint("is_profissional_flag = TRUE", name="ck_profissional_flag_true"),
    )

    # Relacionamentos
    pessoa: Mapped["Pessoa"] = relationship(back_populates="profissional")
    historico_residente: Mapped[List["Residente"]] = relationship(back_populates="profissional", cascade="all, delete-orphan")
    historico_preceptor: Mapped[List["Preceptor"]] = relationship(back_populates="profissional", cascade="all, delete-orphan")


class Residente(Base):
    __tablename__ = "residente"

    id_pessoa: Mapped[int] = mapped_column(Integer, ForeignKey("profissional.id_pessoa", ondelete="CASCADE"), primary_key=True)
    dt_inicio: Mapped[datetime] = mapped_column(DateTime, primary_key=True)
    dt_fim: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    ano_residencia: Mapped[str] = mapped_column(String(2), nullable=False)

    __table_args__ = (
        CheckConstraint("ano_residencia IN ('R1', 'R2', 'R3')", name="ck_ano_residencia"),
        CheckConstraint("dt_fim IS NULL OR dt_fim >= dt_inicio", name="ck_residente_datas"),
    )

    # Relacionamentos
    profissional: Mapped["Profissional"] = relationship(back_populates="historico_residente")
    atendimentos: Mapped[List["Atendimento"]] = relationship(back_populates="residente")
    escala_plantoes: Mapped[List["EscalaPlantao"]] = relationship(back_populates="residente")


class Preceptor(Base):
    __tablename__ = "preceptor"

    id_pessoa: Mapped[int] = mapped_column(Integer, ForeignKey("profissional.id_pessoa", ondelete="CASCADE"), primary_key=True)
    dt_inicio: Mapped[datetime] = mapped_column(DateTime, primary_key=True)
    dt_fim: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    titulacao: Mapped[str] = mapped_column(String(20), nullable=False)

    __table_args__ = (
        CheckConstraint("dt_fim IS NULL OR dt_fim >= dt_inicio", name="ck_preceptor_datas"),
    )

    # Relacionamentos
    profissional: Mapped["Profissional"] = relationship(back_populates="historico_preceptor")
    atendimentos: Mapped[List["Atendimento"]] = relationship(back_populates="preceptor")
    escala_plantoes: Mapped[List["EscalaPlantao"]] = relationship(back_populates="preceptor")



# TABELAS DE APOIO (Telefone e Alergias)

class Telefone(Base):
    __tablename__ = "telefone"

    id_pessoa: Mapped[int] = mapped_column(Integer, ForeignKey("pessoa.id_pessoa", ondelete="CASCADE"), primary_key=True)
    num_telefone: Mapped[str] = mapped_column(String(20), primary_key=True)

    pessoa: Mapped["Pessoa"] = relationship(back_populates="telefones")


class Alergia(Base):
    __tablename__ = "alergia"

    id_alergia: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome_alergia: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    alergias_paciente: Mapped[List["AlergiaPaciente"]] = relationship(back_populates="alergia", cascade="all, delete-orphan")


class AlergiaPaciente(Base):
    __tablename__ = "alergia_paciente"

    id_pessoa: Mapped[int] = mapped_column(Integer, ForeignKey("paciente.id_pessoa", ondelete="CASCADE"), primary_key=True)
    id_alergia: Mapped[int] = mapped_column(Integer, ForeignKey("alergia.id_alergia", ondelete="RESTRICT"), primary_key=True)

    paciente: Mapped["Paciente"] = relationship(back_populates="alergias_paciente")
    alergia: Mapped["Alergia"] = relationship(back_populates="alergias_paciente")



# OPERACIONAL (Unidade, Procedimento, Atendimento e Escalas)

class Unidade(Base):
    __tablename__ = "unidade"

    id_unidade: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    escala_plantoes: Mapped[List["EscalaPlantao"]] = relationship(back_populates="unidade")


class Procedimento(Base):
    __tablename__ = "procedimento"

    id_procedimento: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    codigo: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    nome: Mapped[str] = mapped_column(String(100), nullable=False)
    tempo_medio_execucao: Mapped[int] = mapped_column(Integer, nullable=False)
    nivel_risco: Mapped[str] = mapped_column(String(10), default="BAIXO", nullable=False)

    atendimentos_procedimentos: Mapped[List["AtendimentoProcedimento"]] = relationship(back_populates="procedimento")


class Atendimento(Base):
    __tablename__ = "atendimento"

    id_atendimento: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    data_hora: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    duracao_minutos: Mapped[int] = mapped_column(Integer, nullable=False)
    
    id_paciente: Mapped[int] = mapped_column(Integer, ForeignKey("paciente.id_pessoa", ondelete="RESTRICT"), nullable=False)
    
    # Chaves estrangeiras compostas para respeitar a chave primária de Residente e Preceptor (Histórico)
    id_residente: Mapped[int] = mapped_column(Integer, nullable=False)
    dt_inicio_residente: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    id_preceptor: Mapped[int] = mapped_column(Integer, nullable=False)
    dt_inicio_preceptor: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ["id_residente", "dt_inicio_residente"],
            ["residente.id_pessoa", "residente.dt_inicio"],
            ondelete="RESTRICT",
            name="fk_atendimento_residente"
        ),
        ForeignKeyConstraint(
            ["id_preceptor", "dt_inicio_preceptor"],
            ["preceptor.id_pessoa", "preceptor.dt_inicio"],
            ondelete="RESTRICT",
            name="fk_atendimento_preceptor"
        ),
    )

    # Relacionamentos
    paciente: Mapped["Paciente"] = relationship(back_populates="atendimentos")
    residente: Mapped["Residente"] = relationship(back_populates="atendimentos")
    preceptor: Mapped["Preceptor"] = relationship(back_populates="atendimentos")
    procedimentos_associados: Mapped[List["AtendimentoProcedimento"]] = relationship(
        back_populates="atendimento", cascade="all, delete-orphan"
    )


class AtendimentoProcedimento(Base):
    __tablename__ = "atendimento_procedimento"

    id_atendimento: Mapped[int] = mapped_column(Integer, ForeignKey("atendimento.id_atendimento", ondelete="CASCADE"), primary_key=True)
    id_procedimento: Mapped[int] = mapped_column(Integer, ForeignKey("procedimento.id_procedimento", ondelete="RESTRICT"), primary_key=True)
    
    qtd_executada: Mapped[int] = mapped_column(Integer, default=1, nullable=False)
    tempo_real_gasto: Mapped[int] = mapped_column(Integer, nullable=False)
    observacao_intercorrencias: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_faturado: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relacionamentos
    atendimento: Mapped["Atendimento"] = relationship(back_populates="procedimentos_associados")
    procedimento: Mapped["Procedimento"] = relationship(back_populates="atendimentos_procedimentos")


class EscalaPlantao(Base):
    __tablename__ = "escala_plantao"

    id_escala: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    dia_semana: Mapped[str] = mapped_column(String(15), nullable=False)
    turno: Mapped[str] = mapped_column(String(10), nullable=False)
    
    id_unidade: Mapped[int] = mapped_column(Integer, ForeignKey("unidade.id_unidade", ondelete="RESTRICT"), nullable=False)
    
    id_residente: Mapped[int] = mapped_column(Integer, nullable=False)
    dt_inicio_residente: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    id_preceptor: Mapped[int] = mapped_column(Integer, nullable=False)
    dt_inicio_preceptor: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(
            ["id_residente", "dt_inicio_residente"],
            ["residente.id_pessoa", "residente.dt_inicio"],
            ondelete="RESTRICT",
            name="fk_escala_residente"
        ),
        ForeignKeyConstraint(
            ["id_preceptor", "dt_inicio_preceptor"],
            ["preceptor.id_pessoa", "preceptor.dt_inicio"],
            ondelete="RESTRICT",
            name="fk_escala_preceptor"
        ),
        UniqueConstraint("id_unidade", "dia_semana", "turno", "id_residente", name="un_escala_residente_turno"),
        CheckConstraint("dia_semana IN ('SEGUNDA', 'TERCA', 'QUARTA', 'QUINTA', 'SEXTA', 'SABADO', 'DOMINGO')", name="ck_dia_semana"),
        CheckConstraint("turno IN ('MANHA', 'TARDE', 'NOITE')", name="ck_turno"),
    )

    # Relacionamentos
    unidade: Mapped["Unidade"] = relationship(back_populates="escala_plantoes")
    residente: Mapped["Residente"] = relationship(back_populates="escala_plantoes")
    preceptor: Mapped["Preceptor"] = relationship(back_populates="escala_plantoes")