--asign_to_expo

CREATE OR REPLACE PROCEDURE asign_to_expo(nazov VARCHAR, zone VARCHAR, VARIADIC exemps VARCHAR[])
LANGUAGE plpgsql AS $$
DECLARE ex VARCHAR;
BEGIN
	FOREACH ex IN ARRAY exemps
	LOOP
		INSERT INTO exemplare_zony(exemplareid, zonyid, zaciatok, koniec, status) VALUES
			((SELECT id FROM exemplare WHERE meno = ex), (SELECT id FROM zony WHERE meno = zone),
			 (SELECT zaciatok FROM expozicie WHERE meno = nazov), (SELECT koniec FROM expozicie WHERE meno = nazov),
			 (SELECT status FROM expozicie WHERE meno = nazov));
	END LOOP;
END;
$$;