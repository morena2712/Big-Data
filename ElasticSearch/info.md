# Modello NoSQL – Elasticsearch

Questo modulo contiene l’implementazione del modello NoSQL basato su Elasticsearch per i due domini del progetto:

1. Gestione hotel e prenotazioni
2. Rete di pubblicazioni scientifiche

## Struttura dei dati

### Prenotazioni (Hotel)
I documenti sono denormalizzati e includono:
- dati dell’hotel
- dati del cliente
- dati della camera
- intervallo temporale
- importo totale

Questa scelta ottimizza le query di ricerca e filtraggio.

### Articoli scientifici
Ogni documento rappresenta un articolo e contiene:
- DOI, titolo, anno
- lista di autori (nested)
- lista di temi
- lista di DOI citati

Il modello supporta analisi di citazioni e co-occorrenze.

## Query implementate

### Hotel
- prenotazioni di un hotel in un intervallo di date
- clienti con il maggior numero di prenotazioni

### Pubblicazioni scientifiche
- articoli che citano un determinato DOI
- autori che pubblicano sullo stesso tema
- coppie di autori che hanno collaborato

## Considerazioni

Elasticsearch è ideale per:
- ricerche testuali
- filtri temporali
- aggregazioni analitiche
- analisi esplorative

Non sostituisce SQL (integrità relazionale) né Neo4j (analisi di grafo), ma li completa offrendo un modello documentale ad alte prestazioni.
