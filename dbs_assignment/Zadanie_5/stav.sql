--stav

CREATE OR REPLACE FUNCTION check_stav()
RETURNS TRIGGER AS $$
BEGIN
--zistí či exemplár v danom čase nie je niekde inde
    IF EXISTS (
        SELECT 1
        FROM public.stav s
        WHERE s.exemplareid = NEW.exemplareid
        AND time_overlap(s.zaciatok, s.koniec, NEW.zaciatok, NEW.koniec)
        AND s.status <> 'zrusene'
		AND s.id <> NEW.id
    ) THEN
        RAISE EXCEPTION 'Casy sa prekryvaju';
    END IF;
--ak nie je može insert prebehnúť 
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER before_insert_update_stav
BEFORE INSERT OR UPDATE ON public.stav
FOR EACH ROW
EXECUTE FUNCTION check_stav();
