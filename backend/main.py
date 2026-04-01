from application.orchestrator import MenuOrchestrator
from application.creneauxgenerator import CreneauxGenerator
from domain.generator import MenuGenerator
from domain.planner import MenuPlanner
from domain.editor import MenuEditor
from domain.menu import Menu
from infrastructure.db_connection import get_connection
from infrastructure.sql_recipe_repository import SqlRecipeRepository

def afficher_menu( menu: Menu) -> None:
    # Affichage en console pour tests de fonctionnement minimaliste
    creneaux = menu.creneaux_planifies()
    print("Menu généré: ")
    for creneau in creneaux:
        bloc = menu.obtenir_bloc(creneau)
        print(f"{creneau.jour} {creneau.moment} : {bloc.recette_snapshot.nom}")
    

def main() -> None:
    connexion = None

    try:
        connexion = get_connection()
        repository = SqlRecipeRepository(connexion)

        generator = MenuGenerator(repository)
        planner = MenuPlanner()
        editor = MenuEditor()
        creneaux_generator = CreneauxGenerator()

        orchestrator = MenuOrchestrator(
            generator,
            planner,
            editor,
            creneaux_generator
        )

        resultat = orchestrator.generer_menu()

        if not resultat.succes:
            print(resultat.message)
            return

        print(resultat.message)
        print()

        if resultat.menu is not None:
            afficher_menu(resultat.menu)

    except Exception as e:
        print(f"Erreur technique : {e}")

    finally:
        if connexion is not None:
            connexion.close()


if __name__ == "__main__":
    main()