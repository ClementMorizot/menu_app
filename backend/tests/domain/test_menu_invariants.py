from tests.objets_test import blocs, creneaux
from domain.menu import Menu
from typing import Dict
import pytest

class TestMenuStabilite: 

    def test_menu_vide_est_stable(self):
        # Arrange
        menu = Menu()

        # Assert
        assert menu.est_stable() is True

    def test_menu_valide_est_stable(self):
        # Arrange
        liste_creneaux = [creneaux.lundi_midi(), creneaux.lundi_soir(), creneaux.mardi_midi]
        bloc_1 = blocs.bloc_longueur_1()
        bloc_2 = blocs.bloc_longueur_2()
        menu = Menu()

        # Act 
        menu.ajouter_bloc(liste_creneaux[0],bloc_1)
        menu.ajouter_bloc(liste_creneaux[1],bloc_2)
        menu.ajouter_bloc(liste_creneaux[2],bloc_2)

        # Assert
        # 1. le menu est stable :
        #    - nombre total de créneaux cohérent
        #    - chaque bloc apparaît exactement autant de fois que sa longueur
        assert menu.est_stable() is True

        # 2. utilise tous les créneaux attendus sont bien planifiés
        assert all(menu.est_planifie(creneau) is True for creneau in liste_creneaux)

    def test_menu_avec_bloc_incomplet_n_est_pas_stable(self):
        # Arrange
        liste_creneaux = [creneaux.lundi_midi(), creneaux.lundi_soir(), creneaux.mardi_midi()]
        bloc_1 = blocs.bloc_longueur_1()
        bloc_2 = blocs.bloc_longueur_2()
        menu = Menu()

        # Act 
        menu.ajouter_bloc(liste_creneaux[0],bloc_1)
        menu.ajouter_bloc(liste_creneaux[1],bloc_2)

        # Assert
        assert menu.est_stable() is False

    def test_menu_avec_bloc_present_plus_qu_attendu(self):
        # Arrange
        liste_creneaux = [creneaux.lundi_midi(), creneaux.lundi_soir()]
        bloc_1 = blocs.bloc_longueur_1()
        menu = Menu()

        # Act 
        menu.ajouter_bloc(liste_creneaux[0],bloc_1)
        menu.ajouter_bloc(liste_creneaux[1],bloc_1)

        # Assert
        assert menu.est_stable() is False

class TestMenuCompletude :

    def test_menu_avec_creneau_manquant_n_est_pas_complet(self):
        # Arrange
        liste_creneaux = [creneaux.lundi_midi(), creneaux.lundi_soir(), creneaux.mardi_midi(), creneaux.mercredi_midi()]
        bloc_1 = blocs.bloc_longueur_1()
        bloc_2 = blocs.bloc_longueur_2()
        menu = Menu()

        # Act 
        menu.ajouter_bloc(liste_creneaux[0],bloc_1)
        menu.ajouter_bloc(liste_creneaux[1],bloc_2)
        menu.ajouter_bloc(liste_creneaux[2],bloc_2)

        # Assert
        assert menu.est_complet(len(liste_creneaux)) is False

class TestMenuProtectionAjout :

    def test_ajouter_bloc_sur_creneau_deja_occupe_leve_une_erreur(self):
        # Arrange
        liste_creneaux = [creneaux.lundi_midi()]
        bloc_1 = blocs.bloc_longueur_1()
        bloc_2 = blocs.bloc_longueur_2()
        menu = Menu()

        # Act 
        menu.ajouter_bloc(liste_creneaux[0],bloc_1)

        # Assert
        with pytest.raises(ValueError):
            menu.ajouter_bloc(liste_creneaux[0],bloc_2)
        
