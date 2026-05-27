from dotenv import load_dotenv
from flask import Flask, jsonify
import os
import psycopg2

# Prendi variabili d'ambiente del db
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Crea oggetto di classe Flask per dargli il contesto (dove cercare i file)
app = Flask(__name__)

# QUANDO VISITI I PERCORSI DEFINITI, ESEGUI LA FUNZIONE ASSOCIATA

@app.route('/') # Di default, la route risponde solo a richieste GET
def get_pixels():
    # Connessione al db
    conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD)

    # Oggetto per fare operazioni sul db - esegui SQL e leggi risultati
    cur = conn.cursor()
    cur.execute("SELECT * FROM pixels")
    rows = cur.fetchall() # Leggi tutte le righe

    # Chiudi connessioni
    cur.close()
    conn.close()

    # Restituisci i dati come JSON al browser
    return jsonify(rows)

# Esegui solo se il file è eseguito direttamente - previene esecuzione se lo importi
if __name__ == "__main__":
    app.run(debug=True) # True per sviluppo locale, False per produzione (pubblico)