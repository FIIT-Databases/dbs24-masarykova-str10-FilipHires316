--show_ex

CREATE OR REPLACE FUNCTION show_ex(VARIADIC kateg VARCHAR[])
RETURNS TABLE (
    meno VARCHAR,
    kategorie VARCHAR[]
   )
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT exemplare.meno,
           array_agg(kategorie.meno)
    FROM kategorie 
    JOIN exemplare_kategorie ON kategorie.id = exemplare_kategorie.kategorieid
    JOIN exemplare ON exemplare_kategorie.exemplareid = exemplare.id
    WHERE exemplare.id IN (SELECT exemplareid FROM exemplare_kategorie WHERE kategorieid IN (SELECT id FROM kategorie WHERE kategorie.meno = ANY(kateg)))
    GROUP BY exemplare.meno;
END;
$$;