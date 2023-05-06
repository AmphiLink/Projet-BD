from time import sleep
import os


def main_animateur(cnx, Id_Pers):
    """
    Cette fonction permet d'utiliser les différentes fonctionnnalités de l'application en tant qu'animateur.

    Parameters:
    -----------
    cnx : mysql.connector.connection.MySQLConnection (Object)
    Id_Pers : l'Id de la personne conectée (int)
    """

    choix = "basic"
    while choix not in ("liste_activités", "rajouter une compétence", "Rajouter une animation", "profil", "exit"):
        choix = input(
            "Que voulez vous faire ? (liste_activités, rajouter une compétence, rajouter une animation, profil, exit) ")
        sleep(1)

    if choix == "liste_activités":
        liste_activités(cnx)
    elif choix == "rajouter une compétence":
        os.system("cls")
        print("Choisissez une compétence à rajouter en tapant le numéro correspondant : ")
        NewJob = input(
            "1 : Basketball 6 : Ski-nautique\n2 : Football   7 : Escalade\n3 :Badminton  8 : Mini-Golf\n4 : Volleyball 9 : Club enfants\n5 : Spa        10 : Plongée\n")

        if NewJob == "exit":
            print("Vous avez quitté l'application")
            sleep(1)
            exit()
        myCursor = cnx.cursor(prepared=True)
        # On récupère l'IdStaff
        queryIdStaff = "Select Id_staff FROM STAFF where Id_Pers = %s"
        myCursor.execute(queryIdStaff, (Id_Pers,))
        Id_staff = myCursor.fetchall()[0][0]
        # On récupère l'Idanim
        queryIdanim = "SELECT Id_anim FROM ANIMATEUR WHERE Id_staff = %s"
        myCursor.execute(queryIdanim, (Id_staff,))
        Id_anim = myCursor.fetchall()[0][0]
        # On insère dans la table peut_faire
        queryAdd = "INSERT INTO peut_faire (Id_anim, Id_type_acti) VALUES (%s, %s)"
        myCursor.execute(queryAdd, (Id_anim, NewJob))
        cnx.commit()
    elif choix == "Rajouter une animation":
        myCursor = cnx.cursor(prepared=True)
        os.system("cls")
        print("Choisissez une animation à rajouter en tapant le numéro correspondant : ")
        Id_type_acti = input(
            "1 : Basketball 6 : Ski-nautique\n2 : Football   7 : Escalade\n3 :Badminton  8 : Mini-Golf\n4 : Volleyball 9 : Club enfants\n5 : Spa        10 : Plongée\n")
        Date_acti = input("\nDate de l'animation (AAAA-MM-JJ) ?\n")
        Heure = input("\nHeure de l'animation (HH:MM) ?\n")
        Lieu = input("\nLieu de l'animation ?\n")

        if Id_type_acti == "exit" or Date_acti == "exit" or Heure == "exit" or Lieu == "exit":
            print("Vous avez quitté l'application")
            sleep(1)
            exit()

        # On récupère l'IdStaff
        queryIdStaff = "Select Id_staff FROM STAFF where Id_Pers = %s"
        myCursor.execute(queryIdStaff, (Id_Pers,))
        Id_staff = myCursor.fetchall()[0][0]
        # On récupère l'Idanim
        queryIdanim = "SELECT Id_anim FROM ANIMATEUR WHERE Id_staff = %s"
        myCursor.execute(queryIdanim, (Id_staff,))
        Id_anim = myCursor.fetchall()[0][0]
        # On insère les donnees
        # C'est également ici que se déclenchera notre trigger si l'animateur n'est pas en capacité d'animer l'activité
        queryAddActi = "INSERT INTO ACTIVITE (Date_acti, Heure, Lieu, Id_type_acti, Id_anim) VALUES (%s, %s, %s, %s, %s)"
        myCursor.execute(queryAddActi, (Date_acti, Heure,
                         Lieu, Id_type_acti, Id_anim))
    else:
        print("Vous avez quitté l'application")
        sleep(1)
        exit()


def liste_activités(cnx):
    # Encore à tester et commenter
    myCursor = cnx.cursor(prepared=True)
    queryList = "SELECT Id_type_acti, Nom, Prix, Taille_min_, Age_min FROM TYPE_ACTI"
    myCursor.execute(queryList)
    for Id_type_acti, Nom, Prix, Taille_min_, Age_min in myCursor:
        print("%s :  %s, Prix : %s, Taille_min : %s, Age_min :  %s" %
              (Id_type_acti, Nom, Prix, Taille_min_, Age_min))
