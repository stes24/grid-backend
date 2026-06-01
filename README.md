# Griglia colorata in tempo reale - Backend

Progetto full-stack che consiste di una tabella di quadrati colorabili da più utenti collegati contemporaneamente. Lo stato della griglia è salvato in un database, e l'aggiornamento della stessa avviene in tempo reale ed è immediatamente visibile dagli altri utenti.\
\
Il progetto è suddiviso in due repository, una per il backend e [una per il frontend](https://github.com/stes24/realtime-grid-frontend).

## Tecnologie usate

- **Database**: PostgreSQL per memorizzare lo stato della griglia e come viene modificata.
- **Backend**: Python + Flask per esporre API REST e supportare la comunicazione con i client tramite WebSocket.
- **Frontend**: JavaScript + React per la creazione dell'interfaccia, Vite per il bundling del frontend.