# Griglia colorata in tempo reale - Backend

Progetto full-stack che consiste di una tabella di quadrati colorabili da più utenti collegati contemporaneamente. Lo stato della griglia è salvato in un database, e l'aggiornamento della stessa avviene in tempo reale ed è immediatamente visibile da tutti gli utenti.\
Il progetto è suddiviso in due repository, una per il backend e [una per il frontend](https://github.com/stes24/realtime-grid-frontend).\
\
[LINK ALL'APPLICAZIONE](https://realtime-grid-frontend-production.up.railway.app)

## Tecnologie usate

- **Database**: PostgreSQL per memorizzare lo stato della griglia e come viene modificata.
- **Backend**: Python + Flask per esporre API REST e supportare la comunicazione con i client tramite WebSocket.
- **Frontend**: JavaScript + React per la creazione dell'interfaccia, Vite per il bundling del frontend.

## Installazione ed esecuzione

### Backend

- Scaricare la repository
- Creare e popolare il database PostgreSQL:
  ```SQL
  CREATE TABLE pixels (
      pixel_row INT NOT NULL,
      pixel_col INT NOT NULL,
      color varchar(7) NOT NULL DEFAULT '#FFFFFF',
      PRIMARY KEY (pixel_row, pixel_col)
  )

  INSERT INTO pixels (pixel_row, pixel_col)
  SELECT r, c
  FROM generate_series(0, 9) AS r, generate_series(0, 9) AS c
  ```
- Impostare in .env le variabili d'ambiente del database (```DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD```)
- Installare le librerie nell'ambiente virtuale:
  ```
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  pip install -r requirements.txt
  ```
- Avviare il server nell'ambiente virtuale (```python app.py```)

### Frontend

- Scaricare la repository
- Installare le librerie (```npm install```)
- Impostare in .env la variabile d'ambiente del backend (```VITE_BACKEND_URL=http://localhost:5000```)
- Avviare con ```npm run dev``` e collegarsi a ```http://localhost:5173```