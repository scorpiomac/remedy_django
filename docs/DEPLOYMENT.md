# Guide de déploiement REMEDY (VPS)

Déploiement rapide sur un VPS avec bonnes pratiques **performance** et **sécurité**.

---

## Sommaire

1. [Prérequis](#1-prérequis)
2. [Préparation du serveur](#2-préparation-du-serveur)
3. [Base de données PostgreSQL](#3-base-de-données-postgresql)
4. [Application Django](#4-application-django)
5. [Serveur web et WSGI](#5-serveur-web-et-wsgi)
6. [SSL / HTTPS](#6-ssl--https)
7. [Sécurité](#7-sécurité)
8. [Performance](#8-performance)
9. [Dump et restauration de la base](#9-dump-et-restauration-de-la-base)
10. [Checklist finale](#10-checklist-finale)

---

## 1. Prérequis

- **VPS** : Ubuntu 22.04 LTS (ou Debian 12) recommandé
- **Accès** : root ou utilisateur sudo
- **Domaine** : pointez l’A record vers l’IP du VPS (ex. `remedy.example.com`)

| Composant   | Version minimale |
|------------|-------------------|
| Python     | 3.11+             |
| PostgreSQL | 14+               |
| Nginx      | 1.18+ (ou LiteSpeed / autre) |

---

## 2. Préparation du serveur

### 2.1 Mise à jour et paquets de base

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y build-essential libpq-dev python3-venv python3-dev git curl
```

### 2.2 Utilisateur dédié (recommandé)

```bash
sudo adduser --disabled-password --gecos "" remedy
sudo usermod -aG sudo remedy  # ou sans sudo si déploiement restreint
```

### 2.3 Pare-feu

```bash
sudo ufw allow 22/tcp    # SSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 2.4 Répertoire d’application

```bash
sudo mkdir -p /var/www/remedy
sudo chown remedy:remedy /var/www/remedy
```

---

## 3. Base de données PostgreSQL

### 3.1 Installation

```bash
sudo apt install -y postgresql postgresql-contrib
sudo systemctl enable postgresql
sudo systemctl start postgresql
```

### 3.2 Création base et utilisateur

```bash
sudo -u postgres psql << 'EOF'
CREATE USER remedy_user WITH PASSWORD 'CHANGEZ_MOT_DE_PASSE_FORT';
CREATE DATABASE remedy OWNER remedy_user ENCODING 'UTF8' LC_COLLATE='fr_FR.UTF-8' LC_CTYPE='fr_FR.UTF-8';
\c remedy
GRANT ALL PRIVILEGES ON DATABASE remedy TO remedy_user;
GRANT ALL ON SCHEMA public TO remedy_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO remedy_user;
EOF
```

Remplacez `CHANGEZ_MOT_DE_PASSE_FORT` par un mot de passe fort (générateur ou `openssl rand -base64 32`).

### 3.3 Restauration d’un dump (optionnel)

Si vous avez un dump produit sur l’ancien serveur (voir [§ 9](#9-dump-et-restauration-de-la-base)) :

```bash
sudo -u postgres psql -d remedy < /chemin/vers/remedy_dump_YYYYMMDD.sql
# Ou avec l'utilisateur applicatif (après création de la DB vide) :
psql -h 127.0.0.1 -U remedy_user -d remedy < remedy_dump_YYYYMMDD.sql
```

---

## 4. Application Django

### 4.1 Cloner le dépôt

```bash
cd /var/www/remedy
sudo -u remedy git clone https://github.com/scorpiomac/remedy_django.git .
```

### 4.2 Environnement virtuel et dépendances

```bash
cd /var/www/remedy
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn  # pour servir l’app derrière Nginx
```

### 4.3 Fichier d’environnement (production)

Ne jamais committer `.env` (il est dans `.gitignore`).

```bash
cp .env.example .env
chmod 600 .env
```

Éditez `.env` avec des valeurs **production** :

```ini
# Générer une clé : python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
REMEDY_SECRET_KEY=votre-clé-secrète-longue-et-aléatoire
REMEDY_DEBUG=0
REMEDY_ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com,IP_DU_VPS

REMEDY_DB_NAME=remedy
REMEDY_DB_USER=remedy_user
REMEDY_DB_PASSWORD=le_même_mot_de_passe_que_postgres
REMEDY_DB_HOST=127.0.0.1
REMEDY_DB_PORT=5432
```

### 4.4 Migrations et static

```bash
source .venv/bin/activate
export $(grep -v '^#' .env | xargs)
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py check
```

### 4.5 Droits sur dossiers sensibles

```bash
chmod 700 .env
mkdir -p logs media staticfiles
chown -R remedy:remedy /var/www/remedy
```

---

## 5. Serveur web et WSGI

Deux options : **Gunicorn + Nginx** (très courant) ou **LiteSpeed** (comme en dev).

### Option A : Gunicorn + Nginx

**Fichier systemd pour Gunicorn** (`/etc/systemd/system/remedy.service`) :

```ini
[Unit]
Description=REMEDY Gunicorn
After=network.target postgresql.service

[Service]
User=remedy
Group=remedy
WorkingDirectory=/var/www/remedy
EnvironmentFile=/var/www/remedy/.env
ExecStart=/var/www/remedy/.venv/bin/gunicorn \
    --workers 3 \
    --bind 127.0.0.1:8000 \
    --timeout 120 \
    --access-logfile /var/www/remedy/logs/gunicorn_access.log \
    --error-logfile /var/www/remedy/logs/gunicorn_error.log \
    config.wsgi:application
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable remedy
sudo systemctl start remedy
sudo systemctl status remedy
```

**Nginx** (ex. `/etc/nginx/sites-available/remedy`) :

```nginx
server {
    listen 80;
    server_name votre-domaine.com www.votre-domaine.com;
    client_max_body_size 50M;

    location /static/ {
        alias /var/www/remedy/staticfiles/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
    location /media/ {
        alias /var/www/remedy/media/;
        expires 7d;
    }
    location /.well-known/acme-challenge/ {
        root /var/www/remedy;
        allow all;
    }
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_read_timeout 120s;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/remedy /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

### Option B : LiteSpeed (LSWS)

Si vous installez OpenLiteSpeed / LiteSpeed, configurez un contexte **appserver** pointant vers le répertoire du projet, `config/wsgi.py` et le binaire Python du `.venv` (comme sur votre vhost actuel). Les principes (static/media, env, workers) restent les mêmes.

---

## 6. SSL / HTTPS

Recommandé : **Certbot** (Let’s Encrypt).

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d votre-domaine.com -d www.votre-domaine.com
```

Renouvellement automatique :

```bash
sudo certbot renew --dry-run
```

En production, activez les réglages Django pour HTTPS (voir [§ 7](#7-sécurité)).

---

## 7. Sécurité

### 7.1 Variables d’environnement

| Variable              | Production |
|-----------------------|------------|
| `REMEDY_DEBUG`        | `0`        |
| `REMEDY_SECRET_KEY`   | Clé longue aléatoire, unique par environnement |
| `REMEDY_ALLOWED_HOSTS`| Domaine(s) et IP du VPS uniquement |

### 7.2 Django (déjà dans `settings.py`)

- `DEBUG = False` via `REMEDY_DEBUG=0`
- `SESSION_COOKIE_HTTPONLY = True`
- `CSRF_COOKIE_HTTPONLY = True`
- `SECURE_CONTENT_TYPE_NOSNIFF = True`
- `X_FRAME_OPTIONS = "DENY"`

À activer **une fois HTTPS en place** (dans `config/settings.py` ou via variables d’env) :

```python
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### 7.3 Fichiers sensibles

- `.env` : `chmod 600`, propriétaire = utilisateur qui lance l’app
- Ne jamais exposer `.env`, `db.sqlite3`, `logs/` ou `.venv` via le serveur web

### 7.4 Base de données

- Utilisateur PostgreSQL dédié, mot de passe fort
- Écoute uniquement sur `127.0.0.1` (pas d’exposition publique du port 5432)

---

## 8. Performance

### 8.1 Static / media

- Nginx (ou équivalent) sert `/static/` et `/media/` directement (pas via Django).
- Headers `Cache-Control` et `expires` comme dans l’exemple Nginx (§ 5).
- `python manage.py collectstatic` à chaque déploiement.

### 8.2 Gunicorn

- `--workers 3` (ou `2 * CPU + 1`) selon la RAM.
- `--timeout 120` adapté aux requêtes longues (uploads, exports).
- Pour plus de charge : `--worker-class gthread` ou `gevent` (avec dépendance adaptée).

### 8.3 Base de données

- Index déjà présents sur les modèles (clés, FKs). Vérifier les requêtes lentes avec `django-debug-toolbar` en dev puis optimiser si besoin.
- Connexions : par défaut Django gère le pooling par worker ; pour un pool dédié, envisager `django-db-connection-pool` ou PgBouncer si beaucoup de workers.

### 8.4 Logs

- Fichiers de log (Django, Gunicorn) en dehors de `STATIC_ROOT` / `MEDIA_ROOT`.
- Rotation : logrotate ou paramètres Nginx/LiteSpeed (taille / durée).

---

## 9. Dump et restauration de la base

### 9.1 Créer un dump (sur la machine source)

Sur le serveur où tourne la base REMEDY (ou en local avec accès à la DB) :

```bash
cd /var/www/remedy_django   # ou chemin du projet
./scripts/dump_db.sh
```

Le script lit les variables `REMEDY_DB_*` (depuis `.env` ou l’environnement) et écrit un fichier du type `deploy/remedy_dump_YYYYMMDD_HHMM.sql`.

Transférez ce fichier sur le VPS (scp, rsync, etc.) :

```bash
scp deploy/remedy_dump_*.sql remedy@IP_VPS:/var/www/remedy/deploy/
```

### 9.2 Restaurer sur le VPS

1. Créer la base et l’utilisateur PostgreSQL (voir [§ 3.2](#32-création-base-et-utilisateur)).
2. Restaurer le dump :

```bash
sudo -u postgres psql -d remedy -f /var/www/remedy/deploy/remedy_dump_YYYYMMDD_HHMM.sql
```

Ou avec l’utilisateur applicatif (après création de la base vide) :

```bash
psql -h 127.0.0.1 -U remedy_user -d remedy -f deploy/remedy_dump_YYYYMMDD_HHMM.sql
```

3. Lancer les migrations si le dump est d’un schéma plus ancien : `python manage.py migrate --noinput`.

---

## 10. Checklist finale

- [ ] `REMEDY_DEBUG=0` et `REMEDY_SECRET_KEY` forte
- [ ] `REMEDY_ALLOWED_HOSTS` = domaine(s) + IP du VPS
- [ ] PostgreSQL créé, mot de passe fort, écoute locale
- [ ] Dump restauré (si applicable)
- [ ] `migrate` et `collectstatic` exécutés
- [ ] Gunicorn (ou LiteSpeed) activé et relancé après déploiement
- [ ] Nginx (ou équivalent) configuré pour static/media et proxy vers l’app
- [ ] SSL en place et redirection HTTP → HTTPS
- [ ] Cookies sécurisés et HSTS activés (après SSL)
- [ ] Pare-feu (ufw) : 22, 80, 443 uniquement
- [ ] Logs et rotation configurés

---

## Commandes utiles après déploiement

```bash
# Logs Gunicorn
sudo journalctl -u remedy -f

# Redémarrer l’app
sudo systemctl restart remedy

# Mise à jour du code
cd /var/www/remedy && sudo -u remedy git pull && source .venv/bin/activate && pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput && sudo systemctl restart remedy
```

---

*Document maintenu avec le projet REMEDY (Django).*
