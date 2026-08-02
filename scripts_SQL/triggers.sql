CREATE OR REPLACE FUNCTION fn_check_sobreposicao_escala()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'UPDATE' THEN
        IF EXISTS (
            SELECT 1
            FROM ESCALA_PLANTAO e
            WHERE e.dia_semana = NEW.dia_semana
              AND e.turno = NEW.turno
              AND e.id_residente = NEW.id_residente
              AND e.id_unidade <> NEW.id_unidade
              AND e.id_escala <> OLD.id_escala
        ) THEN
            RAISE EXCEPTION 'O residente % já está escalado para % / % em outra unidade.',
                NEW.id_residente, NEW.dia_semana, NEW.turno;
        END IF;
    ELSE
        IF EXISTS (
            SELECT 1
            FROM ESCALA_PLANTAO e
            WHERE e.dia_semana = NEW.dia_semana
              AND e.turno = NEW.turno
              AND e.id_residente = NEW.id_residente
              AND e.id_unidade <> NEW.id_unidade
        ) THEN
            RAISE EXCEPTION 'O residente % já está escalado para % / % em outra unidade.',
                NEW.id_residente, NEW.dia_semana, NEW.turno;
        END IF;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION fn_audita_atendimento()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        INSERT INTO AUDITORIA_ATENDIMENTO (
            id_atendimento,
            operacao,
            usuario,
            data_hora,
            dados_antigos,
            dados_novos
        )
        VALUES (
            NEW.id_atendimento,
            'INSERT',
            current_user,
            CURRENT_TIMESTAMP,
            NULL,
            to_jsonb(NEW)
        );
        RETURN NEW;
    ELSIF TG_OP = 'UPDATE' THEN
        INSERT INTO AUDITORIA_ATENDIMENTO (
            id_atendimento,
            operacao,
            usuario,
            data_hora,
            dados_antigos,
            dados_novos
        )
        VALUES (
            NEW.id_atendimento,
            'UPDATE',
            current_user,
            CURRENT_TIMESTAMP,
            to_jsonb(OLD),
            to_jsonb(NEW)
        );
        RETURN NEW;
    ELSIF TG_OP = 'DELETE' THEN
        INSERT INTO AUDITORIA_ATENDIMENTO (
            id_atendimento,
            operacao,
            usuario,
            data_hora,
            dados_antigos,
            dados_novos
        )
        VALUES (
            OLD.id_atendimento,
            'DELETE',
            current_user,
            CURRENT_TIMESTAMP,
            to_jsonb(OLD),
            NULL
        );
        RETURN OLD;
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION fn_atualiza_media_procedimentos()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE PROCEDIMENTO
    SET media_tempo_procedimento = (
        SELECT ROUND(AVG(tempo_real_gasto)::numeric, 2)
        FROM ATENDIMENTO_PROCEDIMENTO
        WHERE id_procedimento = NEW.id_procedimento
    )
    WHERE id_procedimento = NEW.id_procedimento;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_check_sobreposicao_escala ON ESCALA_PLANTAO;
CREATE TRIGGER trg_check_sobreposicao_escala
BEFORE INSERT OR UPDATE ON ESCALA_PLANTAO
FOR EACH ROW
EXECUTE FUNCTION fn_check_sobreposicao_escala();

DROP TRIGGER IF EXISTS trg_audita_atendimento ON ATENDIMENTO;
CREATE TRIGGER trg_audita_atendimento
AFTER INSERT OR UPDATE OR DELETE ON ATENDIMENTO
FOR EACH ROW
EXECUTE FUNCTION fn_audita_atendimento();

DROP TRIGGER IF EXISTS trg_atualiza_media_procedimentos ON ATENDIMENTO_PROCEDIMENTO;
CREATE TRIGGER trg_atualiza_media_procedimentos
AFTER INSERT ON ATENDIMENTO_PROCEDIMENTO
FOR EACH ROW
EXECUTE FUNCTION fn_atualiza_media_procedimentos();
