from . import recettes
from domain.recette import Recette
from domain.bloc import Bloc

# Fabrique à bloc
def bloc_depuis_recette(recette : Recette) -> Bloc:
    return Bloc(recette, recette.nombre_repas)

# Blocs valides nominaux
def bloc_longueur_1() -> Bloc:
    recette = recettes.recette_1_repas()
    return bloc_depuis_recette(recette)

def bloc_longueur_2() -> Bloc:
    recette = recettes.recette_2_repas()
    return bloc_depuis_recette(recette)

def bloc_longueur_3() -> Bloc:
    recette = recettes.recette_3_repas()
    return bloc_depuis_recette(recette)

# Blocs supplémentaires pour tests Menu et Domain Services
def bloc_longueur_1_bis() -> Bloc:
    recette = recettes.recette_1_repas_bis()
    return bloc_depuis_recette(recette)

def bloc_longueur_1_ter() -> Bloc:
    recette = recettes.recette_1_repas_ter()
    return bloc_depuis_recette(recette)

def bloc_longueur_1_quater() -> Bloc:
    recette = recettes.recette_1_repas_quater()
    return bloc_depuis_recette(recette)

def bloc_longueur_2_bis() -> Bloc:
    recette = recettes.recette_2_repas_bis()
    return bloc_depuis_recette(recette)

def bloc_longueur_2_ter() -> Bloc:
    recette = recettes.recette_2_repas_ter()
    return bloc_depuis_recette(recette)

def bloc_longueur_2_quater() -> Bloc:
    recette = recettes.recette_2_repas_quater()
    return bloc_depuis_recette(recette)

def bloc_longueur_3_bis() -> Bloc:
    recette = recettes.recette_3_repas_bis()
    return bloc_depuis_recette(recette)

# Blocs valides limites
def bloc_longueur_minimale() -> Bloc:
    recette = recettes.recette_1_repas_bis()
    return bloc_depuis_recette(recette)

def bloc_longueur_maximale() -> Bloc:
    recette = recettes.recette_nombre_repas_maximal()
    return bloc_depuis_recette(recette)

# Blocs invalides métier
def bloc_longueur_excedentaire() -> Bloc:
    recette = recettes.recette_nombre_repas_excedentaire()
    return bloc_depuis_recette(recette)

def bloc_longueur_nulle() -> Bloc:
    recette = recettes.recette_nombre_repas_zero()
    return bloc_depuis_recette(recette)

def bloc_longueur_negative() -> Bloc:
    recette = recettes.recette_nombre_repas_negatif()
    return bloc_depuis_recette(recette)
