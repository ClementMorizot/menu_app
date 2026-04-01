MENU APP (nom non définitif)

Générateur de menus hebdomadaires basé sur les recettes personnelles de l'utilisateur.

Note:

The current version of the project uses a mix of French and English naming.
A full transition to English naming conventions is planned for the next version to improve readability and accessibility.

1. OBJECTIF DU PROJET

Le projet présente un but double : démontrer l'application de multiples technologies et langages en interfaces et répondre à un besoin d'usage. Dans l'objectif de facilité la prise de décision sur les repas de la semaine et la liste des courses associées, cette application utilise les recettes propres de l'utilisateur pour planifier le menu de la semaine. 
Elle prend en compte : les recettes couvrant plusieurs repas, le besoin de changer une ou plusieurs recettes du menu (absent en v0.1 mais prévu pour la v1). D'autres améliorations sont en attente d'implémentation car l'application a été conçue pour être évolutive. 

2. FONCTIONNALITES ACTUELLES

- gestion des recettes via une base de données PostgreSQL
- génération d'un menu hebdomadaire
- planification sur 14 créneaux ordonnés (dimanche midi à samedi soir)
- support de recettes multi-repas
- execution via main.py
- output dans le terminal

3. Architecture du projet

Architecture en couches inspirée du DDD : 
- Domain Layer : contient toute la logique métier.
    - Aggregate Root : Menu
    - Domain Services : MenuGenerator, MenuPlanner et MenuEditor
    - Value Objects : Bloc, Creneau, Recette (jusqu'à la V1 seulement)
- Application Layer : ne contient aucune logique métier. Elle sert de chef d'orchestre pour assembler tous les Value Object du domain grace aux Domain Services. 
- Infrastruture Layer : ne contient aucune logique métier. Elle fait le lien entre le Domain Layer et la base de données PostgreSQL. 

Base de données :
- Recettes stockées en tables
- Fichier Seed permettant d'utiliser le moteur 

5. Structure du dépôt

backend/ contient les couches domain, application et infrastructure
database/ contient les fichiers permettant de créer la base de données et la seed
frontend/ contiendra l'interface utilisateur (placeholder)
docs/ contient la documentation technique du projet

6. Installation et exécution

Prérequis : 
python3
- dont module pytest
- dont module psycopg
tous les fichiers du projet dans son arborescence
postgreSQL

Installation :
PostgreSQL actif sur la session utilisateur
utilisateur a accès à PostgreSQL avec le droit de création et modification d'une base de données
créer une nouvelle base : psql -c "CREATE DATABASE menu_app_dev;"
vérifier que client_encoding et server_encoding en UTF8 (important)

Initialisation de la base: 
\i [chemin d'accès]/database/schema.sql
\i [chemin d'accès]/database/seed.sql

Lancement
python backend/main.py

Tests
Actuellement :
- 48 tests unitaires -> pytest -v
- 1 test de connexion à la base de données -> python backend/tests/infrastructure/test_db_connection.py
    - ce test valide la connexion à la base

7. Etat actuel du projet

Les différentes couches du moteur de génération de menus sont validés en exécution end-to-end. 
Le point d'entrée actuel est via console.
La sortie actuelle est via console.

La v0.1 représente une maquette fonctionnelle du projet. Elle présente les forces du moteur de génération ainsi que sa capacité d'évolution à travers sa structure stable et saine suivant la logique DDD. 
Certains compromis V1 seront par la suite abandonner au profit de fonctionnalités plus rigoureuses, par exemple :
- les recettes sont un Value Object en V1, et deviendront une entité 
- les erreurs remontent mais sont lissées en 2 grandes catégories : métier et technique
- il n'y a pas encore de gestion des préférences utilisateur (saison par exemple)

8. Evolutions prévues

En v1 et au delà, le projet prévoit déjà les fonctionnalités ci-dessous. D'autres pourront être implémentées en plus :
- interface utilisateur
- gestion complète des recettes
- génération de la liste de course
- saisonnalité
- préférence utilisateur
- heuristiques de planification plus avancées

9. Choix techniques et apprentissage

Ce projet m'a permi de travailler et développer :
- architecture en couche
- séparation des règles métiers et orchestration
- séparation des responsabilités
- modélisation des contraintes et des invariants
- création et implémentation d'une stratégie de tests
- préparation d'un environnement de développement
- intégration dans PostgreSQL
