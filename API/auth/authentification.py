from auth.hash import hash_password, verify_password
from time import sleep
from mysql.connector import (connection)
import os


def main_auth(cnx):
    """
    Cette fonction apelle les fonctions login et register en fonction de la demande de l'utilisateur.

    Parameters:
    ----------
    cnx : mysql.connector.connection_cext.CMySQLConnection (Object)

    Returns:
    --------
    Authorized : Il contient les variables suivantes :
    chef_state : True si l'utilisateur est un chef, False sinon (bool)
    user_state : le job de l'utilisateur (str)
    Id_Pers : L'id de l'utilisateur dans la base de données(table PERSONNE) (int)
    """
    Connexion_type = "nothing"
    while Connexion_type not in ("login", "register", "exit"):
        Connexion_type = input(
            "Entrez 'login'.Vous n'avez pas de compte ? Entrez 'register'\n")
        sleep(1)
    if Connexion_type == "login":
        chef_state, user_state, Id_Pers = login(cnx, Authorized=False)
    elif Connexion_type == "register":
        register(cnx)
    else:
        print("\nVous avez quitté l'application")
        sleep(1)
        exit()
    return chef_state, user_state, Id_Pers


def login(cnx, Authorized):
    """
    Permet à l'utilisateur de se connecter à l'application.

    Parameters:
    ----------
    cnx : mysql.connector.connection_cext.CMySQLConnection (Object)

    Returns:
    --------
    Authorized : Il contient les variables suivantes :
    chef_state : True si l'utilisateur est un chef, False sinon (bool)
    user_state : le job de l'utilisateur (str)
    Id_Pers : L'id de l'utilisateur dans la base de données(table PERSONNE) (int)
    """
    while Authorized != True:

        myCursor = cnx.cursor(prepared=True)
        # On crée une liste contenant le nom et l'age de l'utilisateur
        UserInfosListe = []
        PasswordLogin = ""
        UserInfosListe = input(
            "\nEntrez maintenant votre nom et votre age séparé par un espace afin de vous connecter\n").split(" ")
        PasswordLogin = input(
            "Entrez votre mot de passe\nMot de pass oublié ? Tapez 1\n")

        if UserInfosListe[0] == "exit" or PasswordLogin == "exit":
            print("Vous avez quitté l'application")
            sleep(1)
            exit()

        if PasswordLogin == "1":
            # On appelle la fonction reset_mdp
            reset_mdp(cnx, UserInfosListe)

        if len(UserInfosListe) != 2:
            # On recommence la boucle si l'utilisateur n'a pas rentré le bon nombre d'arguments
            login(cnx, Authorized)

        # On vérifie si l'utilisateur a rentré le bon nom et le bon âge
        queryInfos = "SELECT Nom, Age FROM PERSONNE WHERE Nom = %s AND Age = %s"
        myCursor.execute(queryInfos, (UserInfosListe[0], UserInfosListe[1]))
        test = myCursor.fetchall()
        if test == []:
            print("Mauvais nom ou mauvais age. Veuillez réessayer")
            Authorized = False
            return login(cnx, Authorized)

        myCursor = cnx.cursor(prepared=True)
        queryLogin = "SELECT Mot_de_passe FROM PERSONNE WHERE Nom = %s AND Age = %s"
        myCursor.execute(queryLogin, (UserInfosListe[0], UserInfosListe[1]))
        HashPassword = myCursor.fetchall()

        # On compare le password hashé au password entré par l'utilisateur
        resolve = verify_password(PasswordLogin, HashPassword)
        if not resolve:
            print("Mauvais mot de passe. Veuillez réessayer")
            Authorized = False
        else:
            print("Vous êtes connectés !")
            Authorized = True

    myCursor = cnx.cursor(prepared=True)
    queryId = "SELECT Id_Pers FROM PERSONNE WHERE Nom = %s  AND Age = %s"
    myCursor.execute(queryId, (UserInfosListe[0], UserInfosListe[1]))

    # On récupère l'Id_Pers de l'utilisateur que l'on met dans une variable
    Id_Pers = myCursor.fetchall()[0][0]

    chef_state = False
    user_state = "CLIENT"

    # On récupère Prix_chef si celui-ci est nul alors l'utilisateur n'est pas un chef
    queryChef = "SELECT Prix_chef FROM STAFF WHERE Id_Pers = %s"
    myCursor.execute(queryChef, (Id_Pers,))
    test = myCursor.fetchall()

    # On vérifie si l'utilisateur est un client ou un staff puis on vérifie si ce staff est chef ou non
    if test == []:
        return chef_state, user_state, Id_Pers
    else:
        Prix_chef = test[0][0]
        if Prix_chef != None:
            chef_state = True

    # on récupère l'IdStaff de l'utilisateur
    queryIdStaff = "SELECT Id_staff FROM STAFF WHERE Id_Pers = %s"
    myCursor.execute(queryIdStaff, (Id_Pers,))
    if myCursor.with_rows:
        IdStaff = myCursor.fetchall()[0][0]
        # On vérifie si l'utilisateur est un admin, un cuisinier, un animateur ou un technicien

        queryAdmin = "SELECT Id_staff FROM STAFF WHERE Id_staff = %s AND Id_staff in (SELECT Id_staff FROM ADMINISTRATION)"

        queryCuisinier = "SELECT Id_staff FROM STAFF WHERE Id_staff = %s AND Id_staff in (SELECT Id_staff FROM CUISINIER)"

        queryAnimateur = "SELECT Id_staff FROM STAFF WHERE Id_staff = %s AND Id_staff in (SELECT Id_staff FROM ANIMATEUR)"

        queryTechnicien = "SELECT Id_staff FROM STAFF WHERE Id_staff = %s AND Id_staff in (SELECT Id_staff FROM TECHNICIEN)"

        # Si la query Admin n'est pas vide alors l'utilisateur est un admin
        myCursor.execute(queryAdmin, (IdStaff,))
        myCursor.fetchall()
        if myCursor.rowcount != 0:
            user_state = "ADMINISTRATION"

        # Si la query Cuisinier n'est pas vide alors l'utilisateur est un cuisinier
        myCursor.execute(queryCuisinier, (IdStaff,))
        myCursor.fetchall()
        if myCursor.rowcount != 0:
            user_state = "CUISINIER"

        # Si la query Animateur n'est pas vide alors l'utilisateur est un animateur
        myCursor.execute(queryAnimateur, (IdStaff,))
        myCursor.fetchall()
        if myCursor.rowcount != 0:
            user_state = "ANIMATEUR"

        # Si la query Technicien n'est pas vide alors l'utilisateur est un technicien
        myCursor.execute(queryTechnicien, (IdStaff,))
        myCursor.fetchall()
        if myCursor.rowcount != 0:
            user_state = "TECHNICIEN"

    return chef_state, user_state, Id_Pers


def register(cnx):
    """
    Permet à l'utilisateur de s'inscrire à l'application en tant que Client ou membre du staff.

    Parameters:
    ----------
    cnx : mysql.connector.connection_cext.CMySQLConnection (Object)
    """
    myCursor = cnx.cursor(prepared=True)
    UserName = input("Quel est votre nom ? ")
    UserSurname = input("Quel est votre.vos prénom.s ? ")
    UserSurnameList = UserSurname.split(" ")
    UserAge = input("Quel est votre âge ? ")
    UserRole = input("Quel est votre rôle (STAFF ou CLIENT) ? ")
    while UserRole not in ("STAFF", "CLIENT", "exit"):
        UserRole = input("Quel est votre rôle (STAFF ou CLIENT) ? ")
    Password = input("Entrez votre mot de passe ? ")

    if UserName == "exit" or UserSurname == "exit" or UserAge == "exit" or UserRole == "exit" or Password == "exit":
        print("Vous avez quitté l'application")
        sleep(1)
        exit()
    # On hash le mot de passe
    HashToSend = hash_password(Password)

    queryUser = "INSERT INTO PERSONNE (Nom, Age, Mot_de_passe) VALUES(%s, %s, %s)"
    myCursor.execute(queryUser, (UserName, int(UserAge), HashToSend))
    cnx.commit()
    # on récupère l'id du client que l'on vient de créer
    queryId = "SELECT Id_Pers FROM PERSONNE WHERE Nom = %s AND  Age = %s AND Mot_de_passe = %s"
    myCursor.execute(queryId, (UserName, int(UserAge), HashToSend))
    myCursor.fetchall()

    MyCursorName = cnx.cursor(prepared=True)
    # On insère tous les prénoms du Client dans la table Prenom
    for name in UserSurnameList:
        querySurname = "INSERT INTO Prenom (Id_Pers, Prenom) VALUES(%s, %s)"
        MyCursorName.execute(querySurname, (myCursor.lastrowid, name))
        cnx.commit()

    # On le met dans la table client
    if UserRole == "CLIENT":
        userRegister(cnx, myCursor)

    # Ou dans la table STAFF
    else:
        staffRegister(cnx, myCursor)


def userRegister(cnx, myCursor):
    """
    Permet à un client d'enregistrer ses informations suplémentaires.

    Parameters:
    ----------
    cnx : mysql.connector.connection_cext.CMySQLConnection (Object)
    myCursor : mysql.connector.connection_cext.CPreparedMySQLConnection (sa lastrowid contient celle du client enregistré précédemmment donc elle nous sera utile) (Object)
    """
    Cursor = cnx.cursor(prepared=True)
    print("Vous vous êtes enregistré en tant que client dans notre camping veuillez entrer ces informations supplémentaires :\nPS : La commande exit ne fonctionne pas dans cette section.")
    UserCountry = input("De quel pays venez vous ? ")
    UserCP = input("Quel est votre code postal ? ")
    UserCity = input("Quel est votre ville ? ")
    UserHouseNumber = input("Quel est votre numéro de maison ? ")
    UserPhone = input("Quel est votre numéro de téléphone ? ")
    UserMail = input("Quel est votre adresse mail ? ")

    queryCli = "INSERT INTO CLIENT (Id_Pers, Pays, Code_postal, Ville, Numero_de_maison, Con_telephone, Con_Email) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    Cursor.execute(queryCli, (myCursor.lastrowid, UserCountry,
                   UserCP, UserCity, UserHouseNumber, UserPhone, UserMail))
    cnx.commit()
    print("\nVous êtes enregistré en tant que client ! Nous allons maintenant vous rediriger pour que vous puissiez vous connecter où réenregistrer un compte.")
    main_auth(cnx)


def staffRegister(cnx, myCursor):
    """
    Permet à un staff d'enregistrer ses informations suplémentaires.

    Parameters:
    ----------
    cnx : mysql.connector.connection_cext.CMySQLConnection (Object)
    myCursor : mysql.connector.connection_cext.CPreparedMySQLConnection (sa lastrowid contient celle du staff enregistré précédemmment donc elle nous sera utile) (Object)
    """

    UserJob = "nothing"
    print("\nVous vous êtes enregistré en tant que staff dans notre camping veuillez entrer ces informations supplémentaires :\nPS : La commande exit ne fonctionne pas dans cette section.")
    while UserJob not in ("TECHNICIEN", "CUISINIER", "ANIMATEUR", "ADMINISTRATION"):
        UserJob = input(
            "Quel est votre métier ? (TECHNICIEN, CUISINIER, ANIMATEUR ou ADMINISTRATION) ")

    UserPrice = staffPrice(UserJob)
    # On rajoute un staff
    queryStaff = "INSERT INTO STAFF (Id_Pers, Prix) VALUES(%s, %s)"
    myCursor.execute(queryStaff, (myCursor.lastrowid, UserPrice))
    cnx.commit()

    # On récupère l'id du staff que l'on vient de créer
    queryIdStaff = "SELECT Id_staff FROM STAFF WHERE Id_Pers = %s"
    myCursor.execute(queryIdStaff, (myCursor.lastrowid,))
    myCursor.fetchall()

    # On le met dans la table correspondant à son métier
    queryJob = "INSERT INTO {} (Id_staff) VALUES({})".format(
        UserJob, myCursor.lastrowid)
    myCursor.execute(queryJob)
    cnx.commit()

    chefStaff = "Nothing"
    while chefStaff not in ("O", "N"):
        chefStaff = input("Etes-vous chef ? (O/N) ")
        if chefStaff == "O":
            queryChef = "UPDATE STAFF SET Prix_chef = '300.00' WHERE Id_staff = %s"
            myCursor.execute(queryChef, (myCursor.lastrowid,))
            cnx.commit()

    print("\nVous êtes enregistré en tant que staff ! Nous allons maintenant vous rediriger pour que vous puissiez vous connecter où réenregistrer un compte\n")
    main_auth(cnx)


def staffPrice(UserJob):
    """
    Cette fonction attribue un prix à un staff en fonction de son métier.

    Parameters:
    ----------
    UserJob : Job du staff (String)

    Returns:
    -------
    UserPrice : Prix du staff (Float)
    """
    if UserJob == "TECHNICIEN":
        UserPrice = 2000
    elif UserJob == "CUISINIER":
        UserPrice = 2200
    elif UserJob == "ANIMATEUR":
        UserPrice = 1700
    else:
        UserPrice = 3000
    return UserPrice


def reset_mdp(cnx, UserInfosListe):
    """
    Cette fonction permet de réinitialiser le mot de passe d'un utilisateur.

    Parameters:
    ----------
    cnx : mysql.connector.connection_cext.CMySQLConnection (Object)
    UserInfosListe : Liste contenant les informations de l'utilisateur (Noms et prénoms)(List)
    """
    os.system('cls')
    newPassword = "Nothing"
    newPasswordVerif = "Nothing2"
    while newPassword != newPasswordVerif:
        newPassword = input("Entrez votre nouveau mot de passe : ")
        newPasswordVerif = input("Confirmez votre nouveau mot de passe : ")

        if newPassword != newPasswordVerif:
            print("Les mots de passe ne correspondent pas !")

    newPassword = hash_password(newPassword)
    myCursor = cnx.cursor(prepared=True)
    query = "UPDATE PERSONNE SET Mot_de_passe = %s WHERE Nom = %s AND Age = %s"
    myCursor.execute(
        query, (newPassword, UserInfosListe[0], UserInfosListe[1]))
    cnx.commit()
    print("Votre mot de passe a bien été changé !")
    return login(cnx, Authorized=False)
