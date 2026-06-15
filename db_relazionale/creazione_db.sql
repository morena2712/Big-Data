-- CREAZIONE TABELLE DATABASE

CREATE DATABASE IF NOT EXISTS db_alberghiero;
USE db_alberghiero;

-- 1. Creazione entità HOTEL
CREATE TABLE Hotel (
    codice      VARCHAR(20) PRIMARY KEY,
    denominazione        VARCHAR(100) NOT NULL,
    indirizzo   VARCHAR(200) NOT NULL,
    citta       VARCHAR(100) NOT NULL,
    stelle      INT NOT NULL CHECK (stelle BETWEEN 1 AND 5)
);

-- 2. Creazione entità TIPOLOGIA
CREATE TABLE Tipologia (
    id_tipologia        VARCHAR(20) PRIMARY KEY,
    categoria                VARCHAR(50) NOT NULL,
    prezzo_per_notte   DECIMAL(10, 2) NOT NULL CHECK (prezzo_per_notte >= 0)
);

-- 3. Creazione entità CAMERA
CREATE TABLE Camera (
    hotel_codice    VARCHAR(20) NOT NULL,
    numero          VARCHAR(10) NOT NULL,
    id_tipologia    VARCHAR(20) NOT NULL,
    stato           VARCHAR(20) DEFAULT 'Libera' 
        CHECK (stato IN ('Libera', 'Occupata', 'In manutenzione')),
    
    PRIMARY KEY (hotel_codice, numero),
    
    FOREIGN KEY (hotel_codice) 
        REFERENCES Hotel(codice)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
        
    FOREIGN KEY (id_tipologia) 
        REFERENCES Tipologia(id_tipologia)
        ON UPDATE CASCADE
        ON DELETE RESTRICT
);

-- 4. Creazione entità CLIENTE
CREATE TABLE Cliente (
    codice_cliente      VARCHAR(20) PRIMARY KEY,
    nome        VARCHAR(50) NOT NULL,
    cognome     VARCHAR(50) NOT NULL,
    telefono    VARCHAR(20),
    email       VARCHAR(100) UNIQUE NOT NULL
);

-- 5. Trigger per calcolare importo totale
DELIMITER $$

CREATE TRIGGER trg_calcola_importo_totale
BEFORE INSERT ON Prenotazione
FOR EACH ROW
BEGIN
    DECLARE numero_notti INT;
    SET numero_notti = DATEDIFF(NEW.data_partenza, NEW.data_arrivo);
    SET NEW.importo_totale = NEW.prezzo_notte_bloccato * numero_notti;
END$$

DELIMITER ;

-- 6. Creazione entità PRENOTAZIONE 
CREATE TABLE Prenotazione (
    id_prenotazione          VARCHAR(20) PRIMARY KEY,
    cliente_codice           VARCHAR(20) NOT NULL,
    hotel_codice             VARCHAR(20) NOT NULL,
    camera_numero            VARCHAR(10) NOT NULL,
    data_arrivo              DATE NOT NULL,
    data_partenza            DATE NOT NULL,
    numero_pax               INT NOT NULL CHECK (numero_pax > 0),
    stato_prenotazione       VARCHAR(20) DEFAULT 'Confermata' 
        CHECK (stato_prenotazione IN (
            'In attesa', 'Confermata', 'In corso', 
            'Completata', 'Cancellata', 'No-Show'
        )),
    importo_totale           DECIMAL(10, 2) NOT NULL CHECK (importo_totale >= 0),
    prezzo_notte_bloccato    DECIMAL(10, 2) NOT NULL CHECK (prezzo_notte_bloccato >= 0),
    
    FOREIGN KEY (cliente_codice) 
        REFERENCES Cliente(codice_cliente)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
        
    FOREIGN KEY (hotel_codice, camera_numero) 
        REFERENCES Camera(hotel_codice, numero)
        ON UPDATE CASCADE
        ON DELETE CASCADE,
    
    CHECK (data_partenza > data_arrivo)
);

-- 7. Trigger per verificare che le prenotazioni delle camere non si sovrappongano
DELIMITER $$

CREATE TRIGGER trg_no_overlapping_reservations
BEFORE INSERT ON Prenotazione
FOR EACH ROW
BEGIN
    IF EXISTS (
        SELECT 1
        FROM Prenotazione p
        WHERE 
            p.hotel_codice = NEW.hotel_codice
            AND p.camera_numero = NEW.camera_numero
            AND p.stato_prenotazione NOT IN ('Cancellata', 'No-Show')
            AND (
                NEW.data_arrivo < p.data_partenza
                AND NEW.data_partenza > p.data_arrivo
            )
    ) THEN
        SIGNAL SQLSTATE '45000' 
		SET MESSAGE_TEXT = 'Errore: La camera selezionata è già occupata in quelle date.';
    END IF;
END$$

DELIMITER ;
