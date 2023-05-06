from time import sleep
from auth.hash import hash_password
from auth.authentification import staffPrice
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

        # Suppression dans la table correspondante au job de l'employé
        queryDeleteJob = "DELETE FROM {} WHERE Id_staff = (SELECT Id_staff FROM STAFF WHERE Id_Pers = (SELECT Id_Pers FROM PERSONNE WHERE Nom = %s AND Age = %s))".format(
            user_state)
        myCursor.execute(queryDeleteJob, (nom, age))
        cnx.commit()

        # Suppression dans la table Staff du nouvel employé
        queryDeleteStaff = "DELETE FROM STAFF WHERE Id_Pers = (SELECT Id_Pers FROM PERSONNE WHERE Nom = %s AND Age = %s)"
        myCursor.execute(queryDeleteStaff, (nom, age))
        cnx.commit()

        # Partie pour supprimer le.s prénom.s de l'employé
        queryId = "SELECT Id_Pers FROM PERSONNE WHERE Nom = %s AND  Age = %s"
        myCursor.execute(queryId, (nom, age))
        Id_Pers = myCursor.fetchall()[0][0]
        queryDeletePrenom = "DELETE FROM Prenom WHERE Id_Pers = %s"
        myCursor.execute(queryDeletePrenom, (Id_Pers,))
        cnx.commit()

        # Suppression dans la table Personne
        queryDelete = "DELETE FROM PERSONNE WHERE Nom = %s AND Age = %s"
        myCursor.execute(queryDelete, (nom, age))
        cnx.commit()
        print("L'employé a bien été supprimé !")
    else:
        print("Vous avez quitté l'application")
        sleep(1)
        exit()

    os.system("cls")
    main_chef(user_state, cnx)
