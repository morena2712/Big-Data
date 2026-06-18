# Big Data: Architettura Dati Multi-Paradigma (MySQL, Neo4j, Elasticsearch)

Questo progetto mostra come gestire e analizzare i dati usando tre tipi di database diversi (relazionale, a grafo e documentale). Invece di usare un solo database per fare tutto, si è scelto il motore giusto per ogni specifico problema aziendale, ottenendo il massimo delle prestazioni.

## 1. Gestione Hotel: Database Relazionale (MySQL)
### Il problema
Un gruppo alberghiero con strutture dislocate in Puglia necessita di un'infrastruttura centralizzata per gestire l'operatività quotidiana: anagrafiche clienti, disponibilità delle camere in tempo reale, fatturazione e, come vincolo critico, l'assoluta eliminazione dei rischi di overbooking.

### Scelte architetturali
Il sistema modella 5 hotel, 125 camere (25 stanze per struttura ripartite su tipologie Singola, Doppia e Suite), 80 clienti e uno storico controllato di 450 prenotazioni per l'anno 2026.

Le tariffe standard risiedono nell'entità `Tipologia`. Al momento della prenotazione, il valore viene congelato nel campo `prezzo_notte_bloccato` di `Prenotazione`, rendendo lo storico finanziario immune da future modifiche dei listini aziendali.

#### Logiche di Automazione (Trigger)
`BEFORE INSERT` calcola automaticamente l'`importo_totale` moltiplicando i giorni del soggiorno per la tariffa bloccata per notte. Il trigger anti-overbooking blocca sul nascere qualsiasi inserimento o modifica di prenotazioni le cui date si sovrappongano a una stanza già occupata.

### Query di Controllo Operativo
* Inventario della capacità e saturazione camere per struttura e tipologia.
* Classificazione analitica dei clienti fidelizzati e dei principali top spender.
* Business Intelligence economica: fatturato lordo totale, ricavi aggregati su base mensile e fluttuazione storica del prezzo medio per notte.
* Monitoraggio del tasso di cancellazione e calcolo dell'impatto economico teorico dei flussi contrassegnati come Cancellata o No-Show.

## 2. Rete di Pubblicazioni: Database a Grafo (Neo4j)
### Il problema
Un dipartimento universitario richiede uno strumento per mappare e navigare la propria produzione scientifica. L'esigenza non si concentra su dati isolati, ma sull'esplorazione profonda e topologica delle connessioni, per far emergere le dinamiche di collaborazione e l'impatto accademico dei paper.

### Perché usare un database a grafo
Nelle tabelle tradizionali (SQL), per trovare catene di collegamenti servirebbero operazioni di incrocio molto pesanti che rallentano il sistema. Con Neo4j, i dati sono collegati direttamente tra loro tramite frecce (relazioni).

* I Nodi: Autore, Articolo, Tema di ricerca, Venue.

* I Collegamenti: Un autore ha scritto un articolo; un articolo cita un altro articolo; un articolo tratta un tema; un articolo è stato pubblicato in una venue.

### Cosa analizzano le query (Cypher)
* Analisi Strutturale: rilevamento dei nodi centrali della rete (ricercatori più prolifici e articoli con il più alto tasso di citazione).
* Catene di Collaborazione: analisi delle reti di co-autoria e tracciamento dei percorsi di citazione diretti e indiretti.
* Algoritmi Predittivi (Opportunità): identificazione di coppie di autori che pubblicano sulle stesse aree tematiche ma che non hanno mai collaborato a una pubblicazione comune, suggerendo nuove sinergie strategiche per il dipartimento.

## 3. Customer Satisfaction: Analisi dei Feedback (Elasticsearch)
### Il problema
Il management alberghiero vuole monitorare la qualità dei servizi analizzando le recensioni testuali (dati non strutturati) lasciate dagli ospiti. L'esigenza critica è l'indicizzazione e la ricerca Full-Text immediata: l'albergatore deve poter individuare istantaneamente, ad esempio, tutti i commenti che parlano di "pulizia" o di "rumore" all'interno di migliaia di testi liberi.

### Scelte Tecniche e Configurazione dell'Indice
I database normali fanno fatica a cercare parole dentro testi lunghi e liberi. Elasticsearch è un motore di ricerca fatto apposta per questo.
Le recensioni JSON sono inserite nell'indice recensioni_hotel e mantengono riferimenti speculari (hotel_codice, id_prenotazione) con il database MySQL.

* Indice Invertito ed Elisione Linguistica: L'indice adotta l'analyzer nativo italian. Il motore applica lo stemming (riduzione alla radice semantica del lemma). Di conseguenza, una ricerca sulla parola chiave "pulizia" intercetta automaticamente espressioni naturali come "pulito", "pulite" o "pulitissimo".

### Query analitiche (usage.py)
Lo script Python gestisce 26 recensioni realistiche (anno 2026) ed esegue quattro query avanzate tramite Elasticsearch DSL:
* Aggregazione per struttura (terms) e sotto-aggregazione metrica (avg) sul campo punteggio: calcola il rating medio storico di ciascun hotel per tracciare i trend di gradimento del brand.
* Customer Care: calcola un costrutto booleano che isola i voti insufficienti (inferiori a 2) ed esegue un match testuale sulle parole chiave "personale" o "servizio", notificando real-time i disservizi dello staff.
* Focus Rumore Estivo: crea un filtro range temporale mirato sul periodo della movida estiva (1° Giugno – 15 Settembre 2026) associato a un match esteso su sinonimi acustici (rumore, rumorosa, caos, caotica, schiamazzi, disturbo, baccano). Ottimizzato con parametri di fuzziness per tollerare refusi di battitura degli utenti.
* Focus Pulizia Globale: interrogazione full-text destagionalizzata ed estesa a tutto lo storico annuale. Mappa a 360 gradi l'igiene percepita scansionando i termini sia positivi che negativi (pulizia, igiene, sporco, pulito, splendente, polvere).

## Conclusione
Questo ecosistema dimostra i vantaggi della Polyglot Persistence: la robustezza transazionale di MySQL protegge i dati finanziari e previene gli errori operativi; la flessibilità di Neo4j sblocca la conoscenza nascosta nelle reti complesse; la velocità di Elasticsearch trasforma i testi liberi in metriche di controllo immediate. L'integrazione di questi tre paradigmi offre un'infrastruttura scalabile, resiliente e perfettamente allineata alle necessità strategiche di un'organizzazione moderna.
