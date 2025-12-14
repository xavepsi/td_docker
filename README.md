# TD – Application conteneurisée

## Présentation

Ce projet consiste à déployer une application web simple à l’aide de Docker et Docker Compose.
L’objectif est de montrer la mise en place d’une architecture conteneurisée complète avec un frontend, une API et une base de données.

## Architecture

L’application est composée de trois services :

Frontend (Nginx) : affiche l’interface web
API (FastAPI – Python) : fournit les données
Base de données (PostgreSQL) : stocke les informations

Le frontend appelle l’API, qui communique avec la base de données.

## Fonctionnement

L’API expose deux routes :
/status : vérifie que l’API fonctionne
/items : récupère les données depuis PostgreSQL

Le frontend interroge l’API en JavaScript pour afficher les données

La base de données est initialisée automatiquement au premier lancement

## Docker et organisation

Un Dockerfile pour l’API

Un Dockerfile pour le frontend

Un fichier docker-compose.yml pour lancer tous les services

Les variables de configuration sont externalisées dans un fichier .env

Les données sont persistantes grâce à un volume Docker

## Bonnes pratiques appliquées

Builds Docker multi-étapes pour réduire la taille des images

Conteneurs exécutés avec un utilisateur non-root

Healthchecks pour vérifier chaque service

## Commandes utiles :

docker compose ps
docker compose logs -f
docker compose down

## Résultat

Frontend accessible via le navigateur
API fonctionnelle
Connexion à la base de données opérationnell
Déploiement automatisé avec Docker Compose

## Conclusion

Ce projet démontre la mise en place d’une application web conteneurisée fonctionnelle

