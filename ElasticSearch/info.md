# Modulo Elasticsearch: Analisi della Customer Satisfaction

Questo modulo si occupa della gestione, dell'indicizzazione e dell'analisi semantica delle recensioni testuali (dati non strutturati) rilasciate dai clienti al termine del loro soggiorno presso le strutture del gruppo alberghiero.

Mentre il database relazionale (MySQL) governa le transazioni rigide e la consistenza delle prenotazioni, Elasticsearch interviene come motore di recupero di informazioni per estrarre insight aziendali e monitorare il sentiment dei clienti in tempo reale.

## 1. Traccia e Requisiti di Business

Il management alberghiero richiede un sistema centralizzato capace di raccogliere le recenzioni lasciatie dagli ospiti per le rispettive prenotazioni. L'esigenza critica è l'immediatezza della ricerca: gli albergatori e i direttori di reparto devono poter scovare istantaneamente specifiche tematiche all'interno di migliaia di commenti.

### Casi d'uso aziendali richiesti:

1. Valutazione delle strutture: calcolare il rating medio di gradimento per ogni singolo hotel per identificare i trend positivi o negativi;
2. Customer Care): intercettare immediatamente le recensioni gravemente insufficienti che menzionano problemi con lo staff o con i servizi erogati;
3. Controllo Ambientale: monitorare le lamentele legate ai disturbi acustici e al rumore durante il picco della stagione estiva;
4. Ispezione della pulizia: ispezionare l'intero storico annuale alla ricerca di qualsiasi menzione (elogio o critica) riguardante i livelli di igiene e pulizia delle stanze.

## 2. Scelte di Configurazione

I database tradizionali (SQL) o a grafo (Neo4j) non sono strutturati per l'analisi del testo libero. L'uso di operatori come `LIKE '%pulizia%'` in SQL costringe il sistema a una scansione sequenziale dell'intera tabella, portando al collasso delle prestazioni su volumi massivi e fallendo in presenza di errori di battitura o varianti linguistiche.

Per questo modulo, l'indice `recensioni_hotel` è stato configurato sfruttando due funzionalità chiave di Elasticsearch:

* Indice Invertito: trasforma il testo libero in una mappa in cui a ogni parola chiave corrisponde l'elenco immediato dei documenti che la contengono, azzerando i tempi di ricerca;
* Analyzer Italiano (`it_analyzer`): applica lo stemming nativo per la lingua italiana. Il motore riduce ogni parola alla sua radice linguistica. Di conseguenza, cercando "pulizia", il sistema intercetta anche "pulito", "pulite" o "pulitissimo"; cercando "rumore", il sistema intercetta anche "rumorosa".

## 3. Struttura dell'Indice

I documenti JSON all'interno dell'indice sono denormalizzati e contengono i riferimenti numerici (`hotel_codice`, `id_prenotazione`) per garantire un ponte logico diretto con le tabelle transazionali di MySQL:

```json
{
  "mappings": {
    "properties": {
      "id_recensione":    { "type": "keyword" },
      "id_prenotazione":  { "type": "keyword" },
      "hotel_codice":     { "type": "keyword" },
      "cliente_codice":   { "type": "keyword" },
      "punteggio":        { "type": "integer" },
      "testo_recensione": { "type": "text", "analyzer": "it_analyzer" },
      "data_recensione":  { "type": "date" }
    }
  }
}

```

## 4. Logica delle Query Analitiche e Applicative

All'interno del file di esecuzione [usage.py](https://github.com/utente/Big-Data/tree/main/ElasticSearch/usage.py) è stato implementato un insieme di test basato su un dataset iniziale di 26 recensioni realistiche relative all'anno 2026.

### Query 1: Business Intelligence - Rating Medio per Hotel

Esegue un'aggregazione di tipo `terms` su `hotel_codice` e calcola una sotto-aggregazione di tipo `avg` sul campo `punteggio`. Genera una classifica in tempo reale delle strutture basata sulla soddisfazione del cliente, escludendo i dettagli dei singoli testi per massimizzare la velocità.

### Query 2: Customer Care - Segnalazioni Critiche sullo Staff

Sfrutta un costrutto `bool` combinando un `filter` numerico (punteggio inferiore a 2) e una ricerca `multi_match` sulle parole "personale" o "servizio". Permette di isolare istantaneamente i focolai di insoddisfazione legati al comportamento del personale.

### Query 3: Monitoraggio Ambientale - Inquinamento Acustico Estivo

Isola un filtro temporale (`range`) mirato sul periodo della movida estiva (dal 1° Giugno al 15 Settembre 2026) ed esegue una ricerca `match` espansa su un intero dizionario di sinonimi acustici (rumore, rumorosa, caos, caotica, schiamazzi, disturbo, baccano). Grazie all'algoritmo di rilevanza e alla proprietà di `fuzziness`, la query tollera gli errori di battitura degli utenti e ordina i risultati partendo dai disagi più gravi.

### Query 4: Ispezione Sanitaria - Focus Pulizia Globale

Rappresenta una ricerca Full-Text destagionalizzata sull'intero storico aziendale. Scandaglia i testi utilizzando parole chiave sia positive che negative (pulizia, igiene, sporco, pulito, splendente, polvere). Questo consente al team di Housekeeping di avere un report completo sul livello di igiene percepito dagli ospiti nei dodici mesi di attività.
