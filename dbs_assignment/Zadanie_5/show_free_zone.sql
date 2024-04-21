--show_free_zone

CREATE OR REPLACE FUNCTION show_free_zone(od TIMESTAMP WITHOUT TIME ZONE, doo TIMESTAMP WITHOUT TIME ZONE)
RETURNS TABLE (
    meno VARCHAR,
    rozloha INT
   )
LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT zony.meno, zony.rozloha FROM zony
LEFT JOIN expozicie_zony ON zony.id = zonyid
LEFT JOIN expozicie ON expozicieid = expozicie.id
WHERE NOT time_overlap('2024-04-01', '2024-07-01', expozicie.zaciatok, expozicie.koniec);
END;
$$;