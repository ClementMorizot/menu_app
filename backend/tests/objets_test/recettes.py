from uuid import uuid4
from domain.recette import Recette

# Fabrique générale
def recette(id, nom: str,description : str,temps_preparation : int, nombre_repas: int) -> Recette:
    return Recette(id,nom,description,temps_preparation,nombre_repas)

# Recettes valides nominales
def recette_1_repas(nom="Omelette") -> Recette:
    return Recette(id=uuid4(), nom=nom, description = "Description générique", temps_preparation = 1, nombre_repas=1)

def recette_1_repas_bis() -> Recette:
    return Recette(id=uuid4(), nom="Poelee",description = "Description générique", temps_preparation = 1, nombre_repas=1)

def recette_2_repas(nom="Lasagnes") -> Recette:
    return Recette(id=uuid4(), nom=nom,description = "Description générique", temps_preparation = 1, nombre_repas=2)

def recette_3_repas(nom="Risotto") -> Recette:
    return Recette(id=uuid4(), nom=nom,description = "Description générique", temps_preparation = 1, nombre_repas=3)

# Recettes supplémentaires pour tests Menu et Domain Services
def recette_1_repas_ter() -> Recette:
    return Recette(id=uuid4(), nom="Croque-monsieur",description = "Description générique", temps_preparation = 1, nombre_repas=1)

def recette_1_repas_quater() -> Recette:
    return Recette(id=uuid4(), nom="Salade composee",description = "Description générique", temps_preparation = 1, nombre_repas=1)

def recette_2_repas_bis() -> Recette:
    return Recette(id=uuid4(), nom="Chili con carne",description = "Description générique", temps_preparation = 1, nombre_repas=2)

def recette_2_repas_ter() -> Recette:
    return Recette(id=uuid4(), nom="Hachis parmentier",description = "Description générique", temps_preparation = 1, nombre_repas=2)

def recette_2_repas_quater() -> Recette:
    return Recette(id=uuid4(), nom="Curry de poulet",description = "Description générique", temps_preparation = 1, nombre_repas=2)

def recette_3_repas_bis() -> Recette:
    return Recette(id=uuid4(), nom="Couscous",description = "Description générique", temps_preparation = 1, nombre_repas=3)

def recette_3_repas_ter() -> Recette:
    return Recette(id=uuid4(), nom="Paella",description = "Description générique", temps_preparation = 1, nombre_repas=3)

# Recette valide limite
def recette_nom_minimal() -> Recette:
    return Recette(id=uuid4(), nom="A",description = "Description générique", temps_preparation = 1, nombre_repas=1)

def recette_nombre_repas_maximal(nom="Buffet a volonte") -> Recette:
    return Recette(id=uuid4(), nom=nom,description = "Description générique", temps_preparation = 1, nombre_repas=14)

def recette_nom_long() -> Recette:
    return Recette(
        id=uuid4(),
        nom="Gratin de pommes de terre au reblochon, oignons fondants et lardons fumes",
        description = "Description générique", 
        temps_preparation = 1,
        nombre_repas=2,
    )

# Recettes invalides métier
def recette_nom_vide() -> Recette:
    return Recette(id=uuid4(), nom="",description = "Description générique", temps_preparation = 1, nombre_repas=1)

def recette_nom_blanc() -> Recette:
    return Recette(id=uuid4(), nom="   ",description = "Description générique", temps_preparation = 1, nombre_repas=1)

def recette_nombre_repas_zero() -> Recette:
    return Recette(id=uuid4(), nom="Soupe",description = "Description générique", temps_preparation = 1, nombre_repas=0)

def recette_nombre_repas_negatif() -> Recette:
    return Recette(id=uuid4(), nom="Salade",description = "Description générique", temps_preparation = 1, nombre_repas=-1)

def recette_nombre_repas_excedentaire(nom="Orgie romaine") -> Recette:
    return Recette(id=uuid4(), nom=nom,description = "Description générique", temps_preparation = 1, nombre_repas=15)
