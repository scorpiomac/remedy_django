# Dépôt des dumps et fichiers de déploiement

- **Dumps PostgreSQL** : après exécution de `./scripts/dump_db.sh` à la racine du projet, les fichiers `remedy_dump_YYYYMMDD_HHMM.sql` sont créés ici.
- Les dumps sont **versionnés dans Git** pour pouvoir les récupérer au clône lors du déploiement sur un VPS.
- Sur le VPS : après `git clone`, restaurez le dump (voir [docs/DEPLOYMENT.md](../docs/DEPLOYMENT.md) § 9).
- **Attention** : si le dump contient des données sensibles (production), privilégiez un dépôt privé ou un transfert sécurisé hors Git.
