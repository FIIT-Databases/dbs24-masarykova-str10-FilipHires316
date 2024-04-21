--new_expo

CREATE OR REPLACE PROCEDURE new_expo(nazov VARCHAR, od TIMESTAMP WITHOUT TIME ZONE, doo TIMESTAMP WITHOUT TIME ZONE, stat enum, VARIADIC zones VARCHAR[])
LANGUAGE plpgsql AS $$
DECLARE zone VARCHAR;
BEGIN
	INSERT INTO expozicie (meno, zaciatok, koniec, status) VALUES
		(nazov, od, doo, stat);
	FOREACH zone IN ARRAY zones
	LOOP
		INSERT INTO expozicie_zony(expozicieid, zonyid) VALUES
			((SELECT id FROM expozicie WHERE meno = nazov), (SELECT id FROM zony WHERE meno = zone));
	END LOOP;
END;
$$;