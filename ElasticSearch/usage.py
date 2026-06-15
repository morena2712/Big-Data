from elasticsearch import Elasticsearch

def print_results(title, results):
    print(f"\n=== {title} ===")
    hits = results.get("hits", {}).get("hits", [])
    if not hits:
        print("Nessun risultato trovato.")
    for h in hits:
        print(h["_source"])

def main():
    # Connessione al cluster Elasticsearch
    es = Elasticsearch("http://localhost:9200")

    # -------------------------------
    # 1) PRENOTAZIONI HOTEL
    # -------------------------------

    # Query 1: prenotazioni in un intervallo
    query1 = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"hotel_id": "H001"}}
                ],
                "filter": [
                    {"range": {"data_arrivo": {"lte": "2026-06-30"}}},
                    {"range": {"data_partenza": {"gte": "2026-06-01"}}}
                ]
            }
        }
    }
    res1 = es.search(index="prenotazioni", body=query1)
    print_results("Prenotazioni Hotel H001 nel range", res1)

    # Query 2: clienti con più prenotazioni
    query2 = {
        "size": 0,
        "aggs": {
            "clienti_top": {
                "terms": {
                    "field": "cliente_id",
                    "size": 10,
                    "order": {"_count": "desc"}
                },
                "aggs": {
                    "dati_cliente": {
                        "top_hits": {
                            "size": 1,
                            "_source": ["cliente_nome", "cliente_cognome"]
                        }
                    }
                }
            }
        }
    }
    res2 = es.search(index="prenotazioni", body=query2)
    print("\n=== Clienti con più prenotazioni ===")
    print(res2["aggregations"]["clienti_top"]["buckets"])

    # -------------------------------
    # 2) PUBBLICAZIONI SCIENTIFICHE
    # -------------------------------

    # Query 3: articoli che citano un DOI
    query3 = {
        "query": {
            "term": {"cita": "10.1000/A1"}
        }
    }
    res3 = es.search(index="articoli", body=query3)
    print_results("Articoli che citano 10.1000/A1", res3)

    # Query 4: autori che pubblicano su ML
    query4 = {
        "size": 0,
        "query": {
            "term": {"temi": "machine learning"}
        },
        "aggs": {
            "autori_ml": {
                "terms": {
                    "field": "autori.autore_id",
                    "size": 10
                }
            }
        }
    }
    res4 = es.search(index="articoli", body=query4)
    print("\n=== Autori che pubblicano su Machine Learning ===")
    print(res4["aggregations"]["autori_ml"]["buckets"])

    # Query 5: coppie di coautori
    query5 = {
        "size": 0,
        "aggs": {
            "coautori": {
                "nested": {"path": "autori"},
                "aggs": {
                    "autori": {
                        "terms": {"field": "autori.autore_id", "size": 10},
                        "aggs": {
                            "co": {
                                "terms": {"field": "autori.autore_id", "size": 10}
                            }
                        }
                    }
                }
            }
        }
    }
    res5 = es.search(index="articoli", body=query5)
    print("\n=== Coppie di coautori ===")
    print(res5["aggregations"]["coautori"]["autori"]["buckets"])


if __name__ == "__main__":
    main()
