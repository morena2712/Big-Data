# **Database Relazionale (MySQL)**

## **1. Modello Concettuale ed Architetturale**

<img width="3552" height="1908" alt="erdplus (2)" src="https://github.com/user-attachments/assets/adf70b79-d910-4e17-8ada-4fadeee2d35a" />

Il nucleo transazionale del sistema è strutturato su un modello Entità-Relazione (ER) ingegnerizzato tramite ERDPlus. L'architettura si sviluppa attorno a cinque entità principali: Hotel, Camera, Tipologia, Cliente e Prenotazione.

Le relazioni logiche sono state modellate per riflettere i reali vincoli operativi del dominio alberghiero:

* POSSIEDE: Relazione di identificazione forte tra Hotel e Camera. Implementa la dipendenza esistenziale: una camera non può essere censita nel sistema senza un hotel di riferimento.
* CLASSIFICA: Relazione obbligatoria che associa ogni stanza a una categoria tariffaria della tabella Tipologia.
* EFFETTUA: Collega ogni pratica commerciale a un'anagrafica censita nella tabella Cliente.
* ASSOCIA: Vincola in modo univoco ogni record di Prenotazione a una specifica Camera.

### Scelte Progettuali Chiave

* Isolamento delle Tipologie: La separazione delle tariffe base in un'entità dedicata elimina le ridondanze informative e previene anomalie in fase di aggiornamento dei listini.
* Snapshot dei Prezzi: Il campo `prezzo_notte_bloccato` è storicizzato direttamente nella prenotazione al fine di preservare l'integrità dei report finanziari storici a fronte di future variazioni dei prezzi di listino.
* Ridondanza Calcolata (Importo Totale): Il campo `importo_totale` viene memorizzato fisicamente sul disco. Questa denormalizzazione mirata abbatte i costi computazionali delle funzioni di aggregazione (`SUM`, `AVG`) nelle query di Business Intelligence.

## 2. Implementazione SQL e Data Seeding

L'infrastruttura è stata sviluppata in ambiente MySQL 8.0+ utilizzando DBeaver come client di gestione.

* Vedere il file [creazione_db.sql](https://www.google.com/search?q=./db_relazionale/creazione_db.sql)
* Vedere il file [query_popolamento_db.sql](https://www.google.com/search?q=./db_relazionale/query_popolamento_db.sql)

Il popolamento automatizzato sfrutta un generatore sequenziale basato sulla tabella di sistema `information_schema.columns` combinato con funzioni matematiche di MySQL per garantire volumi realistici:

* 125 Camere distribuite equamente (25 stanze per struttura) sui 5 hotel pugliesi.
* 80 Clienti generati combinando liste di nomi e cognomi reali, completi di contatti telefonici e indirizzi e-mail unici verificati.
* 450 Prenotazioni distribuite lungo l'intero anno amministrativo 2026, con lunghezze di soggiorno coerenti e variabili.

### Logiche dei Trigger Aziendali

* Trigger `BEFORE INSERT`: Intercetta la transazione prima della scrittura fisica e calcola l'importo totale moltiplicando i giorni di permanenza reali per la tariffa bloccata per notte.
* Trigger Post-Popolamento (Anti-Overbooking): Configurato e attivato subito dopo il seeding dei dati di test per proteggere il sistema in fase operativa, bloccando a livello transazionale l'inserimento di prenotazioni sovrapposte sulla stessa camera.

## 3. Vincoli e Integrità dei Dati

A protezione della consistenza della base di dati sono stati implementati rigidi vincoli di integrità referenziale e regole di validazione nativa:

* Integrità Temporale: `CHECK (data_partenza > data_arrivo)` impedisce l'inserimento di incongruenze cronologiche nelle prenotazioni.
* Validazione del Business: `CHECK (numero_pax > 0)` assicura che ogni prenotazione registri almeno un occupante pagante.
* Manutenzione del Database: L'opzione `ON DELETE CASCADE` applicata sulla chiave esterna del cliente automatizza la pulizia dello storico e delle prenotazioni collegate in caso di rimozione dell'anagrafica.
* Integrità Referenziale Composta: La relazione di allocazione sfrutta una chiave esterna composta `(hotel_codice, camera_numero)` collegata alla chiave primaria di Camera, garantendo che il sistema assegni stanze realmente esistenti all'interno della specifica struttura selezionata.

## 4. Query di Analisi e Business Intelligence

Le interrogazioni sviluppate rispondono alle metriche prestazionali richieste dal controllo di gestione, ripartite in quattro macro-aree:

### Capacità e Disponibilità

* Conteggio e saturazione delle camere per singolo hotel e per tipologia commerciale.
* Verifica in tempo reale delle camere disponibili all'interno di un intervallo di date personalizzato tramite parametri.
* Classifica delle sistemazioni più richieste e identificazione delle anomalie di occupazione.

### Domanda e Comportamento dei Clienti

* Identificazione dei clienti più attivi per volume di prenotazioni effettuate.
* Analisi dei profili più redditizi per l'azienda.
* Calcolo della durata media dei soggiorni per ottimizzare le strategie di marketing e di housekeeping.

### Performance Economica

* Calcolo del fatturato lordo totale generato dall'intero network alberghiero.
* Scomposizione dei ricavi ed estrazione dei flussi di cassa aggregati per hotel e su base mensile.
* Analisi dell'andamento storico delle tariffe tramite il prezzo medio per notte bloccato.

### Cancellazioni e Risk Management

* Calcolo del tasso di cancellazione globale (rapporto tra pratiche andate a buon fine e flussi di Cancellata / No-Show).
* Reportistica delle cancellazioni per verificare l'affidabilità delle prenotazioni per hotel e per singolo cliente.
* Analisi dell'impatto economico teorico e delle perdite finanziarie stimate causate dalle disdette.

## 5. Obiettivo del Sistema

Il modulo relazionale risponde perfettamente ai requisiti della traccia fornendo:

1. Una struttura dati normalizzata che azzera la ridondanza e le anomalie tipiche dei file di testo piatti.
2. Un ambiente transazionale sicuro basato sulle proprietà ACID per la gestione economica della reception.
3. Un set completo di strumenti di analisi in grado di monitorare la redditività delle strutture, guidando le decisioni strategiche del management alberghiero.

## 6. Conclusione

Questo modulo rappresenta le fondamenta operative dell'intero progetto. L'integrazione di vincoli referenziali composti, trigger di calcolo e query di Business Intelligence dimostra come il modello relazionale sia la scelta ideale per governare i flussi strutturati e transazionali, garantendo la sicurezza e la stabilità dei dati di business.
