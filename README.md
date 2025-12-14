# TD - Application conteneurisée générique

## Architecture

### Services
- **API** (FastAPI Python): Expose deux routes `/status` et `/items` pour interroger la base de données
- **Front** (Nginx): Serveur statique qui interroge l'API via JavaScript
- **Database** (PostgreSQL): Stocke les items

### Interactions
```
Frontend (Nginx) -> API (FastAPI) -> PostgreSQL
```

## Fichiers importants

- `api/main.py`: Application FastAPI
- `api/Dockerfile`: Build multi-étapes pour l'API
- `api/requirements.txt`: Dépendances Python
- `front/index.html`: Page HTML du front
- `front/app.js`: JavaScript pour charger les items
- `front/nginx.conf`: Configuration du reverse proxy
- `front/Dockerfile`: Build multi-étapes pour le front
- `db/init.sql`: Script d'initialisation de la base de données
- `docker-compose.yml`: Orchestration des 3 services
- `.env`: Variables d'environnement
- `.dockerignore`: Fichiers à exclure du build Docker

## Bonnes pratiques mises en œuvre

### Build multi-étapes
- **API**: Étape builder pour installer les deps, puis image finale minimaliste
- **Front**: Étape builder Node, puis image finale Nginx

### Sécurité
- Conteneurs exécutés avec utilisateur non-root (`appuser`)
- `security_opt: no-new-privileges:true` pour éviter les escalades de privilèges
- `cap_drop: ALL` pour retirer toutes les capacités Linux inutiles
- Images Alpine pour réduire la surface d'attaque

### Externalisation des variables
- Fichier `.env` pour les configurations (host, port, utilisateur, mot de passe)
- Variables référencées dans `docker-compose.yml`

### Healthchecks
- DB: `pg_isready` pour vérifier que PostgreSQL est prêt
- API: `curl /status` pour vérifier que l'API est accessible
- Front: `curl /` pour vérifier que Nginx répond
- Permet à Compose de savoir quand chaque service est prêt

### .dockerignore
Exclut les fichiers inutiles du build:
- `__pycache__/`, `*.pyc`: Fichiers Python compilés
- `node_modules/`: Dépendances Node
- `.git`: Historique Git
- `.env`: Fichiers de configuration sensibles

## Commandes clés

### Construction et déploiement
```bash
bash scripts/build_and_deploy.sh
```

### Vérifier les services
```bash
docker compose ps
docker compose logs -f
```

### Arrêter la stack
```bash
docker compose down
```

### Arrêter et supprimer les volumes
```bash
docker compose down -v
```

### Mesurer la taille des images
```bash
docker images td_api:latest --format "table {{.Repository}}\t{{.Size}}"
docker images td_front:latest --format "table {{.Repository}}\t{{.Size}}"
```

## Taille des images

Les builds multi-étapes permettent de réduire significativement la taille:

### API
- Étape builder: ~500MB (avec pip)
- Image finale: ~150MB (sans pip, sans compilateur)
- **Réduction: ~70%**

### Front
- Étape builder Node: ~400MB
- Image finale Nginx: ~40MB
- **Réduction: ~90%**

## Difficultés et améliorations possibles

### Difficultés rencontrées
1. Configuration du reverse proxy Nginx: Nécessite `proxy_pass http://api:8000/` (pas `http://api:8000` seul)
2. Initialisation de PostgreSQL: Les scripts dans `/docker-entrypoint-initdb.d/` ne s'exécutent que la première fois
3. Attendre que les services soient prêts: Healthchecks + `depends_on: condition: service_healthy`

### Améliorations possibles
1. **CI/CD**: Ajouter un pipeline GitHub Actions pour builder et tester automatiquement
2. **Scanning d'images**: Utiliser `docker scan` ou Trivy pour vérifier les vulnérabilités
3. **Signature des images**: Docker Content Trust pour signer et vérifier les images
4. **Logging centralisé**: ELK Stack ou Prometheus + Grafana
5. **Scaling**: Ajouter un load balancer (Nginx, HAProxy) pour plusieurs instances
6. **Secrets**: Utiliser Docker Secrets ou HashiCorp Vault au lieu du `.env`

## Évaluation

### Critères validés
-  Routes `/status` et `/items` fonctionnelles
-  Accès base de données opérationnel
-  Configuration `.env` et variables externalisées
-  Dockerfiles multi-étapes pour API et front
-  Utilisateur non-root dans les conteneurs
-  Initialisation automatique de la base
-  Persistance des données (volume)
-  Frontend fonctionnel interrogeant l'API
-  docker-compose.yml complet
-  Healthchecks configurés
-  Gestion des variables via Compose
-  Sécurité (non-root, no-new-privileges, cap_drop)
-  Script d'automatisation

### Points perfectibles
- Signature des images (Docker Content Trust)
- Scan automatique des vulnérabilités
- Tests unitaires dans le script CI
