Ce document est un document de travail servant de reference projet.
Il conserve l’etat du code, les decisions architecturales validees et les verites temporaires de la version en cours.
Il n’a pas vocation, en l’etat, a remplacer une documentation technique formelle.

1. OBJECTIF DU PROJET

Concevoir une application de generation de menus hebdomadaires basee exclusivement sur les recettes personnelles de l'utilisateur.

Fonctionnalites visees :

Generation automatique d'un menu pour une semaine (dejeuners + diners)
Gestion des recettes (ajout / modification / suppression)
Prise en compte des recettes couvrant plusieurs repas
Possibilite de reroll un repas
Generation future d'une liste de courses
Saison optionnelle

2. ARCHITECTURE GENERALE

Architecture en couches inspiree du DDD.

2.1 APPLICATION LAYER

orchestrator.py
creneauxgenerator.py

2.2 DOMAIN LAYER

menu.py
bloc.py
creneau.py
recette.py
generator.py
planner.py
editor.py
repositories.py

2.3 INFRASTRUCTURE LAYER

db_connection.py
sql_recipe_repository.py

2.4. ENTRY POINT

main.py

3. MODELE DOMAINE

3.1 Recette (Object Value jusqu'en V1, Entity par la suite)

Concept :

Recette persistable
Identifiee par UUID
Definit le nombre de repas couverts

Signature :

class Recette:
id: UUID
nom: str
description : str
temps_preparation : int
nombre_repas: int

3.2 Bloc (Value Object)

Concept :

Snapshot immuable d'une Recette
Couvre plusieurs creneaux
Longueur = nombre de repas couverts

V1 : snapshot simple (reference directe a Recette)

Signature :

class Bloc:
recette_snapshot: Recette
longueur: int

3.2.1 Règle V1 : pas de doublon de recette dans un Menu

En V1, un Menu ne peut contenir qu’un seul bloc par recette (via égalité de bloc).

Conséquences :

Le MenuGenerator ne génère jamais deux blocs issus de la même recette.
Le MenuEditor interdit un reroll vers une recette déjà présente dans le menu.

Cette règle simplifie fortement la génération et l’édition du menu en V1.
Elle pourra être assouplie dans des versions futures.

3.3 Creneau (Value Object)

Concept :

Repas planifiable
Defini par jour + moment

Signature :

class Creneau:
jour: str
moment: str

Note V1 :

Les valeurs de "jour" et "moment" ne sont pas validées au niveau du Domain.
Des valeurs sémantiquement invalides peuvent être instanciées.

La validation de ces champs est volontairement déléguée à la couche Application / UI.

4. AGREGAT ROOT : MENU

Concept :

Maintient un mapping Dict[Creneau, Bloc]
Empêche la collision de creneaux
Garantit la coherence interne

4.1 Invariants valides

Un Menu est stable si :

Le nombre total de creneaux planifies est egal au nombre total de repas declares par les blocs
Chaque bloc est present exactement bloc.longueur fois
Aucun creneau n'est planifie deux fois

Definition actuelle :

def est_stable(self) -> bool

La stabilité du Menu est indépendante de sa complétude. Un Menu peut être stable mais incomplet vis-à-vis d’un nombre de créneaux attendu.

4.2 Methodes actuelles (signatures)

class Menu:

def ajouter_bloc(self, creneau: Creneau, bloc: Bloc) -> None
def remplacer_bloc(self, creneau: Creneau, nouveau_bloc: Bloc) -> None
def supprimer_bloc(self, creneau: Creneau) -> None
def est_planifie(self, creneau: Creneau) -> bool
def obtenir_bloc(self, creneau: Creneau) -> Bloc
def contient_bloc(self, bloc: Bloc) -> bool
def creneaux_du_bloc(self, bloc: Bloc) -> list[Creneau]
def creneaux_planifies(self) -> list[Creneau]
def blocs_uniques(self) -> list[Bloc]
def nombre_total_repas(self) -> int
def verifier_coherence_longueur(self) -> bool
def est_complet(self, nombre_creneaux_attendus: int) -> bool
def est_stable(self) -> bool

5. DOMAIN SERVICEs 

5.1 MENUGENERATOR

Concept :

Produit des blocs
Ne connait pas les creneaux
Ne construit pas de Menu
Pur vis-a-vis de la planification

Dependance :

MenuGenerator depend d'un RecipeRepository pour acceder aux recettes disponibles.

Contraintes validees :

La somme des longueurs des blocs doit egaler le nombre de repas demande
Pas de doublon de recette en V1
Echec clair si generation impossible

Signatures actuelles :

class MenuGenerator:

def __init__(self, recipe_repository: RecipeRepository)
def creer_bloc(self, recette: Recette) -> Bloc
def creer_liste_blocs(self, nombre_repas: int) -> list
def creer_bloc_pour_reroll(self, longueur_bloc : int, recettes_exclues: list[Recette]) -> Bloc

5.2 MENUPLANNER

Concept :

Prend une liste de creneaux ordonnes
Prend une liste de blocs
Construit un Menu stable

Regles V1 :

sum(bloc.longueur) == len(creneaux)
Placement sequentiel pur
Aucune regle metier implicite
Verification finale via menu.est_stable()

Signature actuelle :

class MenuPlanner:

def planifier(self, creneaux: list[Creneau], blocs: list[Bloc]) -> Menu

5.3 MENUEDITOR

Concept :

Permet de modifier un Menu existant tout en respectant les invariants du domaine.

Le MenuEditor est responsable des operations d’edition sur un Menu.
Le MenuEditor n’introduit pas de nouvelle logique métier, il orchestre des opérations atomiques du Menu en respectant ses invariants.

Responsabilite V1 :

Implementer l’operation de reroll d’un bloc.

Definition du reroll V1 :

Un reroll :

Identifie le bloc actuellement planifie sur le creneau cible

Recupere tous les creneaux occupes par ce bloc

Supprime toutes les occurrences de ce bloc dans le menu

Insere un nouveau bloc sur exactement les memes creneaux

Verifie la stabilite finale du menu

Le reroll V1 est donc un remplacement "in-place".

Contraintes metier V1 :

Le creneau cible doit etre planifie
Le nouveau bloc doit avoir une longueur >= 1
Le nouveau bloc doit avoir la meme longueur que le bloc remplace
Le nouveau bloc ne doit pas deja etre present dans le menu
Le nouveau bloc doit referencer une recette differente de celle du bloc remplace
Le menu doit rester stable apres l’operation

Signature actuelle :

class MenuEditor:

def reroll(self, menu: Menu, creneau_cible: Creneau, nouveau_bloc: Bloc) -> None

6. DOMAIN PORT : RECIPEREPOSITORY

Concept :

Interface du domaine permettant l’accès aux recettes persistées.

Le repository est défini sous forme de Protocol afin de découpler complètement le domaine de l’infrastructure.

Le domaine ne connait pas le mode de stockage des recettes (SQL, API, mémoire, etc.).

Signature actuelle :

class RecipeRepository(Protocol):

def list_recipes(self) -> list[Recette]
def find_by_id(self, recette_id: UUID) -> Recette | None
def add_recipe(self, recette: Recette) -> None
def update_recipe(self, recette: Recette) -> None
def delete_recipe(self, recette_id: UUID) -> None

7. APPLICATION LAYER

Le Application Layer est implémenté en version V1 à travers un service principal : MenuOrchestrator.

Responsabilités :

Orchestrer les cas d’usage liés au Menu : génération d’un menu complet, reroll d’un créneau
Construire les données applicatives nécessaires (créneaux V1)
Appeler les services du domaine dans le bon ordre
Intercepter les erreurs du domaine et les traduire en messages exploitables par l’UI
Ne contenir aucune logique métier

Dépendances :

Le MenuOrchestrator reçoit ses dépendances par injection :

MenuGenerator
MenuPlanner
MenuEditor
CreneauxGenerator (service applicatif)

7.1 CreneauxGenerator (Application Service)

Responsabilité :

Produire une liste ordonnée de créneaux correspondant au besoin applicatif V1.

Contraintes V1 :

Nombre de repas compris entre 1 et 14
Ordre fixe :
dimanche midi → samedi soir
Aucune validation métier (déléguée au Domain)

Signature :

class CreneauxGenerator:
    def generer_liste_creneaux(self, nombre_repas: int) -> list[Creneau]

7.2 MenuOrchestrator (Application Service)

Responsabilité :
Coordonner les services du domaine pour exécuter les cas d’usage applicatifs.

Cas d’usage V1 :
Génération d’un menu (generer_menu)
Reroll d’un créneau (reroll_creneau)

Génération de menu

Flux :
Génération de 14 créneaux via CreneauxGenerator
Génération des blocs via MenuGenerator
Planification via MenuPlanner
Retour d’un résultat applicatif

Reroll de créneau

Flux :
Identification du bloc cible via Menu
Extraction de la longueur du bloc
Construction de la liste des recettes exclues (via blocs du menu)
Génération d’un nouveau bloc compatible via MenuGenerator
Application du reroll via MenuEditor
Retour du résultat applicatif

Contrat de sortie (commun aux use cases)

class MenuOrchestratorResult:
    succes: bool
    menu: Menu | None
    message: str

Comportement V1 :

Succès :
succes = True
menu modifié ou généré
message explicite

Échec métier :
succes = False
menu inchangé
message utilisateur explicite

Échec technique :
succes = False
menu inchangé
message générique

Messages V1 standardisés:
Génération :
succès : "Menu créé avec succès"
échec métier : "Impossible de générer un menu avec les recettes disponibles."
échec technique : "Une erreur technique est survenue lors de la génération du menu."

Reroll :
succès : "Repas remplacé avec succès"
échec métier : "Impossible de remplacer ce repas avec les recettes disponibles."
échec technique : "Une erreur technique est survenue lors du remplacement du repas."

Décision importante

L’orchestrator ne contient aucune logique métier : il ne sélectionne pas les recettes, il ne manipule pas directement le planning du menu.
il délègue entièrement : la génération au MenuGenerator, la modification au MenuEditor

8. INFRASTRUCTURE MAYER

8.1 db_connection.py

Responsabilité :

Fournir une connexion PostgreSQL aux composants d’infrastructure.

Rôle :

Isoler la logique technique de connexion à la base
Permettre aux repositories SQL de se concentrer sur la traduction entre SQL et objets métier

8.2 SqlRecipeRepository

Responsabilité :

Implémenter le port RecipeRepository pour la persistance SQL des recettes.

Rôle :

Traduire les demandes du domaine en requêtes SQL
Traduire les résultats SQL en objets métier Recette

Méthodes implémentées :

list_recipes()
find_by_id()
add_recipe()
update_recipe()
delete_recipe()

Principe architectural :

L’infrastructure dépend du domaine.
Le domaine ne dépend jamais de l’infrastructure.

9. ETAT ACTUEL

9.1 Etat actuel

Le domaine est complètement implémenté en version V1.
L'application est complètement implémentée en version V1 (génération de menu et reroll de créneau).
L'infrastructure SQL de base pour les recettes est implémentée.
main.py est codé et permet une exécution console fonctionnelle de la version 0.1.

Composants implémentés :

Recette
Bloc
Creneau
Menu
MenuGenerator
MenuPlanner
MenuEditor
RecipeRepository (Protocol)
CreneauxGenerator
MenuOrchestrator
db_connection.py
SqlRecipeRepository
main.py

10. Decisions architecturales

Decision 1 (implementee)

Le reroll ne fait pas partie de Menu.
Le reroll est implemente dans un Domain Service dedie : MenuEditor.

Decision 2 (implementee)

La planification appartient exclusivement a MenuPlanner.

Decision 3 (implementee)

Role final de Menu :

Stockage du planning
Garantie des invariants
Aucune logique d'agencement

11. VERITES TEMPORAIRES CONSERVEES

11.1 MenuPlanner V1 minimal

Une seule strategie
Placement sequentiel uniquement

11.2 MenuGenerator non deterministe

Utilise random.choice
RNG non injecte
max_essais = 5000 (valeur arbitraire)

11.3 Saison non implemente

Aucun champ saison dans Recette
Aucun filtrage saisonnier

11.4 Stabilite des recettes pendant la vie d’un Menu (V1)

Hypothese V1 :

Les recettes ne changent pas entre la generation d’un menu et les operations de reroll.

Consequence :

Les recettes sont considerees comme non modifiables tant qu’un menu actif existe.

Cette contrainte est appliquee au niveau Application Layer et non au niveau Domain.

Objectif :

Eviter les incoherences entre les snapshots de recette contenus dans les objets Bloc et les recettes stockees dans la base.

11.5 Validation des creneaux en V1

Le Domain n’impose pas de validation stricte sur les valeurs de Creneau (jour, moment).

Des creneaux sémantiquement invalides peuvent être instanciés.

La validation est volontairement deleguee a la couche Application / UI.

Objectif :

Permettre un Domain simple et testable sans contrainte d’interface en V1.

11.6 Mutation du Menu dans les use cases applicatifs

Les opérations de type reroll modifient le Menu "in-place".

Conséquences :

Le Menu est un objet mutable partagé entre le Domain et l’Application Layer
Le MenuOrchestrator retourne le même objet Menu modifié
En cas d’échec, le Menu est garanti inchangé

Cette décision simplifie la V1 mais peut évoluer vers une approche immuable dans les versions futures.

12. MENTIONS BREVES

Exclusions utilisateur : valide mais non implemente
Strategies multiples futures : evolution prevue
Snapshot Bloc : reference directe a Recette (pas de versioning)

13. PRINCIPES STRUCTURANTS

Separation stricte Domain / Application / Infrastructure
Domain deterministe et testable isole
MenuGenerator != MenuPlanner
Menu = garant des invariants uniquement
MenuEditor = responsable des operations de modification du Menu
Aucune regle metier implicite non validee

14 TESTS

14.1 Objets de test

Tous les objets de tests ont été créés :

- recettes
- blocs
- creneaux
- menus

14.2 FakeRecipeRepository

Le fake a été créé pour permettre les tests. Il suit les protocoles établis par le Repository du domaine.

10.3 Tests Domain Layer

Tous les tests ont été écrits et sont prêts à être exploités:

- menus : test des invariants, de la complétude et de la protection face aux ajouts
- generator : tests des méthodes creer_bloc() et creer_liste_blocs() dans des conditions optimales, limites et hostiles
- planner : tests de la planification dans des conditions optimales, limites et hostiles. Validation de la stabilité du Menu post-opération. 
- editor : tests du reroll dans des conditions optimales, limites et hostiles. Validation de continuité de stabilité du Menu post-opération.

Note de vocabulaire:

- optimales : cas nominaux
- limites : cas frontières (longueur, somme, etc)
- hostiles : états incohérents ou corruption des données

14.4 Tests Application Layer

Des tests ont été ajoutés pour valider le comportement du MenuOrchestrator.

Couverture :

génération de menu :
cas nominal
repository insuffisant
validation du résultat applicatif
reroll de créneau :
cas nominal (bloc unitaire)
cas nominal (bloc multi-repas)
créneau non planifié
absence de recette compatible

Stratégie de test :

validation du résultat applicatif (MenuOrchestratorResult)
validation de la stabilité et complétude du menu
validation des effets du reroll sur tous les créneaux concernés
vérification de l’absence de mutation du menu en cas d’échec via comparaison de l’état observable (mapping creneau → bloc)

14.5 Tests Infrastructure Layer

Des tests ont été ajoutés pour valider :

la connexion à la base PostgreSQL
le fonctionnement du repository SQL des recettes
les opérations de lecture, ajout, modification et suppression
la traduction correcte entre données SQL et objets métier

14.6 Résultats

Les tests constituent la principale garantie de validité du domaine et de l'application et permettent leur évolution en toute sécurité.

15. RESULTATS DE TEST

15.1 Validation du domaine

L’ensemble des tests du domaine a été exécuté avec succès.

Après correction de certains tests ambigus liés à la comparaison d’objets métier, la suite de tests est stable.

Résultat :

100% des tests passent
les invariants métier sont respectés dans tous les scénarios testés :
cas nominaux
cas limites
cas hostiles

Conclusion :

Le domaine est validé en tant que boîte noire fiable pour le périmètre V1.

15.2 Validation de l’application

Des tests ont été implémentés pour valider le comportement du MenuOrchestrator, représentant la couche Application.

Les cas d’usage testés sont :

génération de menu :
cas nominal
échec dû à un repository insuffisant
reroll de créneau :
cas nominal (bloc unitaire)
cas nominal (bloc multi-repas)
créneau non planifié
absence de recette compatible avec les contraintes

Les tests vérifient :

le respect du contrat applicatif (MenuOrchestratorResult)
la stabilité et la complétude du Menu après opération
la bonne application du reroll sur l’ensemble des créneaux d’un bloc
l’absence de mutation du Menu en cas d’échec, via comparaison de son état observable

Conclusion :

La couche Application est validée dans le périmètre V1.
Elle orchestre correctement les services du domaine sans introduire de logique métier.

15.3 Validation de l’infrastructure

Des tests ont été exécutés pour valider la connexion à la base et le comportement du SqlRecipeRepository.

Les opérations testées couvrent :

lecture des recettes
recherche par identifiant
ajout
mise à jour
suppression

Conclusion :

L’infrastructure SQL des recettes est validée dans le périmètre V1 actuellement implémenté.

15.4 Validation du point d’entrée

Le fichier main.py a été codé pour assembler les dépendances de l’application et exécuter un cas d’usage complet de génération de menu.
Une exécution réelle a été réalisée avec succès.

Résultat observé :

L’application génère un menu exploitable et l’affiche correctement dans la console.

Conclusion :

La chaîne minimale complète de la version 0.1 est opérationnelle :
repository de recettes -> génération des blocs -> planification -> résultat applicatif -> affichage console

16 POINT D’ENTREE ET EXECUTION

16.1 main.py
Une fonction dédiée est utilisée pour l’affichage du menu en console. Elle parcourt les créneaux du menu et affiche la recette associée à chacun.

main() joue le rôle de point d’entrée technique de l’application.

Responsabilités :

Instancier les dépendances nécessaires (repository, services du domaine et services applicatifs)
Assembler ces dépendances
Déclencher l’exécution d’un cas d’usage via MenuOrchestrator
Afficher le résultat dans la console

main() ne contient aucune logique métier.

16.2 Validation V0.1
Le comportement de main() est cohérent avec le résultat attendu.

Deux cas sont observés :

Succès :
Un menu complet est généré et affiché dans le terminal

Échec :
Un message est affiché, différenciant les erreurs métier des erreurs techniques

Conclusion :

Le point d’entrée permet d’exécuter un cas d’usage complet de manière fiable dans le périmètre V0.1.

17. LIVRABLES PRODUITS

Diagramme UML de structure
Diagramme UML d’architecture
Diagramme UML de séquence
Documentation de travail (mémoire technique, notes techniques)
Architecture en couches implémentée (Domain / Application / Infrastructure)
Suite de tests du domaine, de l’application et de l’infrastructure
Point d’entrée exécutable main.py

18. PROCHAINES ETAPES

18.1. Objectifs pour la V1

Remplacement du point d’entrée console par une interface utilisateur (web ou locale)
Intégration complète des cas d’usage de gestion des recettes (ajout, modification, suppression)

18.2. Futures features

Gestion des exclusions utilisateur
Filtrage saisonnier des recettes
Gestion des utilisateurs
Déploiement de l'application en environnement web