from application.orchestrator import MenuOrchestrator
from application.creneauxgenerator import CreneauxGenerator
from domain.generator import MenuGenerator
from domain.planner import MenuPlanner
from domain.menu import Menu
from tests.fakes.fake_repository import FakeRecipeRepository
from tests.objets_test import recettes, creneaux

#imports pour tests future de la méthode reroll
from domain.editor import MenuEditor
from tests.objets_test import menus

def test_orchestrator_pour_cas_nominal():
    # Arrange
    liste_recette = [recettes.recette_1_repas(),
                     recettes.recette_1_repas_bis(),
                     recettes.recette_1_repas_ter(),
                     recettes.recette_1_repas_quater(),
                     recettes.recette_2_repas(),
                     recettes.recette_2_repas_bis(),
                     recettes.recette_3_repas(),
                     recettes.recette_3_repas_bis()

    ]
    repository = FakeRecipeRepository(liste_recette)
    blocgenerator = MenuGenerator(repository)
    menuplanner = MenuPlanner()
    menueditor = MenuEditor()
    creneauxgenerator = CreneauxGenerator()
    orchestrator = MenuOrchestrator(blocgenerator,menuplanner,menueditor,creneauxgenerator)

    # Act
    result = orchestrator.generer_menu()

    # Assert
    assert result.succes is True
    assert isinstance(result.menu,Menu)
    assert result.menu.est_stable() is True
    assert result.menu.est_complet(14) is True
    assert result.message == "Menu créé avec succès"

def test_orchestrator_pour_repository_insuffisant():
    # Arrange
    liste_recette = [recettes.recette_1_repas(),
                     recettes.recette_1_repas_bis(),
                     recettes.recette_1_repas_ter(),
                     recettes.recette_1_repas_quater(),
                     recettes.recette_2_repas(),

    ]
    repository = FakeRecipeRepository(liste_recette)
    blocgenerator = MenuGenerator(repository)
    menuplanner = MenuPlanner()
    menueditor = MenuEditor()
    creneauxgenerator = CreneauxGenerator()
    orchestrator = MenuOrchestrator(blocgenerator,menuplanner,menueditor,creneauxgenerator)

    # Act
    result = orchestrator.generer_menu()

    # Assert
    assert result.succes is False
    assert result.menu is None
    assert result.message == "Impossible de générer un menu avec les recettes disponibles"
    
def test_reroll_par_orchestrator_dans_un_cas_nominal_pour_recette_un_repas():
    # Arrange
    menu = menus.menu_pour_reroll()
    creneau_cible = creneaux.lundi_midi()
    liste_recettes = [recettes.recette_1_repas_ter()]
    repository = FakeRecipeRepository(liste_recettes)
    generator = MenuGenerator(repository)
    planner = MenuPlanner()
    editor = MenuEditor()
    creneauxgenerator = CreneauxGenerator()
    orchestrator = MenuOrchestrator(generator,planner,editor,creneauxgenerator)

    # Act
    resultat = orchestrator.reroll_creneau(menu, creneau_cible)

    # Assert
    assert menu.est_stable() is True
    assert menu.obtenir_bloc(creneau_cible).recette_snapshot == liste_recettes[0]
    assert resultat.succes is True
    assert isinstance(resultat.menu,Menu)
    assert resultat.message == "Repas remplacé avec succès"

def test_reroll_par_orchestrator_dans_un_cas_nominal_pour_recette_multi_repas():
    # Arrange
    menu = menus.menu_pour_reroll()
    creneau_cible = creneaux.mardi_midi()
    liste_creneaux_affectes = menu.creneaux_du_bloc(menu.obtenir_bloc(creneau_cible))
    liste_recettes = [recettes.recette_2_repas_bis()]
    repository = FakeRecipeRepository(liste_recettes)
    generator = MenuGenerator(repository)
    planner = MenuPlanner()
    editor = MenuEditor()
    creneauxgenerator = CreneauxGenerator()
    orchestrator = MenuOrchestrator(generator,planner,editor,creneauxgenerator)

    # Act
    resultat = orchestrator.reroll_creneau(menu, creneau_cible)

    # Assert
    assert menu.est_stable() is True
    assert all(menu.obtenir_bloc(creneau).recette_snapshot == liste_recettes[0] for creneau in  liste_creneaux_affectes)
    assert resultat.succes is True
    assert isinstance(resultat.menu,Menu)
    assert resultat.message == "Repas remplacé avec succès"

def test_reroll_par_orchestrator_cas_creneau_non_planifie():
    # Arrange
    menu = menus.menu_pour_reroll()
    creneaux_du_menu_initial = menu.creneaux_planifies()
    representation_menu_initial = dict()
    for creneau in creneaux_du_menu_initial :
        representation_menu_initial[creneau] = menu.obtenir_bloc(creneau)
    creneau_cible = creneaux.vendredi_midi()
    liste_recettes = [recettes.recette_1_repas_ter()]
    repository = FakeRecipeRepository(liste_recettes)
    generator = MenuGenerator(repository)
    planner = MenuPlanner()
    editor = MenuEditor()
    creneauxgenerator = CreneauxGenerator()
    orchestrator = MenuOrchestrator(generator,planner,editor,creneauxgenerator)

    # Act
    resultat = orchestrator.reroll_creneau(menu, creneau_cible)

    # Assert
    assert resultat.succes is False
    assert isinstance(resultat.menu,Menu)
    assert resultat.message == "Impossible de remplacer ce repas avec les recettes disponibles"
    assert menu.est_stable() is True
    assert menu.est_complet(len(creneaux_du_menu_initial)) is True

    # Verification que menu reste inchangé
    assert all(menu.obtenir_bloc(creneau) == representation_menu_initial[creneau] for creneau in menu.creneaux_planifies())
    

def test_reroll_par_orchestrator_cas_repository_insuffisant_pour_les_contraintes_du_reroll():
    # Arrange
    menu = menus.menu_pour_reroll()
    creneaux_du_menu_initial = menu.creneaux_planifies()
    representation_menu_initial = dict()
    for creneau in creneaux_du_menu_initial :
        representation_menu_initial[creneau] = menu.obtenir_bloc(creneau)
    creneau_cible = creneaux.lundi_midi()
    liste_recettes = [menu.obtenir_bloc(creneau_cible).recette_snapshot,recettes.recette_2_repas_bis()]
    repository = FakeRecipeRepository(liste_recettes)
    generator = MenuGenerator(repository)
    planner = MenuPlanner()
    editor = MenuEditor()
    creneauxgenerator = CreneauxGenerator()
    orchestrator = MenuOrchestrator(generator,planner,editor,creneauxgenerator)

    # Act
    resultat = orchestrator.reroll_creneau(menu, creneau_cible)

    # Assert
    assert resultat.succes is False
    assert isinstance(resultat.menu,Menu)
    assert resultat.message == "Impossible de remplacer ce repas avec les recettes disponibles"
    assert menu.est_stable() is True
    assert menu.est_complet(len(creneaux_du_menu_initial)) is True

    # Verification que menu reste inchangé
    assert all(menu.obtenir_bloc(creneau) == representation_menu_initial[creneau] for creneau in menu.creneaux_planifies())