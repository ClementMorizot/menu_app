from .bloc import Bloc
from .creneau import Creneau
from .menu import Menu

class MenuPlanner:
    def __init__(self) -> None:
        pass

    def planifier(self, creneaux: list[Creneau], blocs: list[Bloc]) -> Menu:
        nb_creneaux = len(creneaux)
        nb_repas = sum(bloc.longueur for bloc in blocs)

        if nb_repas != nb_creneaux:
            raise ValueError(
                f"Incohérence: somme des longueurs de blocs = {nb_repas} "
                f"mais nombre de créneaux = {nb_creneaux}."
            )

        for bloc in blocs:
            if bloc.longueur <= 0:
                raise ValueError(f"Bloc invalide: longueur={bloc.longueur} (doit être > 0).")

        menu = Menu()
        i = 0

        for bloc in blocs:
            for _ in range(bloc.longueur):
                # i est garanti valide grâce au check nb_repas == nb_creneaux
                menu.ajouter_bloc(creneaux[i], bloc)
                i += 1

        if not menu.est_stable():
            raise ValueError("Menu instable après planification (invariants violés).")

        return menu