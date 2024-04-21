CREATE OR REPLACE FUNCTION check_expozicia() 
RETURNS TRIGGER AS $$
DECLARE
    zony_exists BOOLEAN;
BEGIN
--skontroluje sa či v zóne prebieha expozícia
    SELECT EXISTS (
        SELECT expozicie.id FROM zony
	JOIN expozicie_zony ON zony.id = expozicie_zony.zonyid
	JOIN expozicie ON expozicie_zony.expozicieid = expozicie.id
	WHERE time_overlap(expozicie.zaciatok, expozicie.koniec, NEW.zaciatok, NEW.koniec) AND zony.id = NEW.zonyid AND expozicie.status != 'zrusene' 
    ) INTO zony_exists;
    IF zony_exists THEN
--ak áno skontroluje sa ci exemplar nie je v danom čase inde
        INSERT INTO stav (drzitel, zaciatok, koniec, stav, status, exemplareid) 
        VALUES ('Moje Muzeum', NEW.zaciatok, NEW.koniec, 'vystavene', NEW.status, NEW.exemplareid);
--ak nie vloži sa záznam o vystavení v expozícii
	INSERT INTO exemplare_expozicie(exemplareid, expozicieid) VALUES
	(NEW.exemplareid, (SELECT expozicie.id FROM zony
	JOIN expozicie_zony ON zony.id = expozicie_zony.zonyid
	JOIN expozicie ON expozicie_zony.expozicieid = expozicie.id
	WHERE time_overlap(expozicie.zaciatok, expozicie.koniec, NEW.zaciatok, NEW.koniec) AND zony.id = NEW.zonyid AND expozicie.status != 'zrusene'));
	RETURN NEW;
    ELSE
        RAISE EXCEPTION 'Zonyid neexistuje vo vyfiltrovanom zozname';
        RETURN NULL;
    END IF;
EXCEPTION
    WHEN others THEN
        RAISE EXCEPTION 'Chyba';
        RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER before_insert_update_exemplare_zony
BEFORE INSERT OR UPDATE ON public.exemplare_zony
FOR EACH ROW
EXECUTE FUNCTION check_expozicia();