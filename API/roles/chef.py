from time import sleep
from auth.hash import hash_password
from auth.authentification import staffPrice
from roles.cuisinier import stop_emplacement
import datetime
import os


def main_chef(user_state, cnx, Id_Pers):
    """
    Cette fonction permet d'utiliser les différentes fonctionnnalités de l'application en tant que Chef.

    Parameters:
    -----------
    user_state: le job de l'utilisateur concerné (str)
    cnx : mysql.connector.connection.MySQLConnection (Object)
    Id_Pers : l'Id de la personne concernée (int)
    """

    choix = "basic"
    while choix not in ("liste_employees", "supprimer_employee", "rajouter_employee", "profil", "exit"):
        choix = input(
            "Que voulez vous faire ? (liste_employees, supprimer_employee, rajouter_employee, profil, exit) ")
        sleep(1)

    myCursor = cnx.cursor(prepared=True)
    if choix == "liste_employees":
        # On récupère la liste des employés ayant le même job que le chef
        queryList = "SELECT P.Nom, Pre.Prenom, P.Age FROM PERSONNE P JOIN Prenom Pre ON P.Id_Pers = Pre.Id_Pers JOIN STAFF S ON P.Id_Pers = S.Id_Pers JOIN {} J ON S.Id_staff = J.Id_staff".format(
            user_state)
        myCursor.execute(queryList)
        print(myCursor.fetchall())
        sleep(5)

    elif choix == "rajouter_employee":
        nom = input("Nom de l'employé : ")
        prenom = input("Prénom de l'employé : ")
        prenomsListe = prenom.split(" ")
        age = input("Age de l'employé : ")
        password = input("Mot de passe de l'employé : ")

        if nom == "exit" or prenom == "exit" or age == "exit" or password == "exit":
            print("Vous avez quitté l'application")
            sleep(1)
            exit()

        # On hash le mot de passe
        password = hash_password(password)

        # Insertion dans la table Personne
        queryInsert = "INSERT INTO PERSONNE (Nom, Age, Mot_de_passe) VALUES (%s, %s, %s)"
        myCursor.execute(queryInsert, (nom, age, password))
        cnx.commit()

        UserPrice = staffPrice(user_state)
        # Insertion dans la table Staff du nouvel employé
        queryInsertStaff = "INSERT INTO STAFF (Id_Pers, Prix) VALUES (%s, %s)"
        myCursor.execute(queryInsertStaff, (myCursor.lastrowid, UserPrice))
        cnx.commit()

        # Insertion dans la table correspondante au job de l'employé
        queryInsertJob = "INSERT INTO {} (Id_staff) VALUES (%s)".format(
            user_state)
        myCursor.execute(queryInsertJob, (myCursor.lastrowid,))
        cnx.commit()

        # Partie pour insérer le.s prénom.s de l'employé
        queryId = "SELECT Id_Pers FROM PERSONNE WHERE Nom = %s AND  Age = %s"
        myCursor.execute(queryId, (nom, age))
        Id_Pers = myCursor.fetchall()[0][0]
        for prenom in prenomsListe:
            queryInsertPrenom = "INSERT INTO Prenom (Id_Pers, Prenom) VALUES (%s, %s)"
            myCursor.execute(queryInsertPrenom, (Id_Pers, prenom))
            cnx.commit()
        print("L'employé a bien été ajouté !")

    elif choix == "supprimer_employee":
        nom = input("Nom de l'employé : ")
        age = input("Age de l'employé : ")

        if age == "exit" or nom == "exit":
            print("Vous avez quitté l'application")
            sleep(1)
            exit()

        queryTest = "SELECT Nom, Age FROM PERSONNE WHERE Nom = %s AND Age = %s"
        myCursor.execute(queryTest, (nom, age))
        test = myCursor.fetchall()

        if test == []:
            print("Cet employé n'existe pas !")
            sleep(1)
            return main_chef(user_state, cnx, Id_Pers)

        queryIdPers = "SELECT Id_Pers FROM PERSONNE WHERE Nom = %s AND Age = %s"
        myCursor.execute(queryIdPers, (nom, age))
        Id_Pers = myCursor.fetchall()[0][0]

        queryIdStaff = "SELECT Id_staff FROM STAFF WHERE Id_Pers = %s"
        myCursor.execute(queryIdStaff, (Id_Pers,))
        Id_staff = myCursor.fetchall()[0][0]

        # Suppresssion d'un animateur
        if user_state == "ANIMATEUR":
            # On récupère Id_anim
            queryIdAnim = "SELECT Id_anim FROM ANIMATEUR WHERE Id_staff = %s"
            myCursor.execute(queryIdAnim, (Id_staff,))
            Id_anim = myCursor.fetchall()[0][0]
            # On s'intéresse d'abord aux tables ACTIVITE et peut_faire

            # On supprime d'abord dans la table peut_faire
            queryDeletePeutFaire = "DELETE FROM peut_faire WHERE Id_anim = %s"
            myCursor.execute(queryDeletePeutFaire, (Id_anim,))
            cnx.commit()

            # On supprime ID_anim dans la table ACTIVITE
            # Dans ce cas-ci on ne supprime pas l'activité car elle peut être faite par d'autres animateurs
            # On vérifie si la date de l'activité est passée
            queryNbrJours = "SELECT DATEDIFF(Date_acti, NOW()) FROM ACTIVITE WHERE Id_anim = %s"
            myCursor.execute(queryNbrJours, (Id_anim,))
            DateList = myCursor.fetchall()
            for Date_acti in DateList:
                maDate = str(Date_acti[0])
                queryNbrJours = "SELECT DATEDIFF(Date_acti, NOW()) FROM ACTIVITE WHERE Id_anim = %s and Date_acti = %s"
                myCursor.execute(queryNbrJours, (Id_anim, maDate))
                nbrJours = myCursor.fetchall()[0][0]
                if nbrJours < 0:
                    # Cela veut dire que l'activité est passée
                    pass
                else:
                    queryDeleteActivite = "UPDATE ACTIVITE SET Id_anim = NULL WHERE Id_anim = %s AND Date_acti = %s"
                    myCursor.execute(queryDeleteActivite, (Id_anim, maDate))
                    cnx.commit()

            # On s'intéresse à la table ANIMATEUR
            # On supprime seulement Id_staff de animateur
            queryDeleteAnim = "Update ANIMATEUR SET Id_staff = NULL WHERE Id_anim = %s"
            myCursor.execute(queryDeleteAnim, (Id_anim,))
            cnx.commit()

        # Suppresion d'un cuisnier
        elif user_state == "CUISINIER":
            # On récupère Id_cuis
            queryIdCuis = "SELECT Id_cuis FROM CUISINIER WHERE Id_staff = %s"
            myCursor.execute(queryIdCuis, (Id_staff,))
            Id_cuis = myCursor.fetchall()[0][0]

            # On vérifie si il travaille pour un emplacement
            queryEmplacement = "SELECT Id_emplacement FROM cuisine WHERE Id_cuis = %s"
            myCursor.execute(queryEmplacement, (Id_cuis,))
            test = myCursor.fetchall()

            if test == []:
                # Cela veut dire qu'il ne travaille pas pour un emplacement
                pass
            else:
                # On le fait arrêter de travailler pour l'emplacement pour lequel il travaille
                stop_emplacement(cnx, Id_Pers, Id_cuis)

            # On vérifie si il travaille pour un tournoi
            queryTournoi = "SELECT Id_tournoi FROM cuisine WHERE Id_cuis = %s"
            myCursor.execute(queryTournoi, (Id_cuis,))
            test = myCursor.fetchall()

            if test == []:
                # Cela veut dire qu'il ne travaille pas pour un tournoi
                pass
            else:
                # On vérifie si le tournoi est passé
                Id_tournoi = test[0][0]
                queryNbrJours = "SELECT DATEDIFF(Date_tournoi, NOW()) FROM TOURNOI WHERE Id_tournoi = %s"
                myCursor.execute(queryNbrJours, (Id_tournoi,))
                DateList = myCursor.fetchall()

                for Date_tournoi in DateList:
                    maDate = str(Date_tournoi[0])
                    queryNbrJours = "SELECT DATEDIFF(Date_tournoi, NOW()) FROM TOURNOI WHERE Id_tournoi = %s and Date_tournoi = %s"
                    myCursor.execute(queryNbrJours, (Id_tournoi, maDate))
                    nbrJours = myCursor.fetchall()[0][0]

                    if nbrJours < 0:
                        # Cela veut dire que le tournoi est passé
                        pass
                    else:
                        # On supprime Id_cuis de la table cuisine afin qu'un autre cuisinier le remplace
                        queryDeleteCuisine = "UPDATE CUISINE SET Id_cuis = NULL WHERE Id_cuis = %s AND Id_tournoi IN (SELECT Id_tournoi FROM TOURNOI WHERE Date_tournoi = %s)"
                        myCursor.execute(queryDeleteCuisine,
                                         (Id_cuis, Id_tournoi, maDate))
                        cnx.commit()

            # On supprime Id_staff de CUISINIER
            queryDeleteCuisine = "UPDATE CUISINIER SET Id_staff = NULL WHERE Id_cuis = %s"
            myCursor.execute(queryDeleteCuisine, (Id_cuis,))
            cnx.commit()

        # Suppression d'un technicien
        elif user_state == "TECHNICIEN":
            # On récupère Id_tech
            queryIdTech = "SELECT Id_tech FROM TECHNICIEN WHERE Id_staff = %s"
            myCursor.execute(queryIdTech, (Id_staff,))
            Id_tech = myCursor.fetchall()[0][0]

            # On s'intéresse à la table NETTOIE
            # On vérifie si la date de son netoyage est passée
            queryDateNet = "SELECT Date_net FROM NETTOIE WHERE Id_tech = %s"
            myCursor.execute(queryDateNet, (Id_tech,))
            DateList = myCursor.fetchall()

            DateCursor = cnx.cursor()
            for Date_net in DateList:
                maDate = str(Date_net[0])
                queryNbrJours = "SELECT DATEDIFF(Date_net, NOW()) FROM NETTOIE WHERE Id_tech = %s AND Date_net = %s"
                DateCursor.execute(queryNbrJours, (Id_tech, maDate))
                nbrJours = DateCursor.fetchall()[0][0]
                if nbrJours < 0:
                    # Cela veut dire que le nettoyage est passé
                    pass
                else:
                    queryDeleteTechnicien = "UPDATE NETTOIE SET Id_tech = NULL WHERE Id_tech = %s  AND DATE_NET = %s"
                    DateCursor.execute(
                        queryDeleteTechnicien, (Id_tech, maDate))
                    cnx.commit()

            # On supprime Id_staff de TECHNICIEN
            queryDeleteTechnicien = "UPDATE TECHNICIEN SET Id_staff = NULL WHERE Id_tech = %s"
            myCursor.execute(queryDeleteTechnicien, (Id_tech,))
            cnx.commit()

        # Suppression d'un administrateur
        else:
            # On réupère Id_admin de ADMINISTRATION
            queryIdAdmin = "SELECT Id_admin FROM ADMINISTRATION WHERE Id_staff = %s"
            myCursor.execute(queryIdAdmin, (Id_staff,))
            Id_admin = myCursor.fetchall()[0][0]

            # On ne supprime rien dans fiche compta on doit garder un historique de toute la compta de chaque année et chaque mois

            # On supprime Id_admin de MATERIEL (pas besoin d'historique sur qui s'occupe de la gestion du matériel)
            queryDeleteAdmin = "UPDATE MATERIEL SET Id_admin = NULL WHERE Id_admin = %s"
            myCursor.execute(queryDeleteAdmin, (Id_admin,))
            cnx.commit()

            # On supprime Id_staff de ADMINISTRATION
            queryDeleteAdmin = "UPDATE ADMINISTRATION SET Id_staff = NULL WHERE Id_admin = %s"
            myCursor.execute(queryDeleteAdmin, (Id_admin,))
            cnx.commit()

        # Ces étapes sont communes à tous les jobs

        # Suppression dans la table Staff du nouvel employé
        queryDeleteStaff = "DELETE FROM STAFF WHERE Id_Pers = %s"
        myCursor.execute(queryDeleteStaff, (Id_Pers,))
        cnx.commit()

        # Partie pour supprimer le.s prénom.s de l'employé
        queryDeletePrenom = "UPDATE Prenom SET Prenom = 'Anonymized' WHERE Id_Pers = %s"
        myCursor.execute(queryDeletePrenom, (Id_Pers,))
        cnx.commit()

        # Suppression dans la table Personne
        queryDelete = "UPDATE PERSONNE SET Nom = 'Anonymized', Age = -1, Mot_de_passe = 'Anonymized' WHERE Id_Pers = %s"
        myCursor.execute(queryDelete, (Id_Pers,))
        cnx.commit()
        print("L'employé a bien été supprimé !")
        main_chef(user_state, cnx, Id_Pers)
    else:
        print("Vous avez quitté l'application")
        sleep(1)
        exit()

    os.system("cls")
    main_chef(user_state, cnx, Id_Pers)
