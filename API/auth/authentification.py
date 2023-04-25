from auth.hash import hash_password, verify_password
from time import sleep
from mysql.connector import (connection)


def login(cnx):
    Connexion_type = "nothing"
    Authorized = False
    while Connexion_type not in ("login", "register", "exit"):
        Connexion_type = input(
            "Entrez 'login'.Vous n'avez pas de compte ? Entrez 'register'\n")
        sleep(1)
    if Connexion_type == "login":
        while Authorized != True or Authorized != "Admin":
            myCursor = cnx.cursor()
            UserName = input("Entrez votre nom de famille")
            PasswordLogin = input("Entrez votre mot de passe")
            queryLogin = (
                "SELECT Mot_de_passe FROM PERSONNE WHERE Nom = {}".format(UserName))
            myCursor.execute(queryLogin)
            resolve = verify_password(PasswordLogin, myCursor)
            if not resolve:
                print("Mauvais mot de passe ou nom. Veuillez réessayer")
                Authorized = False
            else:
                print("Vous êtes connectés !")
                Authorized = True

    elif Connexion_type == "register":
        myCursor = cnx.cursor()
        UserName = input("Quel est votre nom ? ")
        UserSurname = input("Quel est votre.vos prénom.s ? ")
        UserSurnameList = UserSurname.split(" ")
        UserAge = input("Quel est votre âge ? ")
        UserRole = input("Quel est votre rôle (STAFF ou CLIENT) ? ")
        while UserRole not in ("STAFF", "CLIENT"):
            UserRole = input("Quel est votre rôle (STAFF ou CLIENT) ? ")
        Password = input("Entrez votre mot de passe ? ")
        HashToSend = hash_password(Password)

        queryUser = ("INSERT INTO PERSONNE (Nom, Age, Mot_de_passe) VALUES({}, {}, {})". format(
            UserName, int(UserAge), HashToSend))
        myCursor.execute(queryUser)
        cnx.commit()
        # on récupère l'id du client que l'on vient de créer
        queryId = ("SELECT Id_pers FROM PERSONNE WHERE Nom = {}".format(UserName))
        myCursor.execute(queryId)

        for name in UserSurnameList:
            querySurname = (
                "INSERT INTO Prenom (id, Prenom) VALUES({}, {})".format(myCursor, name))
            myCursor.execute(querySurname)
            cnx.commit()

        myCursor = cnx.cursor()
        # On le met dans la table client
        if UserRole == "CLIENT":
            queryRole = ("INSERT INTO CLIENT (Id) VALUES({})".format(myCursor))
        else:
            queryRole = ("INSERT INTO STAFF (Id) VALUES({})".format(myCursor))
        myCursor.execute(queryRole)
        cnx.commit()

        Authorized = True
    else:
        return False
    return Authorized
