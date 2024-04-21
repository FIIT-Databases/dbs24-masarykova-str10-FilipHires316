--new_ex

CREATE OR REPLACE PROCEDURE new_ex(nazov VARCHAR, vl BOOLEAN, po BOOLEAN, majitel VARCHAR, od TIMESTAMP WITHOUT TIME ZONE, doo TIMESTAMP WITHOUT TIME ZONE, VARIADIC kateg VARCHAR[])
LANGUAGE plpgsql AS $$
DECLARE kategoria VARCHAR;
BEGIN
--vytvorí sa nový záznam exempláru
	INSERT INTO exemplare (meno, vlastne, pozicane) VALUES
		(nazov, vl, po);
--ak neexistuje záznam o majiteľovi, vytvorí sa a následne sa prepojí s exemplárom
	IF NOT EXISTS (
		SELECT 1 FROM vlastnik 
		WHERE meno = majitel
		) THEN
		INSERT INTO vlastnik (meno) VALUES
			(majitel);
	END IF;
	INSERT INTO vlastnik_exemplare (exemplareid, vlastnikid, zaciatok, koniec) VALUES
		((SELECT id FROM exemplare WHERE meno = nazov), (SELECT id FROM vlastnik WHERE meno = majitel), od, doo);
--pre každú kategóriu sa vytvorí záznam ak ešte neexistuje a následne sa prepojí s exemplárom
	FOREACH kategoria IN ARRAY kateg
	LOOP
		IF NOT EXISTS (
			SELECT 1 FROM kategorie 
			WHERE meno = kategoria
			) THEN
				INSERT INTO kategorie (meno) VALUES
					(kategoria);
		END IF;
		INSERT INTO exemplare_kategorie (exemplareid, kategorieid) VALUES
		((SELECT id FROM exemplare WHERE meno = nazov), (SELECT id FROM kategorie WHERE meno = kategoria));
	END LOOP;
END;
$$;