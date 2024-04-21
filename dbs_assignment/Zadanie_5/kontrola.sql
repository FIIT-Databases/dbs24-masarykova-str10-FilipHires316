--kontrola

CREATE OR REPLACE FUNCTION check_kontrola() 
RETURNS TRIGGER AS $$
BEGIN
--skúsi vytvoriť záznam o kontorle v tabulke stav
    INSERT INTO stav (drzitel, zaciatok, koniec, stav, status, exemplareid) VALUES 
        ('Moje Muzeum', NEW.zaciatok, NEW.koniec, 'kontrola', NEW.status, NEW.exemplareid);
--ak sa podarí vytvorí sa záznam o kontrole aj v tabuľke kontroly
    RETURN NEW;
EXCEPTION
    WHEN others THEN
	RAISE EXCEPTION 'Casy sa prekryvaju';
        RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER before_insert_update_kontroly
BEFORE INSERT OR UPDATE ON public.kontroly
FOR EACH ROW
EXECUTE FUNCTION check_kontrola();