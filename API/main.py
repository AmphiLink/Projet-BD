# Partie Deploy
from auth.authentification import main_auth
from roles.chef import main_chef
from roles.admin import main_admin
from roles.cuisinier import main_cuisinier
from roles.animateur import main_animateur
from roles.technicien import main_technicien
from roles.client import main_client
from __init__ import initialisation
import os


def main():
    """
    Cette fonction apelle toutes les autres fonctions de l'application.
    """

    # On initialise la connexion à la base de données
    cnx = initialisation()
    print("Bienvenue sur notre API Camping.\n")

    # On récupère les informations de l'utilisateur connecté
    chef_state, user_state, Id_Pers = main_auth(cnx)
    if chef_state:
        os.system("cls")
        print("Bienvenue dans la partie Chef de l'application !")
        main_chef(user_state, cnx, Id_Pers)
    else:
        if user_state == "ADMINISTRATION":
            os.system("cls")
            print("Bienvenue dans la partie Admin de l'application !")
            main_admin(cnx, Id_Pers)
        elif user_state == "CUISINIER":
            os.system("cls")
            print("Bienvenue dans la partie Cuisinier de l'application !")
            main_cuisinier(cnx, Id_Pers)
        elif user_state == "ANIMATEUR":
            os.system("cls")
            print("Bienvenue dans la partie Animateur de l'application !")
            main_animateur(cnx, Id_Pers)
        elif user_state == "TECHNICIEN":
            os.system("cls")
            print("Bienvenue dans la partie Technicien de l'application !")
            main_technicien(cnx, Id_Pers)
        else:
            os.system("cls")
            print("Bienvenue dans la partie Client de l'application !")
            main_client(cnx, Id_Pers)

    cnx.close()


main()
