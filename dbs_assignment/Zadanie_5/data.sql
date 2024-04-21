--data

INSERT INTO exemplare (meno, vlastne, pozicane) VALUES
	('Meč', TRUE, FALSE),
	('Štít', TRUE, FALSE),
	('Delo', TRUE, FALSE),
	('Primitívne nástroje', TRUE, FALSE),
	('Rímska prilba', TRUE, FALSE);
	
INSERT INTO kategorie (meno) VALUES
	('pravek'),
	('starovek'),
	('stredovek'),
	('novovek'),
	('zbraň'),
	('zbroj'),
	('nástroj');
	
INSERT INTO exemplare_kategorie (exemplareid, kategorieid) VALUES
	(1, 3),
	(1, 5),
	(2, 3),
	(2, 6),
	(3, 4),
	(3, 5),
	(4, 1),
	(4, 7),
	(5, 2),
	(5, 6);
	
INSERT INTO vlastnik (meno) VALUES
	('Moje múzeum'),
	('Historické múzeum');
	
INSERT INTO vlastnik_exemplare (exemplareid, vlastnikid, zaciatok) VALUES
	(1, 1, '2023-01-01'),
	(2, 1, '2024-01-01'),
	(3, 1, '2024-02-01'),
	(4, 1, '2022-08-12'),
	(5, 1, '2024-03-18');
	
INSERT INTO stav (drzitel, zaciatok, stav, status, exemplareid) VALUES
	('Moje múzeum', '2023-01-01', 'sklad', 'prebieha', 1),
	('Moje múzeum', '2024-01-01', 'sklad', 'prebieha', 2),
	('Moje múzeum', '2024-02-01', 'sklad', 'prebieha', 3),
	('Moje múzeum', '2022-08-12', 'sklad', 'prebieha', 4),
	('Moje múzeum', '2024-03-18', 'sklad', 'prebieha', 5);

INSERT INTO expozicie (meno, zaciatok, koniec, status) VALUES
	('Výstava zbraní', '2024-05-1', '2024-08-1', 'planovane');

INSERT INTO zony (meno, rozloha) VALUES
	('A', 150),
	('B', 100),
	('C', 100),
	('D', 80),
	('E', 50);

INSERT INTO expozicie_zony(expozicieid, zonyid) VALUES
	(1, 1),
	(1, 3);