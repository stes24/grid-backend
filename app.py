from dotenv import load_dotenv
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
conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD)

# Oggetto per fare operazioni sul db - esegui SQL e leggi risultati
cur = conn.cursor()
cur.execute("SELECT * FROM pixels")
for row in cur:
    print(row)

# Chiudi connessioni
cur.close()
conn.close()