# Partie Deploy
from mysql.connector import (connection)
import time
cnx = connection.MySQLConnection(user='admin', password='admin',
                                 host='127.0.0.1',
                                 database='camping_physique')
print("Connection ok")


def main():
    print("Bienvenue sur notre API Camping. Vous pouvez quitter à nimporte quel moment en tapant '/exit'")
    Authorized = login()
    if Authorized != False:
        Operation = input("Que voulez-vous faire ?")
    print("Hate de vous revoir prochainement")
    return False


def login():
    Connexion_type = "nothing"
    Authorized = False
    while Connexion_type != "/login" or Connexion_type != "/register" or Connexion_type != "/exit":
        Connexion_type = input(
            "Entrez '/login'.\nVous n'avez pas de compte ? Entrez '/register'")
        time.sleep(1)
    if Connexion_type == "/login":
        while Authorized != True or Authorized != "Admin":
            cursorLogin = cnx.cursor()
            UserName = input("Entrez votre nom de famille")
            Password = input("Entrez votre mot de passe")
            queryLogin = ("SELECT UserName, Password FROM PERSONNE")
            cursorLogin.execute(queryLogin)
            if cursorLogin == []:
                print("Mauvais mot de passe ou nom. Veuillez réessayer")
                Authorized = False
            else:
                print("Vous êtes connectés !")
                Authorized = True
    elif Connexion_type == "/register":
        myCursor = cnx.cursor()
        UserName = input("Quel est votre nom ?")
        UserSurname = input("Quel est votre.vos prénom.s ?")
        UserSurnameList = UserSurname.split(" ")
        UserAge = input("Quel est votre âge ?")
        while UserRole != "STAFF" or UserRole != "CLIENT":
            UserRole = input("Quel est votre rôle (STAFF ou CLIENT) ?")
        Password = input("Entrez votre mot de passe ?")
        if UserRole == "STAFF":
            queryUser = ("INSERT INTO (Nom, Age, STAFF, CLIENT, Mot_de_passe) VALUES({}, {}, 1, 0, {})". format(
                UserName, UserAge, Password))
        else:
            queryUser = ("INSERT INTO (Nom, Age, STAFF, CLIENT, Mot_de_passe) VALUES({}, {}, 0, 1, {})". format(
                UserName, UserAge, UserRole, Password))
        myCursor.execute(queryUser)
        cnx.commit()
        for name in UserSurnameList:
            querySurname = (
                "INSERT INTO Prenom (Prenom) VALUES({}, {})".format(name))
            myCursor.execute(querySurname)
            cnx.commit()

        Authorized = True
    else:
        return False
    return Authorized


main()
