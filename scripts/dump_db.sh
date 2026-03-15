#!/usr/bin/env bash
# Génère un dump PostgreSQL de la base REMEDY (variables REMEDY_DB_*).
# Usage : depuis la racine du projet : ./scripts/dump_db.sh
# Sortie : deploy/remedy_dump_YYYYMMDD_HHMM.sql

set -e
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# Charger .env si présent
if [ -f .env ]; then
    set -a
    source .env
    set +a
fi

# Vérifier si on utilise PostgreSQL
if [ -n "$REMEDY_DB_USE_SQLITE" ] && echo "$REMEDY_DB_USE_SQLITE" | grep -qiE "^(1|true|yes)$"; then
    echo "La config utilise SQLite (REMEDY_DB_USE_SQLITE). Ce script ne fait que des dumps PostgreSQL."
    echo "Pour SQLite, copiez simplement le fichier db.sqlite3."
    exit 1
fi

DB_NAME="${REMEDY_DB_NAME:-remedy}"
DB_USER="${REMEDY_DB_USER:-remedy_user}"
DB_HOST="${REMEDY_DB_HOST:-127.0.0.1}"
DB_PORT="${REMEDY_DB_PORT:-5432}"
export PGPASSWORD="${REMEDY_DB_PASSWORD:-}"

if [ -z "$PGPASSWORD" ]; then
    echo "Erreur : REMEDY_DB_PASSWORD (ou PGPASSWORD) doit être défini (fichier .env ou export)."
    exit 1
fi

mkdir -p deploy
STAMP=$(date +%Y%m%d_%H%M)
OUTFILE="deploy/remedy_dump_${STAMP}.sql"

echo "Dump de la base $DB_NAME (@ $DB_HOST:$DB_PORT) vers $OUTFILE ..."
pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" \
    --no-owner \
    --no-acl \
    --clean \
    --if-exists \
    -F p \
    -f "$OUTFILE"

unset PGPASSWORD
echo "Dump terminé : $OUTFILE"
echo "Pour restaurer sur le VPS : psql -h 127.0.0.1 -U remedy_user -d remedy -f $OUTFILE"
