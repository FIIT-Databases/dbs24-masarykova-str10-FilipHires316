--zony

CREATE OR REPLACE FUNCTION check_zona()
RETURNS TRIGGER AS $$
DECLARE
    zaciatok1 TIMESTAMP WITHOUT TIME ZONE;
    koniec1 TIMESTAMP WITHOUT TIME ZONE;
    row_data RECORD;
BEGIN
--ovberí sa či zóna nepatrí do inej expozície
    SELECT zaciatok, koniec INTO zaciatok1, koniec1 FROM expozicie
    WHERE expozicie.id = NEW.expozicieid;
    FOR row_data IN 
        SELECT zaciatok, koniec, status
        FROM expozicie_zony
        JOIN expozicie ON expozicieid = expozicie.id
        WHERE zonyid = NEW.zonyid
    LOOP
        IF time_overlap(zaciatok1, koniec1, row_data.zaciatok, row_data.koniec)
	AND row_data.status <> 'zrusene' THEN
        RAISE EXCEPTION 'Casy sa prekrivaju';
    	END IF;
    END LOOP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER before_insert_update_expozicie_zony
BEFORE INSERT OR UPDATE ON public.expozicie_zony
FOR EACH ROW
EXECUTE FUNCTION check_zona();