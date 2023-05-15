import os
from time import sleep
from datetime import datetime
from roles.client import profil
import time


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
    while choix not in ("Nettoyer un secteur", "exit", "1", "2", "3"):
        choix = input(
            "\nQue voulez vous faire ?\n1: Nettoyer un secteur\n2: Regarder votre profil\n3: exit\n ")
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

    else:
        # On affiche les données personnelles de l'utilisateur
        myCursor = cnx.cursor(prepared=True)
        os.system("cls")
        print("Voici votre profil : \n========================\n")
        print("Données personnelles : \n=========================")
        prenomsListe = []
        queryPrenoms = "SELECT Prenom FROM Prenom WHERE Id_Pers = %s"
        myCursor.execute(queryPrenoms, (Id_Pers,))
        for prenoms in myCursor:
            prenomsListe.append(prenoms[0])
        myCursor.fetchall()

        queryInfos = "SELECT Id_staff, Nom, Age, Salaire FROM view_Employe_Technicien WHERE Id_staff = %s GROUP BY Id_staff"
        myCursor.execute(queryInfos, (Id_staff,))

        for (Id_staff, Nom, Age, Salaire) in myCursor:
            print("Id : %s\nNom : %s" % (Id_staff, Nom))
            # On affiche les prénoms stockés dans la liste prenomsListe en ligne
            print("Prénom(s) : %s" % (", ".join(prenomsListe)))
            print("Age : %s\nSalaire : %s \u20ac\n" % (Age, Salaire))
        myCursor.fetchall()
        print("Vos secteurs : \n=========================")
        # On vérifie si le technicien a des secteurs à nettoyer
        queryVerif = "SELECT Id_secteur FROM NETTOIE WHERE Id_tech = %s"
        myCursor.execute(queryVerif, (Id_tech,))
        verif = myCursor.fetchall()

        if verif == []:
            print("Vous n'avez pas de secteurs à nettoyer !")
            a = input("\nAppuyez sur une enter pour continuer")
            if a == "":
                sleep(1)
                os.system("cls")
                main_technicien(cnx, Id_Pers)
        # On récupère les secteurs à nettoyer où qui ont été nettoyés
        querySecteurs = "SELECT Id_secteur, Nom_secteur, Date_net, Heure FROM view_Employe_Technicien WHERE Id_staff = %s GROUP BY Date_net, Heure"
        myCursor.execute(querySecteurs, (Id_staff,))

        verif = 0
        madate = datetime.today()
        MonHeure = datetime.now().time()
        for (Id_secteur, Nom_secteur, Date_net, Heure) in myCursor:
            if verif == 1:
                print("\n=========================")
            # On vérifie si la date d'aujourd'hui est inférieur à la date de nettoyage
            Date_net = datetime.strptime(str(Date_net), '%Y-%m-%d')
            Heure = datetime.strptime(str(Heure), '%H:%M').time()
            if madate <= Date_net and MonHeure <= Heure:
                print("Id : %s\nNom : %s" % (Id_secteur, Nom_secteur))
                print("Date du prochain nettoyage : %s\nHeure du prochain nettoyage : %s\n" % (
                    Date_net, Heure))
            else:
                print("Id : %s\nNom : %s" % (Id_secteur, Nom_secteur))
                print("Date du dernier nettoyage : %s\nHeure du dernier nettoyage : %s\n" % (
                    Date_net, Heure))
            verif = 1

        a = input("\nAppuyez sur une enter pour continuer")
        if a == "":
            sleep(1)
            os.system("cls")
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
