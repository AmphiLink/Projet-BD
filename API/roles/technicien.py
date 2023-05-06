import os
from time import sleep


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
    while choix not in ("Nettoyer un secteur", "profil", "exit", "1", "2", "3"):
        choix = input(
            "\nQue voulez vous faire ?\n (1: Nettoyer un secteur, 2: profil, 3: exit)\n ")
        os.system("cls")

    if choix == "exit" or choix == "3":
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
        Id_secteur = input("\nQuel secteur voulez vous nettoyer ? ")
        Heure = input("Quelle est l'heure du nettoyage ? (HH:MM) ")
        Date = input("Quelle est la date du nettoyage ? (AAAA-MM-JJ) ")

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
        print(secteur[0], ": ", secteur[1])
