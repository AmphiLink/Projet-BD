import os
from time import sleep

from roles.animateur import liste_activités


def main_client(cnx, Id_pers):
    """
    Cette fonction permet d'utiliser les différentes fonctionnnalités de l'application en tant que client.

    Parameters:
    -----------
    cnx : mysql.connector.connection.MySQLConnection (Object)
    Id_Pers : l'Id de la personne conectée (int)
    """

    choix = "basic"
    os.system("cls")
    while choix not in ("Reserver du matériel", "Louer un emplacement", "Rejoindre/Créer une équipe", "Voir la liste des activités", "S'inscrire à une activité", "profil", "exit", "1", "2", "3", "4", "5", "6", "7"):
        choix = input("\nQue voulez vous faire ?\n 1: Reservé du matériel\n 2: Loué un emplacement\n 3: Rejoindre/Créer une équipe\n 4: Voir la liste des activités\n 5: S'inscrire à une activité\n 6: profil\n 7: exit\n ")
        os.system("cls")

    myCursor = cnx.cursor(prepared=True)
    # On récupère l'IdClient
    queryIdClient = "SELECT Id_cli FROM CLIENT where Id_Pers = %s"
    myCursor.execute(queryIdClient, (Id_pers,))
    Id_client = myCursor.fetchall()[0][0]

    if choix == "Reserver du matériel" or choix == "1":
        reserve_mat(cnx, Id_pers, Id_client)

    elif choix == "Louer un emplacement" or choix == "2":
        loue_emplacement(cnx, Id_pers)

    elif choix == "Rejoindre/Créer une équipe" or choix == "3":
        rejoindre_equipe(cnx, Id_pers)

    elif choix == "Voir la liste des activités" or choix == "4":
        liste_activités(cnx)

    elif choix == "S'inscrire à une activité" or choix == "5":
        inscrire_activite(cnx, Id_pers)

    elif choix == "exit" or choix == "7":
        print("Vous avez quitté l'application !")
        sleep(1)
        exit()


def reserve_mat(cnx, Id_pers, Id_client):
    """
    Cette fonction permet de réserver du matériel.

    """
    # Si le client veut réserver du matériel
    myCursor = cnx.cursor(prepared=True)
    queryIdMateriel = "SELECT Id_mat, Nom FROM MATERIEL"
    myCursor.execute(queryIdMateriel)
    queryIdMateriel = myCursor.fetchall()
    for mat in queryIdMateriel:
        mat_list = str(mat)
        mat_list = mat_list.replace("(", "").replace(
            ")", "").replace(",", ":").replace("'", "")
        print(mat_list)
    Id_materiel = input("\nQuel matériel voulez vous réserver ? ")
    queryIdMateriel = "SELECT Id_mat FROM MATERIEL WHERE Id_mat = %s"
    myCursor.execute(queryIdMateriel, (Id_materiel,))

    if myCursor.fetchall() == []:
        print("Le matériel n'existe pas")
        sleep(10)
        main_client(cnx, Id_pers)

    Date_debut = input(
        "Quelle est la date de début de la réservation ? (AAAA-MM-JJ) ")

    if Id_materiel == "exit" or Date_debut == "exit":
        print("Vous avez quitté l'application")
        sleep(1)
        exit()

    # On récupère l'id du matériel en question
    queryIdMateriel = "SELECT Id_mat FROM MATERIEL WHERE Id_mat = %s"
    myCursor.execute(queryIdMateriel, (Id_materiel,))
    Id_materiel = myCursor.fetchall()[0][0]

    # On insert la table Reserve
    queryInsertReserve = "INSERT INTO Loue_mat (Id_cli, Id_mat, Date_loc) VALUES (%s, %s, %s)"
    myCursor.execute(queryInsertReserve, (Id_client, Id_materiel, Date_debut))
    cnx.commit()
    print("\nVous pouvez aller récupérer votre matériel !")
    sleep(3)
    main_client(cnx, Id_pers)


def loue_emplacement(cnx, Id_pers):
    """
    Cette fonction permet de louer un emplacement.

    """
    # Si le client veut louer un emplacement

    myCursor = cnx.cursor(prepared=True)
    queryIdEmplacement = "SELECT Id_emplacement, Type_emplacement FROM EMPLACEMENT"
    myCursor.execute(queryIdEmplacement)
    queryIdEmplacement = myCursor.fetchall()
    for emp in queryIdEmplacement:
        emp_list = str(emp)
        emp_list = emp_list.replace("(", "").replace(
            ")", "").replace(",", ":").replace("'", "")
        print(emp_list)
    Id_emplacement = input("\nQuel type d'emplacement voulez vous louer ? ")
    queryIdEmplacement = "SELECT Type_emplacement FROM EMPLACEMENT WHERE Id_emplacement = %s && Occupation = 0"
    myCursor.execute(queryIdEmplacement, (Id_emplacement,))

    if Id_emplacement == "exit":
        print("Vous avez quitté l'application")
        sleep(1)
        exit()

    if myCursor.fetchall() == []:
        print("Tous les emplacements sont occupés ou l'emplacement n'existe pas")
        sleep(4)
        main_client(cnx, Id_pers)

    # Obtenir plus d'informations sur l'emplacement
    querydetail = "SELECT Type_emplacement, Prix, bbq, nbr_places, acces_eau, cuisinier FROM EMPLACEMENT WHERE Id_emplacement = %s"
    myCursor.execute(querydetail, (Id_emplacement,))
    resultat = myCursor.fetchall()[0]

    type_emp = resultat[0]
    prix = resultat[1]
    bbq = resultat[2]
    nbr_place = resultat[3]
    acces_eau = resultat[4]
    cuisinier = resultat[5]

    os.system("cls")
    print("\nVoici le détail des informations de l'emplacement que vous voulez avez choisi: \n")

    if bbq == 1:
        bbq = "Oui"
    else:
        bbq = "Non"
    if acces_eau == 1:
        acces_eau = "Oui"
    else:
        acces_eau = "Non"

    print(" Id:", Id_emplacement, "\n", type_emp, "\n", "Prix:", prix, "€" "\n", "Barbecue:", bbq, "\n",
          "Nombre de place(s):", nbr_place, "\n", "Accès à l'eau:", acces_eau, "\n", "Cuisinier:", cuisinier, "\n")
    reservation = input(
        "Si vous voulez réserver cet emplacement, entrez son Id, sinon entrez 'back' pour voir les autres emplacements \n")
    os.system("cls")
    if reservation == "back":
        loue_emplacement(cnx, Id_pers)

    if reservation == "exit":
        print("Vous avez quitté l'application")
        sleep(1)
        exit()

    # On récupère l'id de l'emplacement en question
    queryIdEmplacement = "SELECT Id_emplacement FROM EMPLACEMENT WHERE Id_emplacement = %s"
    myCursor.execute(queryIdEmplacement, (reservation,))
    Id_emplacement = myCursor.fetchall()[0][0]

    Date_debut = input(
        "Quelle est la date de début de la location ? (AAAA-MM-JJ) ")
    Date_fin = input(
        "Quelle est la date de fin de la location ? (AAAA-MM-JJ) ")

    if Id_emplacement == "exit" or Date_debut == "exit":
        print("Vous avez quitté l'application")
        sleep(1)
        exit()

    # On récupère l'id de l'emplacement en question
    queryIdEmplacement = "SELECT Id_emplacement FROM EMPLACEMENT WHERE Id_emplacement = %s"
    myCursor.execute(queryIdEmplacement, (Id_emplacement,))
    Id_emplacement = myCursor.fetchall()[0][0]

    # On insert la table Reserve
    queryIdcli = "SELECT Id_cli FROM CLIENT WHERE Id_Pers = %s"
    myCursor.execute(queryIdcli, (Id_pers,))
    id_cli = myCursor.fetchall()[0][0]
    queryInsertReserve = "INSERT INTO loue_emplacement (Id_cli, Id_emplacement, Date_debut, Date_fin) VALUES (%s, %s, %s, %s)"
    myCursor.execute(queryInsertReserve,
                     (id_cli, Id_emplacement, Date_debut, Date_fin))
    cnx.commit()
    print("\nVous pouvez aller récupérer votre emplacement !")
    sleep(3)
    main_client(cnx, Id_pers)


def rejoindre_equipe(cnx, Id_pers):
    """
    Cette fonction permet de rejoindre une équipe.

    """
    # Si le client veut rejoindre une équipe
    mycursor = cnx.cursor(prepared=True)
    create_team = input("Voulez-vous créer une équipe ? (O/N) \n")
    if create_team == "Oui" or create_team == "oui" or create_team == "O" or create_team == "o":
        team_name = input("Quel est le nom de votre équipe ? \n")
        number_of_members = input(
            "Combien de membres voulez-vous dans votre équipe ? \n")
        query = "INSERT INTO EQUIPE (Nom, Nbr_pers) VALUES (%s, %s)"
        mycursor.execute(query, (team_name, number_of_members))
        cnx.commit()
        print("Votre équipe a bien été créée !")
        sleep(2)
        main_client(cnx, Id_pers)

    # Si le client ne veut pas créer d'équipe
    if create_team == "N" or create_team == "Non" or create_team == "non" or create_team == "n":
        query = "SELECT Id_equipe, Nom, Nbr_pers FROM EQUIPE"
        mycursor.execute(query)
        resultats = mycursor.fetchall()

        os.system("cls")
        print("\nVoici la liste des équipes disponibles: \n")
        for resultat in resultats:
            Id_equipe = resultat[0]
            Nom = resultat[1]
            Nbr_pers = resultat[2]
            print(" Id:", Id_equipe, "\n", "Nom:", Nom,
                  "\n", "Nombre de membres:", Nbr_pers, "\n")

        team_id = input(
            "Pour selectionner une équipe, entrez son Id, sinon entrez 'back' pour revenir au menu principal \n")
        os.system("cls")

        # Update de la table Client avec l'Id de l'équipe
        query = "UPDATE CLIENT SET Id_equipe = %s WHERE Id_Pers = %s"
        mycursor.execute(query, (team_id, Id_pers))
        cnx.commit()
        print("Vous avez bien rejoint l'équipe !")

        # Si le client veut revenir au menu principal
        if team_id == "back":
            main_client(cnx, Id_pers)

        # Exit
        if team_id == "exit":
            print("Vous avez quitté l'application")
            sleep(1)
            exit()


def inscrire_activite(cnx, Id_pers):
    """
    Cette fonction permet d'inscrire un client à une activité.

    """
    # On récupère les activités disponibles
    mycursor = cnx.cursor(prepared=True)
    query = "SELECT Id_type_acti, Nom FROM TYPE_ACTIVITE"
    mycursor.execute(query)
    resultats = mycursor.fetchall()
    # On affiche les activités disponibles
    os.system("cls")
    print("\nVoici la liste des activités disponibles: \n")
    print(resultats)

    # Pour obtenir plus d'informations sur une activité
    print("Si vous voulez plus d'informations sur une activité, entrez son Id, sinon entrez 'back' pour revenir au menu principal \n")
    queryInfo = "SELECT a.Date, a.Heure, a.Lieu, t.Id_type_acti, t.Nom, t.Prix, t.Taille_min_, t.Age_min FROM ACTIVITE a JOIN TYPE_ACTI t ON a.Id_type_acti = t.Id_type_acti"
    mycursor.execute(queryInfo)
    resultatInfo = mycursor.fetchall()
    for resultat in resultatInfo:
        Date, Heure, Lieu, Id_type_acti, Nom, Prix, Taille_min_, Age_min = resultat
        print("Date: {}\nHeure: {}\nLieu: {}\nId: {}\nNom: {}\nPrix: {}\nTaille minimum: {}\nAge minimum: {}\n".format(Date, Heure, Lieu, Id_type_acti, Nom, Prix, Taille_min_, Age_min))

    # Si le client veut s'inscrire à une activité
    activity_id = input("Pour selectionner une activité, entrez son Id, sinon entrez 'back' pour revenir au menu principal \n")
    os.system("cls")
    query = "SELECT Id_acti FROM ACTIVITE WHERE Id_type_acti = %s"
    mycursor.execute(query, (activity_id,))
    resultats = mycursor.fetchall()
    if resultats == []:
        print("L'activité n'existe pas")
        sleep(2)
        inscrire_activite(cnx, Id_pers)
    
    # On inscrit le client à l'activité
    query = "SELECT Id_cli FROM CLIENT WHERE Id_Pers = %s"
    mycursor.execute(query, (Id_pers,))
    Id_cli = mycursor.fetchall()[0][0]
    query = "INSERT INTO inscription (Id_cli, Id_acti) VALUES (%s, %s)"
    mycursor.execute(query, (Id_cli, activity_id))
    cnx.commit()
    print("Vous êtes bien inscrit à l'activité !")
