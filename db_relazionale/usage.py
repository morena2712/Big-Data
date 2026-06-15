!pip install mysql-connector-python

import mysql.connector

def connect_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="OlivaMorena-17",
        database="db_alberghiero"
    )
    return conn


# 1. Totale prenotazioni

def totale_prenotazioni(conn):
    query = """
        SELECT COUNT(*) AS totale_prenotazioni
        FROM Prenotazione;
    """
    cur = conn.cursor(dictionary=True)
    cur.execute(query)
    result = cur.fetchone()
    print("Totale prenotazioni:", result["totale_prenotazioni"])


# 2. Fatturato totale

def fatturato_totale(conn):
    query = """
        SELECT SUM(importo_totale) AS fatturato_totale
        FROM Prenotazione
        WHERE stato_prenotazione IN ('Completata', 'In corso');
    """
    cur = conn.cursor(dictionary=True)
    cur.execute(query)
    result = cur.fetchone()
    print("Fatturato totale:", result["fatturato_totale"])


# 3. Clienti con prenotazioni attive

def clienti_attivi(conn):
    query = """
        SELECT DISTINCT
            c.codice_cliente,
            c.nome,
            c.cognome
        FROM Prenotazione p
        JOIN Cliente c
            ON c.codice_cliente = p.cliente_codice
        WHERE p.stato_prenotazione IN ('In attesa', 'Confermata', 'In corso');
    """
    cur = conn.cursor(dictionary=True)
    cur.execute(query)
    results = cur.fetchall()

    print("\nClienti con prenotazioni attive:")
    for row in results:
        print(f"- {row['codice_cliente']} | {row['nome']} {row['cognome']}")


# 4. Prenotazioni di un hotel in un intervallo di date

def prenotazioni_hotel_intervallo(conn, hotel_codice, data_inizio, data_fine):
    query = """
        SELECT *
        FROM Prenotazione
        WHERE hotel_codice = %s
          AND data_arrivo >= %s
          AND data_partenza <= %s
        ORDER BY data_arrivo;
    """
    cur = conn.cursor(dictionary=True)
    cur.execute(query, (hotel_codice, data_inizio, data_fine))
    results = cur.fetchall()

    print(f"\nPrenotazioni per hotel {hotel_codice} tra {data_inizio} e {data_fine}:")
    for row in results:
        print(f"- Prenotazione {row['id_prenotazione']} | Arrivo: {row['data_arrivo']} | Partenza: {row['data_partenza']}")


# 5. Clienti con il maggior numero di prenotazioni

def clienti_con_piu_prenotazioni(conn, limite=5):
    query = """
        SELECT 
            c.codice_cliente,
            c.nome,
            c.cognome,
            COUNT(*) AS numero_prenotazioni
        FROM Prenotazione p
        JOIN Cliente c
            ON c.codice_cliente = p.cliente_codice
        GROUP BY c.codice_cliente, c.nome, c.cognome
        ORDER BY numero_prenotazioni DESC
        LIMIT %s;
    """
    cur = conn.cursor(dictionary=True)
    cur.execute(query, (limite,))
    results = cur.fetchall()

    print(f"\nTop {limite} clienti con più prenotazioni:")
    for row in results:
        print(f"- {row['nome']} {row['cognome']} ({row['codice_cliente']}) | Prenotazioni: {row['numero_prenotazioni']}")


def main():
    conn = connect_db()

    print("\n=== 1) Totale prenotazioni ===")
    totale_prenotazioni(conn)

    print("\n=== 2) Fatturato totale ===")
    fatturato_totale(conn)

    print("\n=== 3) Clienti con prenotazioni attive ===")
    clienti_attivi(conn)

    print("\n=== 4) Prenotazioni di un hotel in un intervallo di date ===")
    prenotazioni_hotel_intervallo(conn, "H001", "2026-06-01", "2026-06-30")

    print("\n=== 5) Clienti con il maggior numero di prenotazioni ===")
    clienti_con_piu_prenotazioni(conn, limite=5)

    conn.close()


if __name__ == "__main__":
    main()
