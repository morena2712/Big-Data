# **Database a Grafo (Neo4j)**

## **1. Obiettivo del modello**
Il database a grafo rappresenta un **knowledge graph della produzione scientifica**, progettato per modellare articoli, autori, affiliazioni, venue, topic e relazioni di citazione.  
L’obiettivo è ottenere una struttura:

- coerente e priva di duplicati  
- semanticamente ricca  
- adatta sia a interrogazioni strutturali sia ad analisi avanzate tramite Graph Data Science  

## **2. Schema concettuale**
Il grafo è composto da cinque categorie principali di nodi:

- **Article** – titolo, DOI, anno, abstract, numero di citazioni  
- **Author** – nome, cognome, email, area di ricerca, h-index  
- **Topic** – nome e descrizione dell’area tematica  
- **Venue** – nome, tipo (Conference/Journal), impact factor  
- **Affiliation** – istituzione di appartenenza degli autori  

Le relazioni modellano:

- **AUTHORED_BY**: autore di un articolo  
- **AFFILIATED_WITH**: istituzione dell’autore  
- **PUBLISHED_IN**: venue di pubblicazione  
- **COVERS**: topic trattati dall’articolo (con proprietà *relevance*)  
- **CITES**: citazioni tra articoli (con proprietà *context*)  
- **CO_AUTHORED**: collaborazione tra autori (derivata)  

<img width="1600" height="1600" alt="Code_Generated_Image" src="https://github.com/user-attachments/assets/6da4c73b-7ace-472a-a6d6-ea679d15a265" />

## **3. Interpretazione del grafo**
Il grafo mostra:

- topic centrali come **Deep Learning**, **Machine Learning**, **Bioinformatics**, **Database Systems**  
- articoli hub collegati a molti topic e venue  
- cluster tematici coerenti (es. Deep Learning ↔ Bioinformatics ↔ Nature Methods)  
- sottoreti legate a Database Systems e Graph Databases (VLDB, SIGMOD)

La disposizione spaziale tramite layout a forze rende visibili:

- comunità  
- sottogruppi tematici  
- connessioni interdisciplinari  

## **4. Vincoli e qualità dei dati**
La costruzione del grafo parte dalla definizione di:

- **vincoli di unicità** (email autore, DOI articolo, nome topic, nome venue, nome affiliazione)  
- **vincoli di esistenza** per proprietà identificative (es. DOI, titolo, email)

Successivamente è stata eseguita una fase di **verifica e pulizia**, che ha incluso:

- ricerca di nodi con proprietà mancanti  
- eliminazione di relazioni duplicate  
- rimozione di nodi orfani (topic non trattati, venue senza articoli, affiliazioni senza autori)  
- ricostruzione corretta delle relazioni CO_AUTHORED  

Questa fase garantisce un grafo consistente e privo di rumore.


## **5. Popolamento del grafo**
Il grafo finale contiene:

- 54 nodi  
- 121 relazioni

Sono stati creati:

- 10 topic  
- 10 venue  
- 10 affiliazioni  
- 12 autori  
- 15 articoli  

Ogni articolo è collegato a più topic tramite `COVERS`, modellando anche l’interdisciplinarità.  
Le citazioni includono un attributo *context* per distinguere il ruolo della citazione (es. *methodology*, *foundation*, *related work*).


## **6. Analisi strutturali**
Una volta pulito il grafo, sono state eseguite query per:

- autori più prolifici  
- articoli più citati  
- topic più trattati  
- venue più attive  
- coppie di autori che collaborano di più  
- autori che cambiano tema nel tempo  
- articoli interdisciplinari  

Queste interrogazioni forniscono una panoramica descrittiva della rete scientifica.


## **7. Analisi avanzate (Graph Data Science)**
Il grafo è stato proiettato in strutture specifiche per applicare algoritmi GDS:

* **PageRank sulla rete delle citazioni**: identifica gli articoli più influenti considerando sia il numero sia la qualità delle citazioni;

* **PageRank sulla rete di co‑autoria**: misura l’influenza sociale degli autori nella rete delle collaborazioni;

* **Louvain (community detection)**: individua gruppi di ricerca e comunità tematiche nella rete di co‑autoria;

* **Label Propagation**: rileva cluster tematici emergenti nella rete delle citazioni, evidenziando strutture latenti.


## **8. Conclusione**
Il knowledge graph realizzato è un ecosistema informativo completo, pulito e coerente, capace di supportare:

- analisi bibliometriche  
- studio delle collaborazioni  
- esplorazione tematica  
- rilevazione di comunità  
- identificazione di strutture latenti  

L’integrazione tra modellazione, pulizia dei dati, query analitiche e algoritmi GDS dimostra la solidità del modello e la sua capacità di rappresentare efficacemente la complessità della produzione scientifica.
