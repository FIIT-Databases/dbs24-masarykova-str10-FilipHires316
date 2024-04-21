--overlap

CREATE OR REPLACE FUNCTION time_overlap(zaciatok TIMESTAMP WITHOUT TIME ZONE, koniec TIMESTAMP WITHOUT TIME ZONE, new_zaciatok TIMESTAMP WITHOUT TIME ZONE, new_koniec TIMESTAMP WITHOUT TIME ZONE)
RETURNS BOOLEAN AS $$
BEGIN
    IF (zaciatok, koniec) OVERLAPS (new_zaciatok, new_koniec) OR (new_zaciatok, new_koniec) OVERLAPS (zaciatok, koniec) THEN RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END;
$$ LANGUAGE plpgsql;