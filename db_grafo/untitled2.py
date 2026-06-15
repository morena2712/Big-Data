!pip install neo4j

from neo4j import GraphDatabase

URI = "neo4j://127.0.0.1:7687"
USER = "neo4j"
PASSWORD = "AAAAAAAAH"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def run_query(query, description):
    print("\n" + "="*80)
    print(description)
    print("="*80)

    with driver.session() as session:
        result = session.run(query)
        for record in result:
            print(record)


# 1. Trovare tutti gli articoli che citano un determinato articolo

query_citing_articles = """
MATCH (citing:Article)-[:CITES]->(target:Article {title: 'Self-Supervised Learning for Protein Structure Prediction'})
RETURN citing;
"""


# 2. Autori che hanno pubblicato sullo stesso tema ma non hanno collaborato

query_authors_same_topic_no_collab = """
MATCH (a1:Author)-[:AUTHORED_BY]-(ar1:Article)-[:COVERS]->(t:Topic),
      (a2:Author)-[:AUTHORED_BY]-(ar2:Article)-[:COVERS]->(t)
      WHERE id(a1) < id(a2)
  AND NOT (a1)-[:CO_AUTHORED]-(a2)
RETURN t.name AS topic,
       a1.firstName + ' ' + a1.surname AS author1,
       a2.firstName + ' ' + a2.surname AS author2
ORDER BY topic;
"""


# 3. Articoli più citati

query_most_cited_articles = """
MATCH (ar:Article)
RETURN ar.title AS title,
       ar.citations AS citationCount
ORDER BY citationCount DESC
LIMIT 5;
"""


# 4.Topic più trattati

query_most_frequent_topics = """
MATCH (ar:Article)-[:COVERS]->(t:Topic)
RETURN t.name AS topic,
       count(ar) AS numArticles
ORDER BY numArticles DESC
LIMIT 5;
"""

# ESECUZIONE DELLE QUERY

if __name__ == "__main__":

    run_query(query_citing_articles,
              "1) Articoli che citano un determinato articolo")

    run_query(query_authors_same_topic_no_collab,
              "2) Autori che pubblicano sullo stesso tema ma non collaborano")

    run_query(query_most_cited_articles,
              "3) Articoli più citati")

    run_query(query_most_frequent_topics,
              "4) Topic più trattati")

    driver.close()