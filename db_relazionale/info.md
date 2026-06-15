# **Database Relazionale (Sintesi Tecnica)**

## **1. Modello Concettuale**

<img width="3552" height="1908" alt="erdplus (2)" src="https://github.com/user-attachments/assets/adf70b79-d910-4e17-8ada-4fadeee2d35a" />

Il modello ER è stato progettato con ERDPlus e si basa su cinque entità principali: **Hotel**, **Camera**, **Tipologia**, **Cliente**, **Prenotazione**.  
Le relazioni implementano i vincoli del dominio:

- **POSSIEDE** — relazione identificante tra Hotel e Camera: una camera non può esistere senza hotel.  
- **CLASSIFICA** — ogni camera appartiene obbligatoriamente a una tipologia.  
- **EFFETTUA** — ogni prenotazione deve essere associata a un cliente.  
- **ASSOCIA** — ogni prenotazione blocca esattamente una camera.

Scelte progettuali fondamentali:

- **Tipologia come entità separata** per eliminare ridondanza e anomalie di aggiornamento.  
- **prezzo_notte_bloccato nella relazione ASSOCIA** utile come snapshot del prezzo al momento della prenotazione.  
- **importo_totale salvato fisicamente** per migliorare la performance nelle analisi economiche.

## **2. Implementazione SQL**
L’implementazione è stata realizzata in MySQL tramite DBeaver.

### **Creazione del database**

Vedere [creazione_db.sql](./db_relazionale/creazione_db.sql)

### **Popolamento**

Vedere [query_popolamento_db.sql](./db_relazionale/query_popolamento_db.sql)

- Generazione automatica di **100 camere** tramite una sequenza costruita interrogando `information_schema.columns`. 
- Creazione di **60 clienti** con email generate dinamicamente e garantite uniche.  
- Inserimento di **250 prenotazioni** con date casuali ma coerenti.

#### **Trigger**
- **Trigger calcolo importo_totale**, attivo prima dell’inserimento delle prenotazioni.  
- **Trigger anti-overbooking**, attivato *dopo* il popolamento per evitare blocchi durante la generazione dei dati.


## **3. Vincoli e Integrità**
- `CHECK (data_partenza > data_arrivo)` per impedire errori temporali.  
- `CHECK (numero_pax > 0)` per garantire prenotazioni valide.  
- `ON DELETE CASCADE` su cliente, in modo da eliminare automaticamente lo storico associato.  
- Chiave esterna composta `(hotel_codice, camera_numero)` per implementare correttamente la relazione ASSOCIA.


## **4. Query di Analisi**
Le interrogazioni sviluppate coprono tutte le esigenze gestionali:

### **Capacità e disponibilità**
- Numero camere per hotel  
- Numero camere per tipologia  
- Camere disponibili in un intervallo di date  
- Camere più richieste  
- Overbooking e sovrapposizioni

### **Domanda e comportamento dei clienti**
- Clienti con più prenotazioni  
- Clienti più redditizi  
- Durata media dei soggiorni  
- Clienti con prenotazioni attive

### **Performance economica**
- Fatturato totale  
- Fatturato per hotel  
- Fatturato mensile  
- Prezzo medio per notte  
- Impatto economico delle cancellazioni

### **Cancellazioni**
- Tasso di cancellazione  
- Cancellazioni per hotel  
- Cancellazioni per cliente  

Ogni query è progettata per rispondere a una domanda gestionale reale e per validare la correttezza del modello.


## **5. Obiettivo del Sistema**
Il database relazionale fornisce:

- una struttura coerente e normalizzata,  
- un dataset realistico e completo,  
- strumenti analitici per valutare domanda, offerta, performance economica e comportamento dei clienti,  
- un ambiente affidabile per simulare scenari gestionali reali.


## **6. Conclusione**
Il sistema integra progettazione concettuale, schema logico, vincoli, trigger, popolamento e interrogazioni avanzate.  
L’insieme dimostra la capacità del modello di supportare analisi operative e strategiche, garantendo integrità dei dati, performance e coerenza con le esigenze del dominio alberghiero.
