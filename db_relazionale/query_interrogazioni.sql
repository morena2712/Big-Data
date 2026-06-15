-- Elenco hotel con numero totale di camere
SELECT 
    h.codice AS hotel_codice,
    h.denominazione   AS hotel_nome,
    COUNT(c.numero) AS totale_camere
FROM Hotel h
LEFT JOIN Camera c
    ON c.hotel_codice = h.codice
GROUP BY h.codice, h.denominazione
ORDER BY totale_camere DESC;

-- Numero camere per tipologia
SELECT 
    t.id_tipologia,
    t.categoria,
    COUNT(*) AS numero_camere
FROM Camera c
JOIN Tipologia t
    ON t.id_tipologia = c.id_tipologia
GROUP BY t.id_tipologia, t.categoria
ORDER BY numero_camere DESC;

-- Hotel con più prenotazioni
SELECT 
    h.codice AS hotel_codice,
    h.denominazione   AS hotel_nome,
    COUNT(p.id_prenotazione) AS numero_prenotazioni
FROM Prenotazione p
JOIN Hotel h
    ON h.codice = p.hotel_codice
GROUP BY h.codice, h.denominazione
ORDER BY numero_prenotazioni DESC;

-- Occupazione media per hotel
SELECT
    h.codice AS hotel_codice,
    h.denominazione   AS hotel_nome,
    SUM(DATEDIFF(p.data_partenza, p.data_arrivo)) AS notti_prenotate,
    COUNT(DISTINCT c.hotel_codice, c.numero)      AS numero_camere,
    SUM(DATEDIFF(p.data_partenza, p.data_arrivo)) 
        / NULLIF(COUNT(DISTINCT c.hotel_codice, c.numero), 0) AS notti_medie_per_camera
FROM Prenotazione p
JOIN Hotel h
    ON h.codice = p.hotel_codice
JOIN Camera c
    ON c.hotel_codice = p.hotel_codice AND c.numero = p.camera_numero
GROUP BY h.codice, h.denominazione;

-- Camere disponibili in un intervallo di date
SELECT 
    c.hotel_codice,
    c.numero AS camera_numero
FROM Camera c
WHERE NOT EXISTS (
    SELECT 1
    FROM Prenotazione p
    WHERE p.hotel_codice = c.hotel_codice
      AND p.camera_numero = c.numero
      AND p.stato_prenotazione NOT IN ('Cancellata', 'No-Show')
      AND (
            :data_inizio < p.data_partenza
        AND :data_fine   > p.data_arrivo
      )
);

-- Camere più richieste
SELECT 
    p.hotel_codice,
    p.camera_numero,
    COUNT(*) AS numero_prenotazioni
FROM Prenotazione p
GROUP BY p.hotel_codice, p.camera_numero
ORDER BY numero_prenotazioni DESC;

-- Camere con overbooking e giorni a rischio
SELECT 
    p1.hotel_codice,
    p1.camera_numero,
    p1.id_prenotazione AS pren1,
    p2.id_prenotazione AS pren2,
    p1.data_arrivo,
    p1.data_partenza,
    p2.data_arrivo,
    p2.data_partenza
FROM Prenotazione p1
JOIN Prenotazione p2
    ON p1.hotel_codice = p2.hotel_codice
   AND p1.camera_numero = p2.camera_numero
   AND p1.id_prenotazione < p2.id_prenotazione
   AND p1.stato_prenotazione NOT IN ('Cancellata', 'No-Show')
   AND p2.stato_prenotazione NOT IN ('Cancellata', 'No-Show')
   AND (
        p1.data_arrivo < p2.data_partenza
    AND p1.data_partenza > p2.data_arrivo
   );

-- Clienti che hanno effettuato più prenotazioni
SELECT 
    c.codice_cliente,
    c.nome,
    c.cognome,
    COUNT(p.id_prenotazione) AS numero_prenotazioni
FROM Prenotazione p
JOIN Cliente c
    ON c.codice_cliente = p.cliente_codice
GROUP BY c.codice_cliente, c.nome, c.cognome
ORDER BY numero_prenotazioni DESC;

-- Clienti che hanno speso di più
SELECT 
    c.codice_cliente,
    c.nome,
    c.cognome,
    SUM(p.importo_totale) AS totale_speso
FROM Prenotazione p
JOIN Cliente c
    ON c.codice_cliente = p.cliente_codice
WHERE p.stato_prenotazione IN ('Completata', 'In corso')
GROUP BY c.codice_cliente, c.nome, c.cognome
ORDER BY totale_speso DESC;

-- Durata media delle prenotazioni
SELECT 
    AVG(DATEDIFF(p.data_partenza, p.data_arrivo)) AS durata_media_notti
FROM Prenotazione p
WHERE p.stato_prenotazione IN ('Completata', 'In corso', 'Confermata');

-- Clienti con prenotazioni attive
SELECT DISTINCT
    c.codice_cliente,
    c.nome,
    c.cognome
FROM Prenotazione p
JOIN Cliente c
    ON c.codice_cliente = p.cliente_codice
WHERE p.stato_prenotazione IN ('In attesa', 'Confermata', 'In corso');

-- Prenotazioni di un hotel in un intervallo di date
SELECT 
    p.*
FROM Prenotazione p
WHERE p.hotel_codice = :hotel_codice
  AND (
        :data_inizio < p.data_partenza
    AND :data_fine   > p.data_arrivo
  )
ORDER BY p.data_arrivo;

-- Fatturato totale del sistema
SELECT 
    SUM(p.importo_totale) AS fatturato_totale
FROM Prenotazione p
WHERE p.stato_prenotazione IN ('Completata', 'In corso');

-- Fatturato per hotel
SELECT 
    h.codice AS hotel_codice,
    h.denominazione   AS hotel_nome,
    SUM(p.importo_totale) AS fatturato
FROM Prenotazione p
JOIN Hotel h
    ON h.codice = p.hotel_codice
WHERE p.stato_prenotazione IN ('Completata', 'In corso')
GROUP BY h.codice, h.denominazione
ORDER BY fatturato DESC;

-- Fatturato mensile
SELECT 
    YEAR(p.data_arrivo)  AS anno,
    MONTH(p.data_arrivo) AS mese,
    SUM(p.importo_totale) AS fatturato
FROM Prenotazione p
WHERE p.stato_prenotazione IN ('Completata', 'In corso')
GROUP BY YEAR(p.data_arrivo), MONTH(p.data_arrivo)
ORDER BY anno, mese;

-- Andamento storico dei prezzi (prezzo media per notte per mese)
SELECT 
    YEAR(p.data_arrivo)  AS anno,
    MONTH(p.data_arrivo) AS mese,
    AVG(p.prezzo_notte_bloccato) AS prezzo_medio_notte
FROM Prenotazione p
GROUP BY YEAR(p.data_arrivo), MONTH(p.data_arrivo)
ORDER BY anno, mese;

-- Tasso di cancellazione
SELECT 
    COUNT(*) AS totale_prenotazioni,
    SUM(stato_prenotazione IN ('Cancellata', 'No-Show')) AS totale_cancellate,
    AVG(stato_prenotazione IN ('Cancellata', 'No-Show')) AS tasso_cancellazione
FROM Prenotazione;

-- Cancellazioni per hotel
SELECT 
    h.codice AS hotel_codice,
    h.denominazione   AS hotel_nome,
    COUNT(*) AS numero_cancellazioni
FROM Prenotazione p
JOIN Hotel h
    ON h.codice = p.hotel_codice
WHERE p.stato_prenotazione IN ('Cancellata', 'No-Show')
GROUP BY h.codice, h.denominazione
ORDER BY numero_cancellazioni DESC;

-- Cancellazioni per cliente
SELECT 
    c.codice_cliente,
    c.nome,
    c.cognome,
    COUNT(*) AS numero_cancellazioni
FROM Prenotazione p
JOIN Cliente c
    ON c.codice_cliente = p.cliente_codice
WHERE p.stato_prenotazione IN ('Cancellata', 'No-Show')
GROUP BY c.codice_cliente, c.nome, c.cognome
ORDER BY numero_cancellazioni DESC;

-- Impatto economico delle cancellazioni
SELECT 
    SUM(p.importo_totale) AS importo_teorico_cancellato
FROM Prenotazione p
WHERE p.stato_prenotazione IN ('Cancellata', 'No-Show');