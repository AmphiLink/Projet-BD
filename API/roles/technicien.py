import os
from time import sleep

from roles.client import profil


def main_technicien(cnx, Id_Pers):
    """
    Cette fonction permet d'utiliser les différentes fonctionnnalités de l'application en tant que Technicien.

    Parameters:
    -----------
    cnx : mysql.connector.connection.MySQLConnection (Object)
    Id_Pers : l'Id de la personne conectée (int)
    """
    choix = "basic"
    os.system("cls")
    while choix not in ("Nettoyer un secteur", "exit", "1", "2"):
        choix = input(
            "\nQue voulez vous faire ?\n 1: Nettoyer un secteur\n 2: exit\n ")
        os.system("cls")

    if choix == "exit" or choix == "2":
        print("Vous avez quitté l'application !")
        sleep(1)
        exit()

    myCursor = cnx.cursor(prepared=True)
    # On récupère l'IdStaff
    queryIdStaff = "SELECT Id_staff FROM STAFF where Id_Pers = %s"
    myCursor.execute(queryIdStaff, (Id_Pers,))
    Id_staff = myCursor.fetchall()[0][0]

    # On récupère l'id_tech
    queryIdTech = "SELECT Id_tech FROM TECHNICIEN WHERE Id_staff = %s"
    myCursor.execute(queryIdTech, (Id_staff,))
    Id_tech = myCursor.fetchall()[0][0]

    if choix == "Nettoyer un secteur" or choix == "1":
        list_secteur(cnx)
        myCursor = cnx.cursor(prepared=True)
        Id_secteur = input("\nQuel secteur voulez vous nettoyer ?\n")
        if Id_secteur == "back":
            main_technicien(cnx, Id_Pers)
        Heure = input("Quelle est l'heure du nettoyage ? (HH:MM)\n")
        Date = input("Quelle est la date du nettoyage ? (AAAA-MM-JJ)\n")

        if Id_secteur == "exit" or Heure == "exit" or Date == "exit":
            print("Vous avez quitté l'application")
            sleep(1)
            exit()

        # On récupère l'id du secteur en question
        queryIdSecteur = "SELECT Id_secteur FROM SECTEUR WHERE Id_secteur = %s"
        myCursor.execute(queryIdSecteur, (Id_secteur,))
        Id_secteur = myCursor.fetchall()[0][0]

        # On insert la table Nettoie
        queryInsertNettoie = "INSERT INTO NETTOIE (Id_tech, Date_net, Heure, Id_secteur) VALUES (%s, %s, %s, %s)"
        myCursor.execute(queryInsertNettoie,
                         (Id_tech, Date, Heure, Id_secteur))
        cnx.commit()
        print("\nVous pouvez aller nettoyer ce secteur !")
        sleep(2)
        main_technicien(cnx, Id_Pers)


def list_secteur(cnx):
    """
    Cette fonction permet d'afficher la liste des secteurs.

    Parameters:
    -----------
    cnx : mysql.connector.connection.MySQLConnection (Object)
    """

    # On récupère la liste des secteurs
    myCursor = cnx.cursor(prepared=True)
    queryListSecteur = "SELECT Id_secteur, Nom FROM SECTEUR"
    myCursor.execute(queryListSecteur)
    listSecteur = myCursor.fetchall()
    print("Voici la liste des secteurs : ")
    for secteur in listSecteur:
        print(secteur[0], ":", secteur[1])
