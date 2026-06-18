# Modulo Grafo: Knowledge Graph della Produzione Scientifica (Neo4j)

## 1. Obiettivo del Modello

Il database basato su grafi è strutturato come un **Knowledge Graph** per mappare e analizzare l'intera produzione scientifica del dipartimento di ricerca. La scelta di questo paradigma supera i limiti strutturali dei database relazionali quando si tratta di navigare connessioni complesse e nidificate (come le catene di citazioni o i flussi di collaborazione).

La progettazione punta a ottenere un ecosistema informativo che sia:

* Privo di ridondanze, duplicati o anomalie di aggiornamento.
* Semanticamente ricco: ogni collegamento esprime una precisa relazione di business ed è dotato di proprietà specifiche.
   Ottimizzato sia per interrogazioni operative rapide sia per algoritmi complessi di Graph Data Science (GDS).

## 2. Schema Concettuale (Nodi e Relazioni)

L'architettura del grafo si articola su cinque macro-categorie di nodi, interconnesse da relazioni orientate e tipizzate.

### I Nodi del Sistema

* Article: Titolo, DOI, Anno, Abstract, Numero di citazioni;
* Author: Nome, Cognome, Email, Area di ricerca principale, H-Index;
* Topic: Nome dell'area tematica, Descrizione concettuale;
* Venue: Nome, Tipologia (Conference / Journal), Impact Factor;
* Affiliation: Nome dell'istituzione/università di appartenenza

### Le Relazioni e le Proprietà di Collegamento

* `(:Author)-[:AUTHORED_BY]->(:Article)` : Associa gli autori alle rispettive pubblicazioni.
* `(:Author)-[:AFFILIATED_WITH]->(:Affiliation)` : Traccia l'appartenenza accademica dei ricercatori.
* `(:Article)-[:PUBLISHED_IN]->(:Venue)` : Identifica la sede editoriale del paper.
* `(:Article)-[:COVERS]->(:Topic)` : Connette l'articolo ai temi trattati. Include la proprietà `relevance` per pesare l'importanza del tema nel testo.
* `(:Article)-[:CITES]->(:Article)` : Mappa la rete delle citazioni. Include la proprietà `context` per comprendere il ruolo della citazione (es. methodology, foundation, related work).
* `(:Author)-[:CO_AUTHORED]->(:Author)` : Relazione derivata che unisce i ricercatori che hanno collaborato a un progetto comune.


## 3. Interpretazione del Grafo e Topologia

<img width="1600" height="1600" alt="Code_Generated_Image" src="https://github.com/user-attachments/assets/bc7f6cf3-c329-455d-96db-31f43f2751bf" />

L'analisi visiva dello spazio del grafo, elaborata tramite un algoritmo di disposizione spaziale (layout a forze), mette in evidenza la struttura organizzativa della conoscenza del dipartimento:

* Hub Tematici Centrali: Aree come Deep Learning, Machine Learning, Bioinformatics e Database Systems fungono da grandi attrattori della rete.
* Articoli Connettori: I paper fondamentali si posizionano al centro del grafo, collegando simultaneamente più aree di ricerca e sedi editoriali diverse.
* Cluster Interdisciplinari: Sono evidenti aggregazioni naturali e coerenti che superano i confini delle singole materie (ad esempio, l'intersezione netta tra Deep Learning - Bioinformatics - Nature Methods).
* Sottoreti Verticali: Network più isolati e specialistici descrivono ambiti precisi, come quello relativo ai database d'avanguardia (Database Systems - Graph Databases - VLDB/SIGMOD).

## 4. Vincoli di Integrità e Qualità del Dato

Prima della fase di inserimento dei record, sono state implementate regole native per garantire la pulizia del database:

* Vincoli di Unicità: Applicati su `Author(email)`, `Article(DOI)`, `Topic(nome)`, `Venue(nome)` e `Affiliation(nome)` per impedire la nascita di nodi duplicati.
* Vincoli di Esistenza: Obbligatorietà per le proprietà identificative critiche (es. presenza tassativa di titolo e DOI per gli articoli).

### Fase di Refactoring e Pulizia Post-Seed

Successivamente al caricamento dei dati è stata eseguita una query di controllo per eliminare il "rumore" strutturale:

* Individuazione e correzione di nodi con proprietà incomplete.
*  Fusione o eliminazione di relazioni duplicate sulla stessa coppia di nodi.
*  Eliminazione automatica di topic non trattati, riviste senza articoli associati o università prive di docenti mappati.
*  Ricostruzione logica e pulita delle relazioni di co-autoria (`CO_AUTHORED`).

## 5. Popolamento e Cardinalità

Metriche: 54 Nodi complessivi e 121 Relazioni attive.

Ogni articolo è volutamente associato a più temi per testare la capacità del sistema di calcolare l'interdisciplinarità. I collegamenti di citazione (`CITES`), inoltre, sfruttano l'attributo `context` per isolare i paper usati come fondamenta teoriche da quelli citati semplicemente nello stato dell'arte.

## 6. Query di Analisi Strutturale

Con il database a regime, la suite di interrogazioni in linguaggio Cypher permette di estrarre report descrittivi fondamentali per la governance del dipartimento:

* Classifica dei ricercatori più prolifici e degli articoli con il più alto impatto scientifico.
* Mappatura dei temi di ricerca più battuti e delle sedi editoriali commercialmente più strategiche.
* Rilevamento delle coppie di autori con la collaborazione più stretta in termini di volume di paper scritti insieme.
* Identificazione degli articoli interdisciplinari e dei ricercatori che modificano i propri interessi tematici nel corso della serie storica.

## 7. Analisi Avanzate (Graph Data Science)

Per estrarre conoscenza latente non visibile tramite semplici query descrittive, il grafo è stato proiettato nel modulo **GDS (Graph Data Science)** per eseguire quattro algoritmi avanzati:

* PageRank sulla Rete delle Citazioni: Calcola l'autorevolezza dei paper. Un articolo guadagna un punteggio alto non solo se riceve molte citazioni, ma se viene citato da altri articoli che sono a loro volta nodi autorevoli della rete.
* PageRank sulla Rete di Co-Autoria: Misura la centralità sociale e accademica dei ricercatori, identificando i profili chiave che fanno da ponte tra i vari laboratori del dipartimento.
* Algoritmo di Louvain (Community Detection): Analizza la densità dei collegamenti nella rete delle collaborazioni per dividere automaticamente i docenti in gruppi di ricerca interni stabili e comunità di lavoro reali.
* Label Propagation Algorithm (LPA): Monitora il flusso delle citazioni per intercettare la nascita di cluster tematici emergenti e tendenze scientifiche latenti prima che vengano codificate formalmente dal mercato.

## 8. Conclusione

Il Knowledge Graph realizzato su Neo4j rappresenta una soluzione di alto livello per la gestione della conoscenza accademica. L'integrazione nativa tra la modellazione a grafo, i rigidi vincoli di qualità del dato, le query di analisi in Cypher e gli algoritmi di Graph Data Science fornisce uno strumento strategico in grado di mappare, misurare e prevedere l'evoluzione della produzione scientifica aziendale con performance millisecondate.
