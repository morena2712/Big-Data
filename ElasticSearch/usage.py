import os
import json
from elasticsearch import Elasticsearch, helpers

# 1. Configurazione del Client Elasticsearch (Compatibile con v8.x)
ES_HOST = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
es = Elasticsearch(ES_HOST)

INDEX_NAME = "recensioni_hotel"


def setup_index():
    settings = {
        "analysis": {
            "analyzer": {
                "it_analyzer": {
                    "type": "italian"
                }
            }
        }
    }

    mappings = {
        "properties": {
            "id_recensione": { "type": "keyword" },
            "id_prenotazione": { "type": "keyword" },
            "hotel_codice": { "type": "keyword" },
            "cliente_codice": { "type": "keyword" },
            "punteggio": { "type": "integer" },
            "testo_recensione": {
                "type": "text",
                "analyzer": "it_analyzer"
            },
            "data_recensione": { "type": "date" }
        }
    }



def populate_data():
    recensioni = [
        { "id_recensione": "R001", "id_prenotazione": "P8a7b6c5", "hotel_codice": "H001", "cliente_codice": "C001", "punteggio": 5, "testo_recensione": "Soggiorno fantastico all'Hotel Sole di Ostuni! La camera era provvista di ogni comfort e la pulizia era assolutamente impeccabile. Ci torneremo di sicuro.", "data_recensione": "2026-03-15" },
        { "id_recensione": "R002", "id_prenotazione": "P1f2e3d4", "hotel_codice": "H002", "cliente_codice": "C012", "punteggio": 3, "testo_recensione": "Il resort Mare Blu ha una vista stupenda sul lungomare di Brindisi, ma le camere sono un po' datate. Note dolenti sulla pulizia del bagno, c'era troppa polvere.", "data_recensione": "2026-05-20" },
        { "id_recensione": "R003", "id_prenotazione": "P9z8y7x6", "hotel_codice": "H003", "cliente_codice": "C045", "punteggio": 4, "testo_recensione": "Struttura molto accogliente immersa nel verde a Cisternino. Personale gentilissimo, stanze decisamente pulite e ordinate all'arrivo. Buona anche la colazione.", "data_recensione": "2026-06-10" },
        { "id_recensione": "R004", "id_prenotazione": "P4k3j2h1", "hotel_codice": "H001", "cliente_codice": "C002", "punteggio": 2, "testo_recensione": "Esperienza mediocre. Personale scontroso e letto scomodo. L'unica nota positiva è la posizione centrale a Ostuni, ma il servizio lascia a desiderare.", "data_recensione": "2026-06-12" },
        { "id_recensione": "R005", "id_prenotazione": "P55a1234", "hotel_codice": "H004", "cliente_codice": "C005", "punteggio": 5, "testo_recensione": "Dormire nei trulli di Alberobello è un'esperienza magica. Struttura silenziosa, letto comodissimo e una colazione artigianale da urlo. Tutto super pulito.", "data_recensione": "2026-04-02" },
        { "id_recensione": "R006", "id_prenotazione": "P66b5678", "hotel_codice": "H005", "cliente_codice": "C022", "punteggio": 1, "testo_recensione": "Esperienza pessima a Monopoli. C'era un rumore d'inferno proveniente dal porto tutta la notte, impossibile chiudere occhio. Personale della reception totalmente indifferente.", "data_recensione": "2026-06-25" },
        { "id_recensione": "R007", "id_prenotazione": "P77c9012", "hotel_codice": "H001", "cliente_codice": "C011", "punteggio": 4, "testo_recensione": "Bell'hotel a Ostuni, la colazione a buffet offre molta scelta. Unica pecca il Wi-Fi che andava a rilento nella nostra stanza. Camere comunque ben pulite ordinizzate.", "data_recensione": "2026-07-01" },
        { "id_recensione": "R008", "id_prenotazione": "P88d3456", "hotel_codice": "H002", "cliente_codice": "C033", "punteggio": 2, "testo_recensione": "Prezzo decisamente troppo alto per i servizi offerti a Brindisi. Il servizio clienti è stato pessimo e la pulizia della doccia lasciava molto a desiderare. Sconsigliato.", "data_recensione": "2026-07-15" },
        { "id_recensione": "R009", "id_prenotazione": "P99e7890", "hotel_codice": "H003", "cliente_codice": "C009", "punteggio": 5, "testo_recensione": "Un'oasi di pace a Cisternino! Il personale ci ha trattato come re. Stanze pulitissime, profumate e aria condizionata perfetta. Rapporto qualità prezzo imbattibile.", "data_recensione": "2026-08-10" },
        { "id_recensione": "R010", "id_prenotazione": "P10f1112", "hotel_codice": "H004", "cliente_codice": "C050", "punteggio": 3, "testo_recensione": "I trulli sono splendidi ma la stanza era un po' umida e fredda. Personale accogliente e colazione accettabile, ma si può fare di meglio sui servizi.", "data_recensione": "2026-08-22" },
        { "id_recensione": "R011", "id_prenotazione": "P11g1314", "hotel_codice": "H005", "cliente_codice": "C071", "punteggio": 4, "testo_recensione": "Posizione fantastica a Monopoli vicino alle spiagge. Camera pulita e spaziosa. Un po' di rumore la sera dovuto alla movida, ma tollerabile.", "data_recensione": "2026-09-05" },
        { "id_recensione": "R012", "id_prenotazione": "P12a0012", "hotel_codice": "H001", "cliente_codice": "C015", "punteggio": 5, "testo_recensione": "Fine settimana perfetto a Ostuni. Il personale è stato squisito e la stanza era pulitissima, profumava di fresco fin dall'ingresso.", "data_recensione": "2026-01-20" },
        { "id_recensione": "R013", "id_prenotazione": "P13b0034", "hotel_codice": "H002", "cliente_codice": "C042", "punteggio": 2, "testo_recensione": "Purtrohto devo fare una nota negativa sul resort di Brindisi. C'era un cattivo odore in corridoio e gli asciugamani in bagno erano visibilmente sporchi.", "data_recensione": "2026-02-14" },
        { "id_recensione": "R014", "id_prenotazione": "P14c0056", "hotel_codice": "H003", "cliente_codice": "C003", "punteggio": 4, "testo_recensione": "Collina Verde è una garanzia di relax a Cisternino. Struttura curata, piscina molto pulita e igienizzata, anche se il servizio a bordo vasca è un po' lento.", "data_recensione": "2026-03-05" },
        { "id_recensione": "R015", "id_prenotazione": "P15d0078", "hotel_codice": "H004", "cliente_codice": "C018", "punteggio": 3, "testo_recensione": "Dormire nel trullo è suggestivo, ma gli spazi sono ridotti. Purtroppo la pulizia del bagno lasciava un po' a desiderare al nostro arrivo, ragnatele ovunque.", "data_recensione": "2026-05-11" },
        { "id_recensione": "R016", "id_prenotazione": "P16e0090", "hotel_codice": "H005", "cliente_codice": "C060", "punteggio": 5, "testo_recensione": "Soggiorno da sogno a Monopoli! Vista mare incredibile, camera splendente di pulito e personale della reception sempre pronto a soddisfare ogni nostra richiesta.", "data_recensione": "2026-06-02" },
        { "id_recensione": "R017", "id_prenotazione": "P17f0111", "hotel_codice": "H001", "cliente_codice": "C025", "punteggio": 1, "testo_recensione": "Un disastro totale in piena estate a Ostuni. Camera non pulita all'arrivo, c'era polvere sui mobili e lo staff del servizio camere ha risposto in modo sgarbato alle nostre lamentele.", "data_recensione": "2026-07-10" },
        { "id_recensione": "R018", "id_prenotazione": "P18g0222", "hotel_codice": "H002", "cliente_codice": "C034", "punteggio": 4, "testo_recensione": "Soggiornato per lavoro a Brindisi. Il personale si è dimostrato molto efficiente e professionale. Stanze base ma con un ottimo livello di igiene generale.", "data_recensione": "2026-07-22" },
        { "id_recensione": "R019", "id_prenotazione": "P19h0333", "hotel_codice": "H003", "cliente_codice": "C077", "punteggio": 5, "testo_recensione": "Esperienza culinaria e di soggiorno fantastica a Cisternino. Massima igiene riscontrata sia nella sala ristorante che nelle camere. Complimenti a tutto il personale.", "data_recensione": "2026-08-05" },
        { "id_recensione": "R020", "id_prenotazione": "P20i0444", "hotel_codice": "H004", "cliente_codice": "C008", "punteggio": 2, "testo_recensione": "Caldo insopportabile ad agosto e l'aria condizionata del trullo era rotta. Abbiamo chiesto assistenza ma il personale è stato scortese e non ha risolto il problema. Servizio pessimo.", "data_recensione": "2026-08-18" },
        { "id_recensione": "R021", "id_prenotazione": "P21j0555", "hotel_codice": "H005", "cliente_codice": "C019", "punteggio": 3, "testo_recensione": "Bella la posizione a Monopoli, ma l'hotel era troppo affollato a fine agosto. Zona piscina caotica e lettini esterni visibilmente sporchi e non igienizzati a dovere.", "data_recensione": "2026-08-30" },
        { "id_recensione": "R022", "id_prenotazione": "P22k0666", "hotel_codice": "H001", "cliente_codice": "C054", "punteggio": 4, "testo_recensione": "Weekend romantico a Ostuni. Ottima la spa interna e buona l'igiene della camera. Il personale del centro benessere è stato davvero accogliente.", "data_recensione": "2026-09-12" },
        { "id_recensione": "R023", "id_prenotazione": "P23l0777", "hotel_codice": "H002", "cliente_codice": "C031", "punteggio": 1, "testo_recensione": "Notte orribile a Brindisi per via di schiamazzi continui nei corridoi. Il servizio di sorveglianza dell'hotel non è intervenuto. Struttura sporca e trascurata.", "data_recensione": "2026-10-01" },
        { "id_recensione": "R024", "id_prenotazione": "P24m0888", "hotel_codice": "H003", "cliente_codice": "C004", "punteggio": 5, "testo_recensione": "Relax autunnale a Cisternino. Camera pulitissima all'arrivo, accoglienza calorosa dello staff e ottimi consigli sui ristoranti della zona. Servizio al top.", "data_recensione": "2026-11-03" },
        { "id_recensione": "R025", "id_prenotazione": "P25n0999", "hotel_codice": "H004", "cliente_codice": "C049", "punteggio": 4, "testo_recensione": "Magica atmosfera invernale ad Alberobello. Struttura ben riscaldata, pulita e confortevole. Un po' carente il servizio colazione, ma accettabile.", "data_recensione": "2026-12-20" },
        { "id_recensione": "R026", "id_prenotazione": "P26o1122", "hotel_codice": "H005", "cliente_codice": "C014", "punteggio": 2, "testo_recensione": "Stanza fredda e umida per il nostro soggiorno di fine anno a Monopoli. Nota dolente sulla pulizia generale, c'era sporco sotto il letto e polvere accumulata sui radiatori.", "data_recensione": "2026-12-28" }
    ]

    actions = [
        {
            "_index": INDEX_NAME,
            "_id": r["id_recensione"],
            "_source": r
        }
        for r in recensioni
    ]

    helpers.bulk(es, actions)
    es.indices.refresh(index=INDEX_NAME)


def run_queries():
    # 1. Rating Medio Storico per Struttura
    aggs1 = {
        "hotel_raggruppati": {
            "terms": { "field": "hotel_codice" },
            "aggs": {
                "voto_medio": { "avg": { "field": "punteggio" } }
            }
        }
    }
    
    res1 = es.search(index=INDEX_NAME, size=0, aggs=aggs1)
    for bucket in res1['aggregations']['hotel_raggruppati']['buckets']:
        print(f"Hotel: {bucket['key']} | Feedback Ricevuti: {bucket['doc_count']} | Rating Medio: {bucket['voto_medio']['value']:.2f}")

    # 2. Servizio e Personale Criticati
    query2 = {
        "bool": {
            "must": [
                { "multi_match": { "query": "personale servizio", "fields": ["testo_recensione"] } }
            ],
            "filter": [
                { "range": { "punteggio": { "lte": 2 } } }
            ]
        }
    }
    
    res2 = es.search(index=INDEX_NAME, query=query2)
    print(f"Trovate {res2['hits']['total']['value']} criticità gravi rilevate:")
    for hit in res2['hits']['hits']:
        src = hit['_source']
        print(f"[{src['id_recensione']}] Hotel {src['hotel_codice']} | Punteggio: {src['punteggio']} | Data: {src['data_recensione']}")
        print(f"Feedback: {src['testo_recensione']}\n")

    # 3. Analisi Inquinamento Acustico / Movida Estiva
    query3 = {
        "bool": {
            "must": [
                { 
                    "match": { 
                        "testo_recensione": { 
                            "query": "rumore rumorosa caos caotica schiamazzi disturbo baccano", 
                            "operator": "or",
                            "fuzziness": "AUTO"
                        } 
                    } 
                }
            ],
            "filter": [
                { 
                    "range": { 
                        "data_recensione": { 
                            "gte": "2026-06-01", 
                            "lte": "2026-09-15" 
                        } 
                    } 
                }
            ]
        }
    }
    
    res3 = es.search(index=INDEX_NAME, query=query3)
    print(f"Trovate {res3['hits']['total']['value']} segnalazioni di disturbo acustico nel periodo estivo:")
    for hit in res3['hits']['hits']:
        src = hit['_source']
        print(f"[{src['id_recensione']}] Data: {src['data_recensione']} | Hotel: {src['hotel_codice']} | Punteggio: {src['punteggio']}")
        print(f"Feedback: {src['testo_recensione']}\n")

    # 4. Recensioni sulla pulizia
    query4 = {
        "match": { 
            "testo_recensione": { 
                "query": "pulizia igiene sporco pulito splendente polvere", 
                "operator": "or",
                "fuzziness": "AUTO"
            } 
        }
    }
    
    res4 = es.search(index=INDEX_NAME, query=query4)
    print(f"Trovate {res4['hits']['total']['value']} recensioni totali sul tema Pulizia/Igiene:")
    for hit in res4['hits']['hits']:
        src = hit['_source']
        print(f"[{src['id_recensione']}] Data: {src['data_recensione']} | Hotel: {src['hotel_codice']} | Voto: {src['punteggio']}")
        print(f"Feedback: {src['testo_recensione']}\n")


if __name__ == "__main__":
    print("Inizializzazione script di gestione analitica...")
    if es.ping():
        print("Connessione con il cluster Elasticsearch stabilita.")
        setup_index()
        populate_data()
        run_queries()
        print("Sincronizzazione ed esecuzione completate con successo.")
    else:
        print("Errore critico: Impossibile raggiungere il server Elasticsearch su", ES_HOST)
