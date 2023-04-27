from auth.hash import hash_password, verify_password
from time import sleep
from mysql.connector import (connection)


def main_auth(cnx, Authorized):
    Connexion_type = "nothing"
    while Connexion_type not in ("login", "register", "exit"):
        Connexion_type = input(
            "Entrez 'login'.Vous n'avez pas de compte ? Entrez 'register'\n")
        sleep(1)
    if Connexion_type == "login":
        Authorized = login(cnx, Authorized)
    elif Connexion_type == "register":
        register(cnx, Authorized)
    else:
        print("\nVous avez quitté l'application")
        sleep(1)
        exit()
    return Authorized


def login(cnx, Authorized):
    while Authorized != True:
        myCursor = cnx.cursor()
        # On crée une liste contenant le nom et l'age de l'utilisateur

        UserInfosListe = input(
            "Entrez maintenant votre nom et votre age séparé par un espace afin de vous connecter\n").split(" ")
        PasswordLogin = input("Entrez votre mot de passe ")

        # On teste le mot de passe rentré par cet utilisateur
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

    queryId = ("SELECT Id_Pers FROM PERSONNE WHERE Nom = '{}' AND Age = '{}'".format(
        UserInfosListe[0], UserInfosListe[1]))
    myCursor.execute(queryId)
    myCursor.fetchall()

    chef_state = False
    user_state = "Client"

    # On récupère Prix_chef si celui-ci est nul alors l'utilisateur n'est pas un chef
    queryChef = ("SELECT Prix_chef FROM STAFF WHERE Id_Pers = '{}'".format(
        myCursor.lastrowid))
    myCursor.execute(queryChef)
    myCursor.fetchall()

    # On vérifie si Prix_chef n'est pas nul
    if myCursor.rowcount != 0:
        chef_state = True

    # on récupère l'IdStaff de l'utilisateur
    myCursor.execute(queryId)
    myCursor.fetchall()
    # On récupère le rôle de l'utilisateur
    queryIdStaff = (
        "SELECT Id_staff FROM STAFF WHERE Id_Pers = '{}'".format(myCursor.lastrowid))
    myCursor.execute(queryIdStaff)
    myCursor.fetchall()
    queryAdmin = ("SELECT Id_staff FROM STAFF WHERE Id_staff = '{}' AND Id_staff in (SELECT Id_staff FROM ADMINISTRATION)".format(
        myCursor.lastrowid))
    myCursor.execute(queryIdStaff)
    myCursor.fetchall()
    queryCuisinier = (
        "SELECT Id_staff FROM STAFF WHERE Id_staff = '{}' AND Id_staff in (SELECT Id_staff FROM CUISINIER)".format(myCursor.lastrowid))
    myCursor.execute(queryIdStaff)
    myCursor.fetchall()
    queryAnimateur = (
        "SELECT Id_staff FROM STAFF WHERE Id_staff = '{}' AND Id_staff in (SELECT Id_staff FROM ANIMATEUR)".format(myCursor.lastrowid))
    myCursor.execute(queryIdStaff)
    myCursor.fetchall()
    queryTechnicien = (
        "SELECT Id_staff FROM STAFF WHERE Id_staff = '{}' AND Id_staff in (SELECT Id_staff FROM TECHNICIEN)".format(myCursor.lastrowid))

    myCursor.execute(queryAdmin)
    myCursor.fetchall()
    if myCursor.rowcount != 0:
        user_state = "Admin"

    myCursor.execute(queryCuisinier)
    myCursor.fetchall()
    if myCursor.rowcount != 0:
        user_state = "Cuisinier"

    myCursor.execute(queryAnimateur)
    myCursor.fetchall()
    if myCursor.rowcount != 0:
        user_state = "Animateur"

    myCursor.execute(queryTechnicien)
    myCursor.fetchall()
    if myCursor.rowcount != 0:
        user_state = "Technicien"

    return chef_state, user_state


def register(cnx, Authorized):
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
        userRegister(cnx, myCursor, Authorized)
    else:
        staffRegister(cnx, myCursor, Authorized)


def userRegister(cnx, myCursor, Authorized):
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
    main_auth(cnx, Authorized)


def staffRegister(cnx, myCursor, Authorized):
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

    # On rajoute un staff
    queryStaff = ("INSERT INTO STAFF (Id_Pers, Prix) VALUES('{}', '{}')".format(
        myCursor.lastrowid, UserPrice))
    myCursor.execute(queryStaff)
    cnx.commit()

    # On récupère l'id du staff que l'on vient de créer
    queryIdStaff = (
        "SELECT Id_staff FROM STAFF WHERE Id_Pers = '{}'".format(myCursor.lastrowid))
    myCursor.execute(queryIdStaff)
    myCursor.fetchall()

    # On le met dans la table correspondant à son métier
    queryJob = ("INSERT INTO {} (Id_staff) VALUES('{}')".format(
        UserJob, myCursor.lastrowid))
    myCursor.execute(queryJob)
    cnx.commit()

    # On lui demande si il est chef et on récupère de nouveau l'id_staff dans notre curseur
    myCursor.execute(queryIdStaff)
    myCursor.fetchall()

    chefStaff = "Nothing"
    while chefStaff not in ("O", "N"):
        chefStaff = input("Etes-vous chef ? (O/N) ")
        if chefStaff == "O":
            queryChef = (
                "UPDATE STAFF SET Prix_chef = '300.00' WHERE Id_staff = '{}'".format(myCursor.lastrowid))
            myCursor.execute(queryChef)
            cnx.commit()

    print("\nVous êtes enregistré en tant que staff ! Nous allons maintenant vous rediriger pour que vous puissiez vous connecter où réenregistrer un compte\n")
    main_auth(cnx, Authorized)
