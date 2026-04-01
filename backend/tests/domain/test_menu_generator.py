from tests.objets_test import recettes
from domain.bloc import Bloc
from domain.generator import MenuGenerator
from tests.fakes.fake_repository import FakeRecipeRepository
import pytest

# Tests de la méthode creer_bloc(recette)

def test_creer_bloc_retourne_un_bloc_de_meme_longueur_que_la_recette():
    # Arrange
    recette = recettes.recette_2_repas()
    repository = FakeRecipeRepository([recette])
    generator = MenuGenerator(repository)

    # Act
    bloc = generator.creer_bloc(recette)

    # Assert
    assert bloc.recette_snapshot == recette
    assert bloc.longueur == recette.nombre_repas

@pytest.mark.parametrize(
    "fabrique_recette,longueur_attendue",
    [
        (recettes.recette_1_repas, 1),
        (recettes.recette_2_repas, 2),
        (recettes.recette_nombre_repas_maximal, 14),
        (recettes.recette_nombre_repas_zero, 0),
        (recettes.recette_nombre_repas_negatif, -1),
    ],
)
def test_creer_bloc_recopie_nombre_repas_dans_longueur(fabrique_recette, longueur_attendue):
    recette = fabrique_recette()
    repository = FakeRecipeRepository([recette])
    generator = MenuGenerator(repository)

    bloc = generator.creer_bloc(recette)

    assert bloc.longueur == longueur_attendue

# Tests de la méthode creer_blocs(nombre_repas)

def test_creer_liste_blocs_cas_simple():
    # Arrange
    nombre_repas = 3
    recette_1 = recettes.recette_1_repas()
    recette_2 = recettes.recette_2_repas()
    repository = FakeRecipeRepository([recette_1, recette_2])
    generator = MenuGenerator(repository)

    # Act
    blocs = generator.creer_liste_blocs(nombre_repas)

    # Assert

    # 1. somme correcte
    assert sum(b.longueur for b in blocs) == nombre_repas

    # 2. pas de doublon de recette
    ids = [b.recette_snapshot.id for b in blocs]
    assert len(ids) == len(set(ids))

    # 3. types corrects
    assert all(isinstance(b, Bloc) for b in blocs)

    # 4. correspond aux recettes disponibles
    recettes_ids = {recette_1.id, recette_2.id}
    assert all(b.recette_snapshot.id in recettes_ids for b in blocs)

def test_creer_liste_blocs_cas_repository_vide():
    # Arrange
    nombre_repas = 1
    repository = FakeRecipeRepository([])
    generator = MenuGenerator(repository)

    # Act / Assert
    with pytest.raises(ValueError) : 
        generator.creer_liste_blocs(nombre_repas)

def test_creer_liste_blocs_cas_repository_insuffisant():
    # Arrange
    nombre_repas = 14
    recette_1 = recettes.recette_1_repas()
    recette_2 = recettes.recette_2_repas()
    repository = FakeRecipeRepository([recette_1, recette_2])
    generator = MenuGenerator(repository)

    # Act / Assert
    with pytest.raises(ValueError) : 
        generator.creer_liste_blocs(nombre_repas)

def test_creer_liste_blocs_cas_nominal_14_repas():
    # Arrange
    nombre_repas = 14
    recette_1 = recettes.recette_1_repas()
    recette_1_bis = recettes.recette_1_repas_bis()
    recette_1_ter = recettes.recette_1_repas_ter()
    recette_1_quater = recettes.recette_1_repas_quater()
    recette_2 = recettes.recette_2_repas()
    recette_2_bis = recettes.recette_2_repas_bis()
    recette_2_ter = recettes.recette_2_repas_ter()
    recette_2_quater = recettes.recette_2_repas_quater()
    recette_3 = recettes.recette_3_repas()
    recette_3_bis = recettes.recette_3_repas_bis()
    liste_recettes = [recette_1,recette_1_bis,recette_1_ter,recette_1_quater,recette_2,recette_2_bis,recette_2_ter,recette_2_quater,recette_3,recette_3_bis]
    repository = FakeRecipeRepository(liste_recettes)
    generator = MenuGenerator(repository)

    # Act
    liste_blocs = generator.creer_liste_blocs(nombre_repas)

    # Assert

    # 1. Somme correct
    assert sum(b.longueur for b in liste_blocs) == nombre_repas

    # 2. pas de doublon de recette
    liste_ids = [b.recette_snapshot.id for b in liste_blocs]
    assert len(liste_ids) == len(set(liste_ids))

    # 3. vérification des types
    assert all(isinstance(bloc,Bloc) for bloc in liste_blocs)

    # 4. correspond aux recettes disponibles
    recettes_selectionnees = [b.recette_snapshot for b in liste_blocs]
    assert all(recette in liste_recettes for recette in recettes_selectionnees)

def test_creer_liste_cas_monobloc():
    # Arrange
    nombre_repas = 3
    recette = recettes.recette_3_repas()
    repository = FakeRecipeRepository([recette])
    generator = MenuGenerator(repository)

    # Act
    blocs = generator.creer_liste_blocs(nombre_repas)

    # Assert

    # 1. somme correcte
    assert blocs[0].longueur == nombre_repas

    # 2. recette correcte
    assert blocs[0].recette_snapshot == recette

    # 3. types corrects
    assert all(isinstance(b, Bloc) for b in blocs)

    # 4. nombre de bloc = 1
    assert len(blocs) == 1

# Tests de la méthode creer_bloc_pour_reroll

def test_creer_un_bloc_pour_reroll_dans_un_repository_nominal():
    # Arrange
    recette_1 = recettes.recette_1_repas()
    recette_1_bis = recettes.recette_1_repas_bis()
    recette_2 = recettes.recette_2_repas()
    liste_recettes = [recette_1,recette_1_bis,recette_2]
    repository = FakeRecipeRepository(liste_recettes)
    blocgenerator = MenuGenerator(repository)
    longueur_bloc = 1
    recettes_exclues = [recette_1]

    # Act
    nouveau_bloc = blocgenerator.creer_bloc_pour_reroll(longueur_bloc,recettes_exclues)

    # Assert
    assert isinstance(nouveau_bloc,Bloc)
    assert nouveau_bloc.longueur == longueur_bloc
    assert nouveau_bloc.recette_snapshot == recette_1_bis

def test_creer_bloc_pour_reroll_choisit_une_recette_compatible_parmi_plusieurs_candidates():
    # Arrange
    recette_1 = recettes.recette_1_repas()
    recette_1_bis = recettes.recette_1_repas_bis()
    recette_1_ter = recettes.recette_1_repas_ter()
    liste_recettes = [recette_1, recette_1_bis, recette_1_ter]
    repository = FakeRecipeRepository(liste_recettes)
    blocgenerator = MenuGenerator(repository)

    # Act
    nouveau_bloc = blocgenerator.creer_bloc_pour_reroll(1, [recette_1])

    # Assert
    assert nouveau_bloc.longueur == 1
    assert nouveau_bloc.recette_snapshot in [recette_1_bis, recette_1_ter]
    assert nouveau_bloc.recette_snapshot not in [recette_1]
    
def test_creer_un_bloc_pour_reroll_avec_longueur_inferieur_a_1():
    # Arrange
    recette_1 = recettes.recette_1_repas()
    recette_1_bis = recettes.recette_1_repas_bis()
    recette_2 = recettes.recette_2_repas()
    liste_recettes = [recette_1,recette_1_bis,recette_2]
    repository = FakeRecipeRepository(liste_recettes)
    blocgenerator = MenuGenerator(repository)
    longueur_bloc = 0
    recettes_exclues = [recette_1]

    # Act / assert
    with pytest.raises(ValueError):
        _ = blocgenerator.creer_bloc_pour_reroll(longueur_bloc,recettes_exclues)

def test_creer_bloc_pour_reroll_sans_recette_compatible_disponible():
    # Arrange
    recette_1 = recettes.recette_1_repas()
    recette_1_bis = recettes.recette_1_repas_bis()
    recette_2 = recettes.recette_2_repas()
    liste_recettes = [recette_1,recette_1_bis,recette_2]
    repository = FakeRecipeRepository(liste_recettes)
    blocgenerator = MenuGenerator(repository)
    longueur_bloc = 3
    recettes_exclues = [recette_1]

    # Act / assert
    with pytest.raises(ValueError):
        _ = blocgenerator.creer_bloc_pour_reroll(longueur_bloc,recettes_exclues)

def test_creer_bloc_pour_reroll_en_verifiant_la_liste_des_exclusions():
    # Arrange
    recette_1 = recettes.recette_1_repas()
    recette_1_bis = recettes.recette_1_repas_bis()
    recette_2 = recettes.recette_2_repas()
    liste_recettes = [recette_1,recette_1_bis,recette_2]
    repository = FakeRecipeRepository(liste_recettes)
    blocgenerator = MenuGenerator(repository)
    longueur_bloc = 2
    recettes_exclues = [recette_2]

    # Act / assert
    with pytest.raises(ValueError):
        _ = blocgenerator.creer_bloc_pour_reroll(longueur_bloc,recettes_exclues)