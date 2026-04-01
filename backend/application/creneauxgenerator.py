from domain.creneau import Creneau

_ORDRE_CRENEAUX = [
            ["dimanche", "midi"],
            ["dimanche", "soir"],
            ["lundi", "midi"],
            ["lundi", "soir"],
            ["mardi", "midi"],
            ["mardi", "soir"],
            ["mercredi", "midi"],
            ["mercredi", "soir"],
            ["jeudi", "midi"],
            ["jeudi", "soir"],
            ["vendredi", "midi"],
            ["vendredi", "soir"],
            ["samedi", "midi"],
            ["samedi", "soir"]
        ]
class CreneauxGenerator:
    def generer_liste_creneaux(self, nombre_repas : int) -> list[Creneau] :
        if nombre_repas < 1 or nombre_repas > len(_ORDRE_CRENEAUX) :
            raise ValueError(f"Nombre repas invalide: {nombre_repas}")
        
        return list(Creneau(_ORDRE_CRENEAUX[i][0],_ORDRE_CRENEAUX[i][1]) for i in range(nombre_repas))
