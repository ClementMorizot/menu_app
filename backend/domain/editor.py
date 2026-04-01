from .bloc import Bloc
from .creneau import Creneau
from .menu import Menu

class MenuEditor:
    
    def __init__(self) -> None :
        pass

    def reroll(self, menu : Menu, creneau_cible : Creneau, nouveau_bloc : Bloc) -> None :
        if not menu.est_planifie(creneau_cible) :
            raise ValueError(f"Creneau cible non planifié")
        
        if nouveau_bloc.longueur < 1:
            raise ValueError(f"Nouveau bloc de longueur incohérente (<1)")
        
        ancien_bloc = menu.obtenir_bloc(creneau_cible)

        if ancien_bloc == nouveau_bloc:
            raise ValueError(f"Le nouveau bloc est identique à l'ancien bloc")
        
        if menu.contient_bloc(nouveau_bloc):
            raise ValueError(f"Bloc déjà présent dans le Menu")        

        if ancien_bloc.longueur != nouveau_bloc.longueur:
            raise ValueError(f"Incohérence longueur ancien et nouveau bloc")
        
        creneaux_impactes = menu.creneaux_du_bloc(ancien_bloc)
        if len(creneaux_impactes) != ancien_bloc.longueur:
            raise ValueError(f"Incohérence longueur du bloc et nombre de creneaux")
        
        for creneau in creneaux_impactes:
            menu.supprimer_bloc(creneau)

        for creneau in creneaux_impactes:
            menu.ajouter_bloc(creneau,nouveau_bloc)
        
        if not menu.est_stable() :
            raise ValueError(f"Menu instable")
