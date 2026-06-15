# Big-Data

Questa repositary presenta la progettazione e l’analisi di due distinti domini applicativi attraverso l’uso di basi di dati relazionali e a grafo. La prima parte riguarda la gestione informatizzata di un gruppo alberghiero: vengono modellati hotel, camere, clienti e prenotazioni, con l’obiettivo di supportare il controllo della disponibilità, la prevenzione delle sovrapposizioni e la consultazione dello storico. Su questo modello vengono eseguite diverse query, tra cui l’analisi delle prenotazioni per intervallo temporale e l’identificazione dei clienti più attivi.

La seconda parte affronta la costruzione di un knowledge graph dedicato alle pubblicazioni scientifiche di un dipartimento di ricerca. Il modello include autori, articoli, citazioni e temi di ricerca, consentendo l’esplorazione delle reti di collaborazione e delle relazioni tematiche. Anche in questo caso vengono formulate query significative, come l’individuazione degli articoli che citano un determinato lavoro e degli autori che condividono un tema senza aver collaborato.

## 1. Sistema per Gruppo Alberghiero
Traccia: Un piccolo gruppo alberghiero vuole informatizzare la gestione delle proprie strutture. Ogni hotel è identificato da un codice, ha un nome, un indirizzo, una città e una categoria espressa in stelle. Ogni hotel dispone di diverse camere, contraddistinte da numero, tipologia, prezzo per notte e stato attuale, ad esempio libera, occupata o in manutenzione. Di ogni cliente si vogliono registrare codice, nome, cognome, telefono ed email. I clienti possono effettuare prenotazioni per una o più notti, indicando data di arrivo, data di partenza e numero di persone. Per ciascuna prenotazione il sistema deve associare una specifica camera e memorizzare anche l’importo totale previsto. La base di dati deve permettere di controllare la disponibilità delle camere e lo storico delle prenotazioni effettuate dai clienti.

## 2. Rete di pubblicazioni scientifiche.
Traccia: Un dipartimento di ricerca vuole costruire un knowledge graph delle proprie pubblicazioni. Ogni autore ha nome, cognome, affiliazione, email e area di ricerca. Ogni articolo scientifico è descritto da titolo, anno, DOI e venue di pubblicazione. Gli articoli possono citare altri articoli, essere scritti da più autori e trattare uno o più temi scientifici. I temi sono concetti come machine learning, bioinformatica, database o computer vision. Il grafo deve consentire di analizzare collaborazioni scientifiche, reti di citazione e collegamenti tra temi di ricerca. Gli studenti devono modellare il dominio in modo da poter rispondere sia a domande strutturali sia a domande di esplorazione.

## 3. ElasticSearch
Dopo aver modellato il dominio gestionale degli hotel in ambiente SQL, sfruttando la struttura relazionale per garantire integrità, vincoli e coerenza transazionale, e dopo aver rappresentato la rete delle pubblicazioni scientifiche in Neo4j, valorizzando la natura fortemente connessa dei dati tramite un grafo orientato alle relazioni, il passo successivo consiste nell’esplorare come gli stessi domini possano essere analizzati attraverso Elasticsearch.

In questo contesto, Elasticsearch non sostituisce i modelli precedenti, ma li completa:

* rispetto a SQL, offre capacità di ricerca testuale, aggregazioni analitiche e interrogazioni temporali ad alte prestazioni;
* rispetto a Neo4j, consente esplorazioni rapide basate su co‑occorrenze, filtri e correlazioni, pur senza la profondità semantica di un grafo nativo.
  
L’obiettivo è quindi mostrare come gli stessi dataset — prenotazioni alberghiere e pubblicazioni scientifiche — possano essere indicizzati e interrogati in Elasticsearch per ottenere risposte immediate a domande operative e analitiche, integrando così i punti di forza dei tre paradigmi: relazionale, grafico e documentale.
