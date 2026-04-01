from domain.creneau import Creneau

# Fabrique générale 
def creneau(jour : str, moment : str) -> Creneau:
    return Creneau(jour = jour, moment = moment)

# Creneaux nominaux
def lundi_midi() -> Creneau:
    return Creneau(jour = "lundi", moment = "midi")

def lundi_soir() -> Creneau:
    return Creneau(jour = "lundi", moment = "soir")

def mardi_midi() -> Creneau:
    return Creneau(jour = "mardi", moment = "midi")

def mardi_soir() -> Creneau:
    return Creneau(jour = "mardi", moment = "soir")

def mercredi_midi() -> Creneau:
    return Creneau(jour = "mercredi", moment = "midi")

def mercredi_soir() -> Creneau:
    return Creneau(jour = "mercredi", moment = "soir")

def jeudi_midi() -> Creneau:
    return Creneau(jour = "jeudi", moment = "midi")

def jeudi_soir() -> Creneau:
    return Creneau(jour = "jeudi", moment = "soir")

def vendredi_midi() -> Creneau:
    return Creneau(jour = "vendredi", moment = "midi")

def vendredi_soir() -> Creneau:
    return Creneau(jour = "vendredi", moment = "soir")

def samedi_midi() -> Creneau:
    return Creneau(jour = "samedi", moment = "midi")

def samedi_soir() -> Creneau:
    return Creneau(jour = "samedi", moment = "soir")

def dimanche_midi() -> Creneau:
    return Creneau(jour = "dimanche", moment = "midi")

def dimanche_soir() -> Creneau:
    return Creneau(jour = "dimanche", moment = "soir")

# Creneaux invalides
def creneau_jour_invalide() -> Creneau:
    return Creneau(jour="lundii", moment="midi")

def creneau_moment_invalide() -> Creneau:
    return Creneau(jour="lundi", moment="matin")

def creneau_jour_vide() -> Creneau:
    return Creneau(jour="", moment="midi")

def creneau_moment_vide() -> Creneau:
    return Creneau(jour="lundi", moment="")