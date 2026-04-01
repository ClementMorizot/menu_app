#domain/menu.py

from typing import Dict
from .creneau import Creneau
from .bloc import Bloc

class Menu:
    def __init__(self):
        self._planning: Dict[Creneau, Bloc] = {}
    
    @property
    def planning(self) -> Dict[Creneau, Bloc]:
        return self._planning.copy()
    
    def ajouter_bloc(self, creneau: Creneau, bloc: Bloc):
        if creneau in self._planning:
            raise ValueError(f"Le créneau est déjà planifié.")
        self._planning[creneau] = bloc

    def remplacer_bloc(self, creneau: Creneau, nouveau_bloc: Bloc):
        if creneau not in self._planning:
            raise ValueError(f"Créneau non planifié")

        self._planning[creneau] = nouveau_bloc

    def est_planifie(self, creneau: Creneau) -> bool:
        return creneau in self._planning
    
    def supprimer_bloc(self, creneau: Creneau) -> None:
        if creneau not in self._planning:
            raise ValueError(f"Créneau non planifié")
        del self._planning[creneau]
        
    def obtenir_bloc(self, creneau: Creneau) -> Bloc:
        if creneau not in self._planning:
            raise ValueError(f"Créneau non planifié")
        return self._planning[creneau]
    
    def contient_bloc(self, bloc: Bloc) -> bool:
        return bloc in self._planning.values()
    
    def creneaux_du_bloc(self, bloc: Bloc) -> list[Creneau]:
        creneaux = []
        for creneau, b in self._planning.items():
            if b == bloc:
                creneaux.append(creneau)
        return creneaux

    def creneaux_planifies(self) -> list[Creneau]:
        creneaux = []
        for c in self._planning.keys():
            creneaux.append(c)
        
        return creneaux
    
    def est_complet(self, nombre_creneaux_attendus: int) -> bool:
        return len(self._planning) == nombre_creneaux_attendus
    
    def peut_remplacer(self, creneau:Creneau, nouveau_bloc : Bloc) -> bool:
        if not self.est_planifie(creneau):
            return False
        if self.contient_bloc(nouveau_bloc):
            return False
        return True
    
    def verifier_coherence_longueur(self) -> bool:
        for bloc in self.blocs_uniques():
            if len(self.creneaux_du_bloc(bloc)) != bloc.longueur:
                return False
        return True
    
    def blocs_uniques(self) -> list[Bloc]:
        blocs_uniques = []
        for bloc in self._planning.values():
            if bloc not in blocs_uniques:
                blocs_uniques.append(bloc)

        return blocs_uniques
    
    def nombre_total_repas(self) -> int:
        somme_total = 0
        blocs = self.blocs_uniques()
        for bloc in blocs:
            somme_total += bloc.longueur
        
        return somme_total

    def est_stable(self) -> bool:
        return (len(self._planning) == self.nombre_total_repas()) and self.verifier_coherence_longueur()
    