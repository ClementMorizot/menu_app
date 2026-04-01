from tests.objets_test import menus, blocs, creneaux
from domain.editor import MenuEditor
import pytest

def test_reroll_remplace_toutes_les_occurrences_du_bloc_cible():
    # Arrange
    menu = menus.menu_deux_blocs_longueur_2()
    creneau_cible = creneaux.lundi_midi()
    nouveau_bloc = blocs.bloc_longueur_2_ter()
    bloc_spectateur = menu.obtenir_bloc(creneaux.mardi_midi())
    editor = MenuEditor()

    # Act
    editor.reroll(menu,creneau_cible,nouveau_bloc)

    # Assert
    assert menu.est_stable() is True
    assert menu.obtenir_bloc(creneaux.lundi_midi()) == nouveau_bloc
    assert menu.obtenir_bloc(creneaux.lundi_soir()) == nouveau_bloc
    assert menu.obtenir_bloc(creneaux.mardi_midi()) == bloc_spectateur
    assert menu.obtenir_bloc(creneaux.mardi_soir()) == bloc_spectateur

def test_reroll_leve_une_erreur_si_le_creneau_cible_n_est_pas_planifie():
    # Arrange
    menu = menus.menu_deux_blocs_longueur_2()
    creneau_cible = creneaux.vendredi_midi()
    nouveau_bloc = blocs.bloc_longueur_2_ter()
    editor = MenuEditor()

    # Act / Assess
    with pytest.raises(ValueError):
        editor.reroll(menu,creneau_cible,nouveau_bloc)

def test_reroll_leve_une_erreur_si_le_nouveau_bloc_est_de_longueur_inferieure_a_1():
    # Arrange
    menu = menus.menu_deux_blocs_longueur_2()
    creneau_cible = creneaux.lundi_midi()
    nouveau_bloc = blocs.bloc_longueur_nulle()
    editor = MenuEditor()

    # Act / Assess
    with pytest.raises(ValueError):
        editor.reroll(menu,creneau_cible,nouveau_bloc)

def test_reroll_leve_une_erreur_si_le_nouveau_bloc_est_le_bloc_demande_en_modification():
    # Arrange
    menu = menus.menu_deux_blocs_longueur_2()
    creneau_cible = creneaux.lundi_midi()
    ancien_bloc = menu.obtenir_bloc(creneau_cible)
    nouveau_bloc = ancien_bloc
    editor = MenuEditor()

    # Act / Assess
    with pytest.raises(ValueError):
        editor.reroll(menu,creneau_cible,nouveau_bloc)

def test_reroll_leve_une_erreur_si_le_nouveau_bloc_est_le_bloc_deja_dans_le_menu_sur_un_autre_creneau():
    # Arrange
    menu = menus.menu_pour_reroll()
    creneau_cible = creneaux.mardi_soir()
    nouveau_bloc = menu.obtenir_bloc(creneaux.lundi_midi())
    editor = MenuEditor()

    # Act / Assess
    with pytest.raises(ValueError):
        editor.reroll(menu,creneau_cible,nouveau_bloc)

def test_reroll_leve_une_erreur_si_ancien_et_nouveau_bloc_n_ont_pas_la_meme_longueur():
    # Arrange
    menu = menus.menu_deux_blocs_longueur_2()
    creneau_cible = creneaux.lundi_midi()
    nouveau_bloc = blocs.bloc_longueur_1()
    editor = MenuEditor()

    # Act / Assess
    with pytest.raises(ValueError):
        editor.reroll(menu,creneau_cible,nouveau_bloc)

def test_reroll_leve_une_erreur_si_le_bloc_cible_est_deja_incoherent_dans_le_menu():
    # Arrange
    menu = menus.menu_instable_bloc_incomplet()
    creneau_cible = creneaux.lundi_soir()
    nouveau_bloc = blocs.bloc_longueur_2_ter()
    editor = MenuEditor()

    # Act / Assess
    with pytest.raises(ValueError):
        editor.reroll(menu,creneau_cible,nouveau_bloc)