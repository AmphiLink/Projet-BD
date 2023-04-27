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
        while Authorized != True:
            myCursor = cnx.cursor()
            UserInfosListe = input(
                "Entrez maintenant votre nom et votre age séparé par un espace afin de vous connecter\n").split(" ")
            PasswordLogin = input("Entrez votre mot de passe ")
            queryLogin = (
                "SELECT Mot_de_passe FROM PERSONNE WHERE Nom = '{}' AND Age = '{}'".format(UserInfosListe[0], UserInfosListe[1]))
            myCursor.execute(queryLogin)
            resolve = verify_password(PasswordLogin, myCursor.fetchall())
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

        queryUser = ("INSERT INTO PERSONNE (Nom, Age, Mot_de_passe) VALUES('{}', '{}', '{}')". format(
            UserName, int(UserAge), HashToSend))
        myCursor.execute(queryUser)
        cnx.commit()
        # on récupère l'id du client que l'on vient de créer
        queryId = (
            "SELECT Id_Pers FROM PERSONNE WHERE Nom = '{}' AND  Age = '{}' AND Mot_de_passe = '{}'".format(UserName, int(UserAge), HashToSend))
        myCursor.execute(queryId)
        myCursor.fetchall()

        MyCursorName = cnx.cursor()
        for name in UserSurnameList:
            querySurname = (
                "INSERT INTO Prenom (Id_Pers, Prenom) VALUES('{}', '{}')".format(myCursor.lastrowid, name))
            MyCursorName.execute(querySurname)
            cnx.commit()

        # On le met dans la table client
        if UserRole == "CLIENT":
            userRegister(cnx, myCursor)
        else:
            staffRegister(cnx, myCursor)

        Authorized = True
    else:
        return 0
    return Authorized


def userRegister(cnx, myCursor):
    Cursor = cnx.cursor()
    print("Vous vous êtes enregistré en tant que client dans notre camping veuillez entrer ces informations supplémentaires :")
    UserCountry = input("De quel pays venez vous ? ")
    UserCP = input("Quel est votre code postal ? ")
    UserCity = input("Quel est votre ville ? ")
    UserHouseNumber = input("Quel est votre numéro de maison ? ")
    UserPhone = input("Quel est votre numéro de téléphone ? ")
    UserMail = input("Quel est votre adresse mail ? ")
    queryCli = ("INSERT INTO CLIENT (Id_Pers, Pays, Code_postal, Ville, Numero_de_maison, Con_telephone, Con_Email) VALUES('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
        myCursor.lastrowid, UserCountry, UserCP, UserCity, UserHouseNumber, UserPhone, UserMail))
    Cursor.execute(queryCli)
    cnx.commit()
    print("\nVous êtes enregistré en tant que client ! Nous allons maintenant vous rediriger pour que vous puissiez vous connecter où réenregistrer un compte")
    login(cnx)


def staffRegister(cnx, myCursor):
    UserJob = "nothing"
    print("\nVous vous êtes enregistré en tant que staff dans notre camping veuillez entrer ces informations supplémentaires :\n")
    while UserJob not in ("TECHNICIEN", "CUISINIER", "ANIMATEUR", "ADMINISTRATION"):
        UserJob = input(
            "Quel est votre métier ? (TECHNICIEN, CUISINIER, ANIMATEUR ou ADMINISTRATION) ")
    if UserJob == "TECHNICIEN":
        UserPrice = 2000
    elif UserJob == "CUISINIER":
        UserPrice = 2200
    elif UserJob == "ANIMATEUR":
        UserPrice = 1700
    else:
        UserPrice = 3000
    queryStaff = ("INSERT INTO STAFF (Id_Pers, Prix) VALUES('{}', '{}')".format(
        myCursor.lastrowid, UserPrice))
    myCursor.execute(queryStaff)
    cnx.commit()
    queryIdStaff = (
        "SELECT Id_staff FROM STAFF WHERE Id_Pers = '{}'".format(myCursor.lastrowid))
    myCursor.execute(queryIdStaff)
    myCursor.fetchall()
    queryJob = ("INSERT INTO {} (Id_staff) VALUES('{}')".format(
        UserJob, myCursor.lastrowid))
    myCursor.execute(queryJob)
    cnx.commit()
    print("\nVous êtes enregistré en tant que staff ! Nous allons maintenant vous rediriger pour que vous puissiez vous connecter où réenregistrer un compte\n")
    login(cnx)
