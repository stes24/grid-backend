from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
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

logging.basicConfig(level=logging.DEBUG)

# QUANDO TI COLLEGHI AI PERCORSI DEFINITI, ESEGUI LA FUNZIONE ASSOCIATA

# Leggi tutti i pixel
@app.route("/pixels", methods=["GET"])
def get_pixels():
    logging.debug("Ricevuta chiamata GET in /pixels")
    conn = get_connection()

    # Oggetto per fare operazioni sul db - esegui SQL e leggi risultati
    cur = conn.cursor()
    cur.execute("SELECT * FROM pixels")
    db_rows = cur.fetchall() # Leggi tutte le tuple
    col_names = [desc[0] for desc in cur.description] # Nomi delle colonne

    # Chiudi connessioni
    cur.close()
    conn.close()

    # Converti le tuple in dizionari con chiavi nominate, poi restituisci come JSON
    pixels = [dict(zip(col_names, r)) for r in db_rows] # zip crea coppie chiave-valore, dict crea dizionario da esse
    logging.debug("Invio tutti i pixel")
    return jsonify(pixels)

# Leggi il pixel con riga e colonna specificati
@app.route("/pixels/<int:row>,<int:col>", methods=["GET"])
def get_single_pixel(row, col):
    logging.debug(f"Ricevuta chiamata GET in /pixels/{row},{col}")
    conn = get_connection()

    cur = conn.cursor()
    cur.execute("SELECT * FROM pixels WHERE pixel_row = %s AND pixel_col = %s", (row, col))
    db_row = cur.fetchone()
    col_names = [desc[0] for desc in cur.description]

    cur.close()
    conn.close()

    if db_row is None:
        logging.debug(f"Pixel {row},{col} non trovato")
        return jsonify({"errore": "Pixel non trovato"}), 404

    pixel = dict(zip(col_names, db_row))
    logging.debug(f"Invio il pixel {row},{col}: {pixel}")
    return jsonify(pixel)

# Aggiorna il colore del pixel con riga e colonna specificati
@app.route("/pixels/<int:row>,<int:col>", methods=["PUT"])
def update_pixel(row, col):
    logging.debug(f"Ricevuta chiamata PUT in /pixels/{row},{col}")
    new_color = request.json.get("color")

    conn = get_connection()

    cur = conn.cursor()
    cur.execute("UPDATE pixels SET color = %s WHERE pixel_row = %s AND pixel_col = %s", (new_color, row, col))
    conn.commit()

    cur.close()
    conn.close()

    logging.debug(f"Aggiornato il pixel {row},{col} al colore {new_color}")
    return jsonify({"pixel_row": row, "pixel_col": col, "color": new_color})

# Esegui solo se il file è eseguito direttamente - previene esecuzione se lo importi
if __name__ == "__main__":
    app.run(debug=True) # True per sviluppo locale, False per produzione (pubblico)