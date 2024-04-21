-- CALL new_ex('Renesančný obraz', TRUE, FALSE, 'Moje múzeum', '2024-04-21', null, 'novovek', 'renesancia', 'obraz');

-- SELECT exemplare.meno, array_agg(kategorie.meno), vlastnik.meno AS vlastnik FROM exemplare
-- JOIN vlastnik_exemplare on exemplare.id = exemplareid
-- JOIN vlastnik on vlastnik_exemplare.vlastnikid = vlastnik.id
-- JOIN exemplare_kategorie on exemplare.id = exemplare_kategorie.exemplareid
-- JOIN kategorie on kategorieid = kategorie.id
-- GROUP BY(exemplare.meno, vlastnik.meno)

-- SELECT show_ex('stredovek');

-- SELECT show_ex('stredovek', 'novovek')

-- SELECT expozicie.meno, zaciatok, koniec, status, array_agg(zony.meno) AS zony FROM expozicie
-- JOIN expozicie_zony on expozicie.id = expozicieid
-- JOIN zony on expozicie_zony.zonyid = zony.id
-- group by(expozicie.meno, zaciatok, koniec, status)

-- SELECT show_free_zone('2024-03-01', '2024-06-30')

-- CALL new_expo('Stredovek', '2024-03-01', '2024-06-01', 'planovane', 'A', 'B', 'E')

-- CALL new_expo('Stredovek', '2024-03-01', '2024-06-01', 'planovane', 'D', 'B', 'E')

-- CALL asign_to_expo('Výstava zbraní', 'A', 'Meč', 'Štít')

-- CALL new_ex('Egyptská koruna', FALSE, FALSE, 'Múzeum histórie', '2022-02-01', '2024_04-22', 'Egypt', 'Koruna')

-- INSERT INTO vlastnik_exemplare (vlastnikid, exemplareid, zaciatok) VALUES
-- 	(1, 7, '2024-04-23');

-- SELECT * from vlastnik_exemplare