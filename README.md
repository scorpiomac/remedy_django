# REMEDY V1 - Django (Security-First)

Ce dossier contient la nouvelle base REMEDY en Django pour une cible "grandes organisations", avec un socle securite standardise et un dashboard superadmin personnalise.

Stack front choisi pour V1: **Bootstrap** (rapidite d'execution).  
Si besoin on pourra migrer vers Tailwind plus tard sans toucher a la logique metier.

## Ce qui est deja en place

- Projet Django: `config`
- Apps metier: `accounts`, `claims`, `core`
- Auth Django (session + CSRF)
- Modele de donnees initial REMEDY:
  - `IPM`, `Patient`, `Category`, `CoverageRule`
  - `Claim`, `ClaimDocument`, `ClaimAuditLog`, `NotificationLog`
  - `StaffProfile` (role staff: System/IPM/Doctor/Pharmacy)
- Dashboard superadmin personnalise:
  - URL: `/superadmin/`
  - KPIs: IPMs, patients, claims, submitted, blocked, coverage rules
  - Tableau des derniers dossiers

## Lancer en local

```bash
cd /usr/local/lsws/Example/html/remedy_django
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python -m pip install psycopg[binary]
.venv/bin/python manage.py migrate
.venv/bin/python manage.py createsuperuser
.venv/bin/python manage.py runserver 0.0.0.0:8100
```

Ensuite:
- Login: `http://localhost:8100/accounts/login/`
- Dashboard superadmin: `http://localhost:8100/superadmin/`
- Django admin: `http://localhost:8100/admin/`

## Variables d'environnement

Copier `.env.example` dans votre gestionnaire d'env:
- `REMEDY_SECRET_KEY`
- `REMEDY_DEBUG`
- `REMEDY_ALLOWED_HOSTS`
- `REMEDY_DB_NAME`
- `REMEDY_DB_USER`
- `REMEDY_DB_PASSWORD`
- `REMEDY_DB_HOST`
- `REMEDY_DB_PORT`

Exemple de base PostgreSQL:

```sql
CREATE DATABASE remedy;
CREATE USER remedy_user WITH PASSWORD 'change-me';
GRANT ALL PRIVILEGES ON DATABASE remedy TO remedy_user;
```

## Suite du chantier (sans feature creep)

1. State machine stricte REMEDY (DRAFT -> ... -> BLOCKED terminal)
2. APIs REST minimales
3. UI provider claim submission
4. UI patient verification via token one-time
5. RBAC fin par role + scope IPM
