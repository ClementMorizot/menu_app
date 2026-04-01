from dataclasses import dataclass
from domain.menu import Menu
from domain.generator import MenuGenerator
from domain.planner import MenuPlanner
from domain.editor import MenuEditor
from domain.creneau import Creneau
from application.creneauxgenerator import CreneauxGenerator

@dataclass
class MenuOrchestratorResult:

    succes : bool
    menu : Menu | None
    message : str

class MenuOrchestrator:
    def __init__(
            self,
            menugenerator : MenuGenerator,
            menuplanner : MenuPlanner,
            menueditor : MenuEditor,
            creneauxgenerator : CreneauxGenerator
    ) -> None :
        self._menugenerator = menugenerator
        self._menuplanner = menuplanner
        self._menueditor = menueditor
        self._creneauxgenerator = creneauxgenerator

    def generer_menu(self) -> MenuOrchestratorResult:
        nombre_repas = 14

        try:

            liste_creneaux = self._creneauxgenerator.generer_liste_creneaux(nombre_repas)
            liste_blocs = self._menugenerator.creer_liste_blocs(nombre_repas)
            menu = self._menuplanner.planifier(liste_creneaux,liste_blocs)

            return MenuOrchestratorResult(
                succes = True,
                menu = menu,
                message= "Menu créé avec succès"
            )
        
        except ValueError :
            return MenuOrchestratorResult(
                succes  =False,
                menu = None,
                message = "Impossible de générer un menu avec les recettes disponibles"
            )
        
        except Exception:
            return MenuOrchestratorResult(
                succes = False,
                menu = None,
                message = "Une erreur technique est survenue lors de la génération du menu"
            )
        
    def reroll_creneau(
            self,
            menu : Menu,
            creneau_cible : Creneau,
    ) -> MenuOrchestratorResult :
        
        try:
            bloc_cible = menu.obtenir_bloc(creneau_cible)
            liste_exclusion_recette = [bloc.recette_snapshot for bloc in menu.blocs_uniques()]
            nouveau_bloc = self._menugenerator.creer_bloc_pour_reroll(bloc_cible.longueur,liste_exclusion_recette)
            self._menueditor.reroll(menu,creneau_cible,nouveau_bloc)

            return MenuOrchestratorResult(
                succes = True,
                menu = menu,
                message = "Repas remplacé avec succès"
            )
        
        except ValueError:

            return MenuOrchestratorResult(
                succes = False,
                menu = menu,
                message = "Impossible de remplacer ce repas avec les recettes disponibles"
            )
        
        except Exception:

            return MenuOrchestratorResult(
                succes = False,
                menu = menu,
                message = "Une erreur technique est survenue lors du remplacement du repas"
            )