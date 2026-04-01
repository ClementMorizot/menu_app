from tests.objets_test import creneaux, blocs
from domain.menu import Menu
from domain.planner import MenuPlanner
import pytest

def test_planifier_retourne_un_menu_stable_et_complet_dans_le_cas_minimal():
    # Arrange
    liste_creneaux = [creneaux.lundi_midi()]
    liste_blocs = [blocs.bloc_longueur_1()]
    planner = MenuPlanner()

    # Act
    menu = planner.planifier(liste_creneaux,liste_blocs)

    # Assert
    assert menu.est_stable()
    assert menu.est_complet(len(liste_creneaux))
    assert menu.blocs_uniques() == liste_blocs
    assert menu.creneaux_planifies() == liste_creneaux
    assert isinstance(menu,Menu)

def test_planifier_place_les_blocs_sequentiellement():
    # Arrange
    bloc_1 = blocs.bloc_longueur_1()
    bloc_3 = blocs.bloc_longueur_3()
    liste_creneaux = [creneaux.lundi_midi(),creneaux.lundi_soir(),creneaux.mardi_midi(),creneaux.mardi_soir()]
    liste_blocs = [bloc_1,bloc_3]
    planner = MenuPlanner()

    # Act
    menu = planner.planifier(liste_creneaux,liste_blocs)

    # Assert
    assert menu.est_stable()
    assert menu.obtenir_bloc(liste_creneaux[0]) == bloc_1
    assert menu.obtenir_bloc(liste_creneaux[1]) == bloc_3
    assert menu.obtenir_bloc(liste_creneaux[2]) == bloc_3
    assert menu.obtenir_bloc(liste_creneaux[3]) == bloc_3

def test_planifier_leve_une_erreur_si_somme_longueur_blocs_inferieur_au_nombre_creneaux():
    # Arrange
    liste_creneaux = [creneaux.lundi_midi(), creneaux.lundi_soir()]
    liste_blocs = [blocs.bloc_longueur_1()]
    planner = MenuPlanner()

    # Act / Assert
    with pytest.raises(ValueError) :
        planner.planifier(liste_creneaux,liste_blocs)


def test_planifier_leve_une_erreur_si_somme_longueur_blocs_superieur_au_nombre_creneaux():
    # Arrange
    liste_creneaux = [creneaux.lundi_midi()]
    liste_blocs = [blocs.bloc_longueur_2()]
    planner = MenuPlanner()

    # Act / Assert
    with pytest.raises(ValueError):
        planner.planifier(liste_creneaux,liste_blocs)