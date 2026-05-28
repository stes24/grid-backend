from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_cors import CORS
import os
import psycopg2

# Prendi variabili d'ambiente del db
load_dotenv()
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Connessione al db
def get_connection():
    return psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD)

# Crea oggetto di classe Flask per dargli il contesto (dove cercare i file)
app = Flask(__name__)

# Permette richieste cross-origin solo dall'URL del frontend
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
CORS(app, origins=[FRONTEND_URL])

# QUANDO TI COLLEGHI AI PERCORSI DEFINITI, ESEGUI LA FUNZIONE ASSOCIATA

# Leggi tutti i pixel
@app.route("/pixels", methods=["GET"])
def get_pixels():
    conn = get_connection()

    # Oggetto per fare operazioni sul db - esegui SQL e leggi risultati
    cur = conn.cursor()
    cur.execute("SELECT * FROM pixels")
    rows = cur.fetchall() # Leggi tutte le righe

    # Chiudi connessioni
    cur.close()
    conn.close()

    # Restituisci i dati come JSON al browser
    return jsonify(rows)

# Leggi il pixel con ID specificato
@app.route("/pixels/<int:id>", methods=["GET"])
def get_pixel_by_id(id):
    conn = get_connection()

    cur = conn.cursor()
    cur.execute("SELECT * FROM pixels WHERE id = %s", (id,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    if row is None:
        return jsonify({"errore": "Pixel non trovato"}), 404

    return jsonify(row)
    
# Esegui solo se il file è eseguito direttamente - previene esecuzione se lo importi
if __name__ == "__main__":
    app.run(debug=True) # True per sviluppo locale, False per produzione (pubblico)