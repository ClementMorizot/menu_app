from domain.menu import Menu
from . import blocs, creneaux


def menu_vide() -> Menu:
    return Menu()


def menu_depuis_associations(associations) -> Menu:
    menu = Menu()
    for creneau, bloc in associations:
        menu.ajouter_bloc(creneau, bloc)
    return menu

def menu_nominal_simple() -> Menu:
    return menu_depuis_associations([
        (creneaux.lundi_midi(), blocs.bloc_longueur_1()),
    ])

def menu_partiel_stable() -> Menu:
    bloc_1 = blocs.bloc_longueur_1()
    bloc_2 = blocs.bloc_longueur_2()
    bloc_3 = blocs.bloc_longueur_3()

    return menu_depuis_associations([
        (creneaux.lundi_midi(), bloc_1),
        (creneaux.lundi_soir(), bloc_2),
        (creneaux.mardi_midi(), bloc_2),
        (creneaux.mardi_soir(), bloc_3),
        (creneaux.mercredi_midi(), bloc_3),
        (creneaux.mercredi_soir(), bloc_3),
    ])

def menu_nominal_complet() -> Menu:
    bloc_1 = blocs.bloc_longueur_1()
    bloc_2 = blocs.bloc_longueur_2()
    bloc_3 = blocs.bloc_longueur_3()
    bloc_1_bis = blocs.bloc_longueur_1_bis()
    bloc_2_bis = blocs.bloc_longueur_2_bis()
    bloc_3_bis = blocs.bloc_longueur_3_bis()
    bloc_1_ter = blocs.bloc_longueur_1_ter()
    bloc_2_ter = blocs.bloc_longueur_2_ter()
    bloc_1_quater = blocs.bloc_longueur_1_quater()

    return menu_depuis_associations([
        (creneaux.lundi_midi(), bloc_1),
        (creneaux.lundi_soir(), bloc_2),
        (creneaux.mardi_midi(), bloc_2),
        (creneaux.mardi_soir(), bloc_3),
        (creneaux.mercredi_midi(), bloc_3),
        (creneaux.mercredi_soir(), bloc_3),
        (creneaux.jeudi_midi(), bloc_1_bis),
        (creneaux.jeudi_soir(), bloc_2_bis),
        (creneaux.vendredi_midi(), bloc_2_bis),
        (creneaux.vendredi_soir(), bloc_3_bis),
        (creneaux.samedi_midi(), bloc_1_ter),
        (creneaux.samedi_soir(), bloc_2_ter),
        (creneaux.dimanche_midi(), bloc_2_ter),
        (creneaux.dimanche_soir(), bloc_1_quater),
    ])

def menu_instable_longueur_bloc_incoherente() -> Menu : 
    bloc_1 = blocs.bloc_longueur_1()
    bloc_2 = blocs.bloc_longueur_2()
    return menu_depuis_associations([
        (creneaux.lundi_midi(), bloc_1),
        (creneaux.lundi_soir(), bloc_2),
        (creneaux.mardi_midi(), bloc_2),
        (creneaux.mardi_soir(), bloc_1),
    ])

def menu_instable_bloc_incomplet() -> Menu :
    bloc_1 = blocs.bloc_longueur_1()
    bloc_2 = blocs.bloc_longueur_2()
    bloc_3 = blocs.bloc_longueur_3()

    return menu_depuis_associations([
        (creneaux.lundi_midi(), bloc_1),
        (creneaux.lundi_soir(), bloc_2),
        (creneaux.mardi_midi(), bloc_2),
        (creneaux.mardi_soir(), bloc_3),
        (creneaux.mercredi_midi(), bloc_3),
    ])

def menu_pour_reroll() -> Menu : 
    bloc_1 = blocs.bloc_longueur_1()
    bloc_2 = blocs.bloc_longueur_2()
    bloc_1_bis = blocs.bloc_longueur_1_bis()

    return menu_depuis_associations([
        (creneaux.lundi_midi(), bloc_1),
        (creneaux.lundi_soir(), bloc_2),
        (creneaux.mardi_midi(), bloc_2),
        (creneaux.mardi_soir(), bloc_1_bis),
    ])

def menu_un_bloc_longueur_3() -> Menu:
    bloc = blocs.bloc_longueur_3()

    return menu_depuis_associations([
        (creneaux.mardi_soir(), bloc),
        (creneaux.mercredi_midi(), bloc),
        (creneaux.mercredi_soir(), bloc),
    ])

def menu_deux_blocs_longueur_2() -> Menu:
    bloc_1 = blocs.bloc_longueur_2()
    bloc_2 = blocs.bloc_longueur_2_bis()

    return menu_depuis_associations([
        (creneaux.lundi_midi(), bloc_1),
        (creneaux.lundi_soir(), bloc_1),
        (creneaux.mardi_midi(), bloc_2),
        (creneaux.mardi_soir(), bloc_2),
    ])