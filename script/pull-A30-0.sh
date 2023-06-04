#!/bin/bash

# Configurazione delle informazioni di connessione SSH
HOST="A30_0"
USERNAME="guido"

# Ottieni il nome del repository dalla cartella corrente
REPO_NAME=$(basename "$(cd .. && pwd)")

# URL del repository su GitHub
REPO_URL="git@github.com:nome_utente/$REPO_NAME.git"

# Directory di destinazione per il clone del repository
DEST_DIR="~/repos/$REPO_NAME"

# Comando per verificare se il repository esiste già
CHECK_REPO_COMMAND="[ -d \"$DEST_DIR/.git\" ]"

# Connessione SSH e verifica se il repository esiste
ssh -t "$USERNAME@$HOST" "$CHECK_REPO_COMMAND"

# Se il repository non esiste, clonalo
if [ $? -ne 0 ]; then
    ssh -t "$USERNAME@$HOST" "git clone $REPO_URL $DEST_DIR"
fi

# Esegui il pull del repository
ssh -t "$USERNAME@$HOST" "cd $DEST_DIR && git pull"