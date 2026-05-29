from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import emit, SocketIO
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

logging.basicConfig(level=logging.DEBUG)

# Crea oggetto di classe Flask per dargli il contesto (dove cercare i file)
app = Flask(__name__)

# URL del frontend (usato sia per CORS delle API REST che per il WebSocket)
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
CORS(app, origins=[FRONTEND_URL]) # CORS per le API REST
socketio = SocketIO(app, cors_allowed_origins=FRONTEND_URL) # CORS per il WebSocket

# QUANDO TI COLLEGHI AI PERCORSI DEFINITI, ESEGUI LA FUNZIONE ASSOCIATA

# Leggi tutti i pixel
@app.route("/pixels", methods=["GET"])
def get_pixels():
    logging.debug("GET /pixels - Ricevuta chiamata")

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
    logging.debug("GET /pixels - Invio tutti i pixel")
    return jsonify(pixels)

# Leggi il pixel con riga e colonna specificati
@app.route("/pixels/<int:row>,<int:col>", methods=["GET"])
def get_single_pixel(row, col):
    logging.debug(f"GET /pixels/{row},{col} - Ricevuta chiamata")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM pixels WHERE pixel_row = %s AND pixel_col = %s", (row, col))
    db_row = cur.fetchone()
    col_names = [desc[0] for desc in cur.description]

    cur.close()
    conn.close()

    if db_row is None:
        logging.debug(f"GET /pixels/{row},{col} - Pixel non trovato")
        return jsonify({"errore": "Pixel non trovato"}), 404

    pixel = dict(zip(col_names, db_row))
    logging.debug(f"GET /pixels/{row},{col} - Invio il pixel: {pixel}")
    return jsonify(pixel)

# Aggiorna il colore del pixel con riga e colonna specificati (come esempio, non usato)
@app.route("/pixels/<int:row>,<int:col>", methods=["PUT"])
def update_pixel(row, col):
    logging.debug(f"PUT /pixels/{row},{col} - Ricevuta chiamata")

    new_color = request.json.get("color")
    if not new_color:
        logging.debug(f"PUT /pixels/{row},{col} - Colore mancante")
        return jsonify({"errore": "Colore mancante"}), 400

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE pixels SET color = %s WHERE pixel_row = %s AND pixel_col = %s", (new_color, row, col))
    conn.commit()

    cur.close()
    conn.close()

    updated_pixel = {"pixel_row": row, "pixel_col": col, "color": new_color}
    logging.debug(f"PUT /pixels/{row},{col} - Aggiornato il pixel: {updated_pixel}")
    return jsonify(updated_pixel)

# OPERAZIONI SOCKET

@socketio.on("connect")
def connect_handler():
    client_id = request.sid
    logging.debug(f"ID {client_id} - Client connesso")
    emit("message", f"Benvenuto, sei il client {client_id}")

@socketio.on("disconnect")
def disconnect_handler():
    logging.debug(f"ID {request.sid} - Client disconnesso")

@socketio.on("update_pixel")
def update_pixel_handler(data):
    client_id = request.sid
    row = data.get("pixel_row")
    col = data.get("pixel_col")
    new_color = data.get("color")

    if row is None or col is None or not new_color:
        logging.debug(f"ID {client_id} - Dati mancanti: {data}")
        emit("error", {"errore": "Dati mancanti"})
        return
    logging.debug(f"ID {client_id} - Aggiornare il pixel nel db: {data}")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE pixels SET color = %s WHERE pixel_row = %s AND pixel_col = %s", (new_color, row, col))
    conn.commit()

    cur.close()
    conn.close()

    logging.debug(f"ID {client_id} - Invio broadcast: {data}")
    emit("update_pixel", {"pixel_row": row, "pixel_col": col, "color": new_color}, broadcast=True)

# Esegui solo se il file è eseguito direttamente - previene esecuzione se lo importi
if __name__ == "__main__":
    socketio.run(app, debug=True) # True per sviluppo locale, False per produzione (pubblico)