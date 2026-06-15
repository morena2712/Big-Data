-- 1. Inserimento dati in HOTEL

INSERT INTO Hotel VALUES
('H001','Hotel Sole','Via Roma 10','Ostuni',4),
('H002','Mare Blu Resort','Lungomare 25','Brindisi',5),
('H003','Collina Verde','Via dei Pini 8','Cisternino',3),
('H004','Trulli Paradise','Contrada Monte 12','Alberobello',4),
('H005','Porto Sereno','Via del Porto 3','Monopoli',4);

-- 2. Inserimento dati in TIPOLOGIA

INSERT INTO Tipologia VALUES
('T1','Singola',55),
('T2','Doppia',85),
('T3','Suite',150);

-- 3. Inserimento dati in CAMERA

INSERT INTO Camera (hotel_codice, numero, id_tipologia, stato)
SELECT
    CASE
        WHEN n <= 25 THEN 'H001'
        WHEN n <= 50 THEN 'H002'
        WHEN n <= 75 THEN 'H003'
        WHEN n <= 100 THEN 'H004'
        ELSE 'H005'
    END AS hotel_codice,
    LPAD((n-1)%20+1, 3, '0') AS numero,
    ELT(FLOOR(1 + RAND()*3), 'T1','T2','T3') AS id_tipologia,
    ELT(FLOOR(1 + RAND()*3), 'Libera','Occupata','In manutenzione') AS stato
FROM (
    SELECT @row := @row + 1 AS n
    FROM information_schema.columns, (SELECT @row := 0) r
    LIMIT 125
) AS seq;

-- 4. Inserimento dati in CLIENTE

SET @nomi = 'Marco,Giulia,Luca,Sara,Francesco,Chiara,Alessandro,Martina,Giorgio,Elena';
SET @cognomi = 'Rossi,Bianchi,Verdi,Ferrari,Esposito,Romano,Gallo,Costa,Fontana,Greco';

INSERT INTO Cliente (codice_cliente, nome, cognome, telefono, email)
SELECT
    CONCAT('C', LPAD(n,3,'0')),
    ELT(FLOOR(1 + RAND()*10), 'Marco','Giulia','Luca','Sara','Francesco','Chiara','Alessandro','Martina','Giorgio','Elena'),
    ELT(FLOOR(1 + RAND()*10), 'Rossi','Bianchi','Verdi','Ferrari','Esposito','Romano','Gallo','Costa','Fontana','Greco'),
    CONCAT('3', LPAD(FLOOR(RAND()*999999999), 9, '0')),
    CONCAT(
        LOWER(ELT(FLOOR(1 + RAND()*10), 'marco','giulia','luca','sara','francesco','chiara','alessandro','martina','giorgio','elena')),
        '.',
        LOWER(ELT(FLOOR(1 + RAND()*10), 'rossi','bianchi','verdi','ferrari','esposito','romano','gallo','costa','fontana','greco')),
        n,
        '@example.com'
    )
FROM (
    SELECT @i := @i + 1 AS n
    FROM information_schema.columns, (SELECT @i := 0) r
    LIMIT 80
) AS seq;

-- 5. Inserimento dati in PRENOTAZIONE

INSERT INTO Prenotazione (
    id_prenotazione, cliente_codice, hotel_codice, camera_numero,
    data_arrivo, data_partenza, numero_pax,
    stato_prenotazione, importo_totale, prezzo_notte_bloccato
)
SELECT
    CONCAT('P', SUBSTRING(UUID(), 1, 8)) AS id_prenotazione,
    CONCAT('C', LPAD(FLOOR(1 + RAND()*60),3,'0')) AS cliente_codice,
    c.hotel_codice,
    c.numero AS camera_numero,
    DATE_ADD('2026-01-01', INTERVAL @arr := FLOOR(RAND()*300) DAY) AS data_arrivo,
    DATE_ADD('2026-01-01', INTERVAL @arr + FLOOR(1 + RAND()*7) DAY) AS data_partenza,
    FLOOR(1 + RAND()*3) AS numero_pax,
    ELT(FLOOR(1 + RAND()*6),
        'In attesa','Confermata','In corso','Completata','Cancellata','No-Show'
    ) AS stato_prenotazione,
    0 AS importo_totale,
    CASE c.id_tipologia
        WHEN 'T1' THEN 55
        WHEN 'T2' THEN 85
        ELSE 150
    END AS prezzo_notte_bloccato
FROM (
    SELECT @p := @p + 1 AS n
    FROM information_schema.columns, (SELECT @p := 0) r
    LIMIT 320
) AS seq
JOIN (
    SELECT hotel_codice, numero, id_tipologia
    FROM Camera
    ORDER BY RAND()
) AS c
ON 1=1;
