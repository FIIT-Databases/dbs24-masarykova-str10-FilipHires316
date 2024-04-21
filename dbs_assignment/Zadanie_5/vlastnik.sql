--vlastnik

CREATE OR REPLACE FUNCTION check_vlastnik()
RETURNS TRIGGER AS $$
BEGIN
--Overí sa či exemplár v čase nevlastní niekto iný
    IF EXISTS (
        SELECT 1
        FROM public.vlastnik_exemplare ve
        WHERE ve.exemplareid = NEW.exemplareid
        AND time_overlap(ve.zaciatok, ve.koniec, NEW.zaciatok, NEW.koniec)
    ) THEN
        RAISE EXCEPTION 'Casy sa prekryvaju';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER before_insert_update_vlastnik_exemplare
BEFORE INSERT OR UPDATE ON public.vlastnik_exemplare
FOR EACH ROW
EXECUTE FUNCTION check_vlastnik();