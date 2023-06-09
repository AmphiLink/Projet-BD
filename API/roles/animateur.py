from time import sleep
import os
import mysql.connector


def main_animateur(cnx, Id_Pers):
    """
    Cette fonction permet d'utiliser les différentes fonctionnnalités de l'application en tant qu'animateur.

    Parameters:
    -----------
    cnx : mysql.connector.connection.MySQLConnection (Object)
    Id_Pers : l'Id de la personne conectée (int)
    """
    os.system("cls")
    choix = "basic"
    while choix not in ("liste_activités", "rajouter une compétence", "rajouter une animation", "gérer une animation", "profil", "exit", "1", "2", "3", "4", "5", "6"):
        choix = input(
            "Que voulez vous faire ?\n\n1: liste_activités\n2: rajouter une compétence\n3: rajouter une animation\n4: gérer une animation\n5: profil\n6: exit\n")
        os.system("cls")
        sleep(1)

    myCursor = cnx.cursor(prepared=True)
    # On récupère l'IdStaff
    queryIdStaff = "SELECT Id_staff FROM STAFF WHERE Id_Pers = %s"
    myCursor.execute(queryIdStaff, (Id_Pers,))
    Id_staff = myCursor.fetchall()[0][0]
    # On récupère l'Idanim
    queryIdanim = "SELECT Id_anim FROM ANIMATEUR WHERE Id_staff = %s"
    myCursor.execute(queryIdanim, (Id_staff,))
    Id_anim = myCursor.fetchall()[0][0]

    if choix == "liste_activités" or choix == "1":
        liste_activités(cnx, Id_Pers)
        main_animateur(cnx, Id_Pers)
    elif choix == "rajouter une compétence" or choix == "2":
        os.system("cls")
        NewJob = ""
        print("Choisissez une compétence à rajouter en tapant le numéro correspondant : ")
        while NewJob not in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "exit"):
            NewJob = input(
                "\n1 : Basketball  6 : Ski-nautique\n2 : Football    7 : Escalade\n3 : Badminton   8 : Mini-Golf\n4 : Volleyball  9 : Club enfants\n5 : Spa         10 : Plongée\n")

        if NewJob == "exit":
            print("Vous avez quitté l'application")
            sleep(1)
            exit()
        myCursor = cnx.cursor(prepared=True)
        # On insère dans la table peut_faire
        queryAdd = "INSERT INTO peut_faire (Id_anim, Id_type_acti) VALUES (%s, %s)"
        myCursor.execute(queryAdd, (Id_anim, NewJob))
        cnx.commit()
        print("Compétence ajoutée !")
        sleep(2)
        main_animateur(cnx, Id_Pers)

    elif choix == "rajouter une animation" or choix == "3":
        myCursor = cnx.cursor(prepared=True)
        os.system("cls")
        print("Choisissez une animation à rajouter en tapant le numéro correspondant : ")
        Id_type_acti = input(
            "\n1 : Basketball  6 : Ski-nautique\n2 : Football    7 : Escalade\n3 : Badminton   8 : Mini-Golf\n4 : Volleyball  9 : Club enfants\n5 : Spa         10 : Plongée\n")
        Date_acti = input("\nDate de l'animation (AAAA-MM-JJ) ? ")
        Heure = input("\nHeure de l'animation (HH:MM) ? ")
        Lieu = input("\nLieu de l'animation ? ")

        if Id_type_acti == "exit" or Date_acti == "exit" or Heure == "exit" or Lieu == "exit":
            print("Vous avez quitté l'application")
            sleep(1)
            exit()
        # On insère les donnees
        queryAddActi = "INSERT INTO ACTIVITE (Date_acti, Heure, Lieu, Id_type_acti, Id_anim) VALUES (%s, %s, %s, %s, %s)"
        myCursor.execute(queryAddActi, (Date_acti, Heure,
                         Lieu, Id_type_acti, Id_anim))
        print("Compétence ajoutée !")
        sleep(2)
        main_animateur(cnx, Id_Pers)

    elif choix == "gérer une animation " or choix == "4":
        myCursor = cnx.cursor(prepared=True)
        os.system("cls")
        print("Voici les activités à animer disponibles :\n")
        queryList = "SELECT Id_acti, Date_acti, Heure, Lieu, TA.Nom, A.Id_type_acti FROM ACTIVITE A, TYPE_ACTI TA WHERE A.Id_type_acti = TA.Id_type_acti AND Id_anim is null"
        myCursor.execute(queryList)
        ma_liste = []
        ActiGestion = ""
        # On affiche les activités disponibles
        for Id_acti, Date_acti, Heure, Lieu, Nom, Id_type_acti in myCursor:
            print("%s : Date : %s, Heure : %s, Lieu :  %s, Activité : %s\n" %
                  (Id_acti, Date_acti, Heure, Lieu, Nom))
            ma_liste.append(Id_acti)
        myCursor.fetchall()
        while ActiGestion not in ma_liste:
            ActiGestion = input(
                "Choisissez une animation à gérer en tapant le numéro d'identification de l'animation :\n")
            # On cast ActiGestion en int
            ActiGestion = int(ActiGestion)

        # On rajoute l'Id_anim dans la table ACTIVITE
        try:
            queryUpdate = "UPDATE ACTIVITE SET Id_anim = %s WHERE Id_acti = %s"
            myCursor.execute(queryUpdate, (Id_anim, ActiGestion))
            cnx.commit()
            print("Animation rajoutée !")
            sleep(2)
        except mysql.connector.Error as err:
            # Récupérez le code d'erreur et le message
            error_message = err.msg
            print("{}".format(error_message))
            sleep(2)
        main_animateur(cnx, Id_Pers)

    elif choix == "profil" or choix == "5":
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

        queryInfos = "SELECT Id_staff, Nom, Age, Salaire, Date_acti, Heure, Lieu, Id_type_acti, Activite, Prix_acti, Taille_min_, Age_min FROM view_Animateur_Activite WHERE Id_staff = %s"
        myCursor.execute(queryInfos, (Id_staff,))

        verif = 0
        for Id_staff, Nom, Age, Salaire, Date, Heure, Lieu, Id_type_acti, NomActi, Prix, Taille_min_, Age_min in myCursor:
            if verif == 0:
                print("Id : %s\nNom : %s" % (Id_staff, Nom))
                # On affiche les prénoms stockés dans la liste prenomsListe en ligne
                print("Prénom(s) : %s" % (", ".join(prenomsListe)))
                print("Age : %s\nSalaire : %s \u20ac" % (Age, Salaire))
                print("\nVos activités : \n=========================")
            if verif == 1:
                print("\n=========================")
            if Date == None:
                print("Vous n'avez pas d'activité prévue")
            else:
                print("Date : %s\nHeure : %s\nLieu : %s\nActivité : %s\nPrix : %s \u20ac\nTaille minimum : %s cm\nAge minimum : %s ans\n" % (
                    Date, Heure, Lieu, NomActi, Prix, Taille_min_, Age_min))

            verif = 1

        myCursor.fetchall()
        queryCompetences = "SELECT Id_type_acti, Activite, Prix_acti, Taille_min_, Age_min FROM view_Animateur_PossibleActivite WHERE Id_staff = %s"
        myCursor.execute(queryCompetences, (Id_staff,))
        print("\nActivités que vous pouvez animer : \n=========================")
        for Id_type_acti, Activite, Prix_acti, Taille_min_, Age_min in myCursor:
            if Id_type_acti == None:
                print("Vous n'avez pas de compétences")
            else:
                print("Activité : %s\nPrix : %s \u20ac\nTaille minimum : %s cm\nAge minimum : %s ans\n" % (
                    Activite, Prix_acti, Taille_min_, Age_min))
        a = input("\nAppuyez sur une enter pour continuer")
        if a == "":
            os.system("cls")
            main_animateur(cnx, Id_Pers)

    else:
        print("Vous avez quitté l'application")
        sleep(1)
        exit()


def liste_activités(cnx, Id_Pers):
    """
    Cette fonction permet d'afficher la liste des activités disponibles.

    Parameters:
    -----------
    cnx : mysql.connector.connection.MySQLConnection (Object)
    """
    myCursor = cnx.cursor(prepared=True)
    queryList = "SELECT Id_type_acti, Nom, Prix, Taille_min_, Age_min FROM TYPE_ACTI"
    myCursor.execute(queryList)
    # On récupère les données et on les affiche
    for Id_type_acti, Nom, Prix, Taille_min_, Age_min in myCursor:
        print("%s : %s\nPrix : %s\nTaille minimum : %s\nAge minimum : %s\n" %
              (Id_type_acti, Nom, Prix, Taille_min_, Age_min))
    myCursor.fetchall()
    sleep(4)
