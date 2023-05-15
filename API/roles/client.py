import os
from time import sleep

from roles.animateur import liste_activités


def main_client(cnx, Id_Pers):
    """
    Cette fonction permet d'utiliser les différentes fonctionnnalités de l'application en tant que client.

    Parameters:
    -----------
    cnx : mysql.connector.connection.MySQLConnection (Object)
    Id_Pers : l'Id de la personne conectée (int)
    """

    choix = "basic"
    os.system("cls")
    while choix not in ("Réserver du matériel", "Louer un emplacement", "Rejoindre/Créer une équipe", "Voir la liste des activités", "S'inscrire à une activité", "S'inscrire à un tournoi" "profil", "exit", "1", "2", "3", "4", "5", "6", "7", "8"):
        choix = input("\nQue voulez vous faire ?\n 1: Reservé du matériel\n 2: Loué un emplacement\n 3: Rejoindre/Créer une équipe\n 4: Voir la liste des activités\n 5: S'inscrire à une activité\n 6: S'inscrire à un tournoi\n 7: profil\n 8: exit\n")
        os.system("cls")

    myCursor = cnx.cursor(prepared=True)
    # On récupère l'IdClient
    queryIdClient = "SELECT Id_cli FROM CLIENT where Id_Pers = %s"
    myCursor.execute(queryIdClient, (Id_Pers,))
    Id_client = myCursor.fetchall()[0][0]

    if choix == "Reserver du matériel" or choix == "1":
        reserve_mat(cnx, Id_Pers, Id_client)

    elif choix == "Louer un emplacement" or choix == "2":
        loue_emplacement(cnx, Id_Pers)

    elif choix == "Rejoindre/Créer une équipe" or choix == "3":
        rejoindre_equipe(cnx, Id_Pers)

    elif choix == "Voir la liste des activités" or choix == "4":
        liste_activités(cnx, Id_Pers)
        skip = input("Appuyez sur entrée pour continuer")
        if skip == "":
            os.system("cls")
            main_client(cnx, Id_Pers)

    elif choix == "S'inscrire à une activité" or choix == "5":
        inscrire_activite(cnx, Id_Pers)

    elif choix == "S'inscrire à un tournoi" or choix == "6":
        inscrire_tournoi(cnx, Id_Pers)

    elif choix == "profil" or choix == "7":
        profil(cnx, Id_Pers)

    elif choix == "exit" or choix == "8":
        print("Vous avez quitté l'application !")
        sleep(1)
        exit()


def reserve_mat(cnx, Id_Pers, Id_client):
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
        sleep(2)
        main_client(cnx, Id_Pers)

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
    main_client(cnx, Id_Pers)


def loue_emplacement(cnx, Id_Pers):
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
    # On récupère les types d'emplacement disponibles
    queryIdEmplacement = "SELECT Type_emplacement FROM EMPLACEMENT WHERE Id_emplacement = %s && Occupation = 0"
    myCursor.execute(queryIdEmplacement, (Id_emplacement,))

    if Id_emplacement == "exit":
        print("Vous avez quitté l'application")
        sleep(1)
        exit()

    if myCursor.fetchall() == []:
        print("Tous ces types d'emplacements sont occupés")
        sleep(4)
        main_client(cnx, Id_Pers)

    # Obtenir plus d'informations sur l'emplacement
    os.system("cls")
    print("\nVoici le détail des informations de l'emplacement que vous voulez avez choisi: \n")

    querydetail = "SELECT Type_emplacement, Prix, bbq, nbr_places, acces_eau, cuisinier FROM EMPLACEMENT WHERE Id_emplacement = %s"
    myCursor.execute(querydetail, (Id_emplacement,))
    resultat = myCursor.fetchall()
    # Ici pas besoin de vérifier que ce type d'emplacement est disponible car on l'a déjà fait
    verif = 0
    for resultats in resultat:
        type_emp = resultats[0]
        prix = resultats[1]
        bbq = resultats[2]
        nbr_place = resultats[3]
        acces_eau = resultats[4]
        cuisinier = resultats[5]

        if bbq == 1:
            bbq = "Oui"
        else:
            bbq = "Non"
        if acces_eau == 1:
            acces_eau = "Oui"
        else:
            acces_eau = "Non"
        if verif == 1:
            print("\n=========================\n")
        print("Id:", Id_emplacement, "\n", type_emp, "\n", "Prix:", prix, "€" "\n", "Barbecue:", bbq, "\n",
              "Nombre de place(s):", nbr_place, "\n", "Accès à l'eau:", acces_eau, "\n", "Cuisinier:", cuisinier, "\n")
        verif = 1
    if len(resultat) == 1:
        reservation = input(
            "Si vous voulez réserver cet emplacement, entrez son Id, sinon entrez 'back' pour voir les autres emplacements \n")
    else:
        reservation = input(
            "Entrez l'Id de l'emplacement que vous-voulez réserver, sinon entrez 'back' pour voir les autres types d'emplacements \n")
    os.system("cls")
    if reservation == "back":
        loue_emplacement(cnx, Id_Pers)

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

    # On insert dans la table loue_emplacement
    queryIdcli = "SELECT Id_cli FROM CLIENT WHERE Id_Pers = %s"
    myCursor.execute(queryIdcli, (Id_Pers,))
    id_cli = myCursor.fetchall()[0][0]
    queryInsertReserve = "INSERT INTO loue_emplacement (Id_cli, Id_emplacement, Date_debut, Date_fin) VALUES (%s, %s, %s, %s)"
    myCursor.execute(queryInsertReserve,
                     (id_cli, Id_emplacement, Date_debut, Date_fin))
    cnx.commit()

    # On met à jour la table emplacement
    queryUpdateEmp = "UPDATE EMPLACEMENT SET Occupation = 1 WHERE Id_emplacement = %s"
    myCursor.execute(queryUpdateEmp, (Id_emplacement,))
    cnx.commit()

    print("\nVous pouvez aller récupérer votre emplacement !")
    sleep(3)
    main_client(cnx, Id_Pers)


def rejoindre_equipe(cnx, Id_Pers):
    """
    Cette fonction permet de rejoindre une équipe.

    """
    # Si le client veut rejoindre une équipe
    mycursor = cnx.cursor(prepared=True)
    create_team = input("Voulez-vous créer une équipe ? (O/N) \n")
    queryVerif = "SELECT Id_equipe FROM CLIENT WHERE Id_Pers = %s"
    mycursor.execute(queryVerif, (Id_Pers,))
    if create_team == "Oui" or create_team == "oui" or create_team == "O" or create_team == "o":
        # On vérifie que la personne n'est pas déjà dans une équipe
        if mycursor.fetchall()[0][0] == None:
            team_name = input("Quel est le nom de votre équipe ? \n")
            number_of_members = input(
                "Combien de membres voulez-vous dans votre équipe ? \n")
            # On crée l'équipe
            queryAddEquipe = "INSERT INTO EQUIPE (Nom, Nbr_PersMax, Nbr_pers) VALUES (%s, %s, 1)"
            mycursor.execute(queryAddEquipe, (team_name, number_of_members))
            cnx.commit()

            # On récupère l'id de l'équipe que l'on vient de créer
            queryIdEquipe = "SELECT Id_equipe FROM EQUIPE WHERE Nom = %s"
            mycursor.execute(queryIdEquipe, (team_name,))
            Id_equipe = mycursor.fetchall()[0][0]

            # On ajoute l'id de l'équipe dans la table client
            queryAddInCli = "UPDATE CLIENT SET Id_equipe = %s WHERE Id_Pers = %s"
            mycursor.execute(queryAddInCli, (Id_equipe, Id_Pers))
            cnx.commit()
            print("Votre équipe a bien été créée !")
            sleep(2)
            main_client(cnx, Id_Pers)
        else:
            print("Vous êtes déjà dans une équipe !")
            sleep(2)
            main_client(cnx, Id_Pers)

    # Si le client ne veut pas créer d'équipe
    if create_team == "N" or create_team == "Non" or create_team == "non" or create_team == "n":
        if mycursor.fetchall()[0][0] == None:
            # On affiche les équipes disponibles non pleines
            query = "SELECT Id_equipe, Nom, Nbr_pers FROM EQUIPE WHERE Nbr_pers < Nbr_pers_max"
            mycursor.execute(query)
            resultats = mycursor.fetchall()
            os.system("cls")
            print("\nVoici la liste des équipes disponibles: \n")
            for resultat in resultats:
                Id_equipe = resultat[0]
                Nom = resultat[1]
                Nbr_pers = resultat[2]
                Nbr_PersMax = resultat[3]
                print(" Id:", Id_equipe, "\n", "Nom:", Nom, "\n",
                      "Nombre de membres:", Nbr_pers + "/" + Nbr_PersMax, "\n")

            team_id = input(
                "Pour selectionner une équipe, entrez son Id, sinon entrez 'back' pour revenir au menu principal \n")
            os.system("cls")

            # Si le client veut revenir au menu principal
            if team_id == "back":
                main_client(cnx, Id_Pers)

            if team_id == "exit":
                print("Vous avez quitté l'application !")
                sleep(1)
                exit()

            # on récupère le nombre de membres de l'équipe
            queryNbrPers = "SELECT Nbr_pers FROM EQUIPE WHERE Id_equipe = %s WHERE Nbr_pers < Nbr_pers_max"
            mycursor.execute(queryNbrPers, (team_id,))
            Nbr_pers = mycursor.fetchall()[0][0]

            # Ici pas besoin de vérifier que l'équipe est pleine car on l'a fait au-dessus
            Nbr_pers = int(Nbr_pers) + 1

            # On met à jour le nombre de membres de l'équipe
            queryUpdateNbrPers = "UPDATE EQUIPE SET Nbr_pers = %s WHERE Id_equipe = %s"
            mycursor.execute(queryUpdateNbrPers, (Nbr_pers, team_id))
            cnx.commit()

            # On ajoute l'id de l'équipe dans la table client
            queryAdd = "UPDATE CLIENT SET Id_equipe = %s WHERE Id_Pers = %s"
            mycursor.execute(queryAdd, (team_id, Id_Pers))
            cnx.commit()
            print("Vous avez bien rejoint l'équipe !")

        else:
            print("Vous êtes déjà dans une équipe !")
            sleep(2)
            main_client(cnx, Id_Pers)

    if create_team == "exit":
        print("Vous avez quitté l'application !")
        sleep(1)
        exit()


def inscrire_activite(cnx, Id_Pers):
    """
    Cette fonction permet d'inscrire un client à une activité.

    """
    # On récupère les activités disponibles
    mycursor = cnx.cursor(prepared=True)
    queryInfos = "SELECT Date_acti, Heure, Lieu, TA.Id_type_acti, TA.Nom, TA.Prix, Taille_min_, Age_min FROM ACTIVITE ACT, TYPE_ACTI TA WHERE Date_acti > CURDATE() AND ACT.Id_type_acti = TA.Id_type_acti"
    mycursor.execute(queryInfos)
    # On affiche les activités disponibles
    os.system("cls")
    print("\nVoici la liste des activités disponibles: \n")
    verif = 0
    if mycursor.rowcount == 0:
        print("Il n'y a pas d'activités disponibles pour le moment !")
        sleep(2)
        main_client(cnx, Id_Pers)
    for Date, Heure, Lieu, Id, Activite, Prix, Taille, Age in mycursor:
        if verif == 1:
            print("\n=========================")
        print("Id :", Id, "\nDate:", Date, "\nHeure:", Heure, "\nLieu:", Lieu, "\nActivité:",
              Activite, "\nPrix:", Prix, "\nTaille minimum:", Taille, "\nAge minimum:", Age, "\n")
        verif = 1

    # Si le client veut s'inscrire à une activité
    activity_id = input(
        "Pour selectionner cette activité, entrez son Id, sinon entrez 'back' pour revenir au menu principal \n")
    # On vérifie que le client n'est pas déjà inscrit à l'activité
    query = "SELECT Id_cli FROM inscription WHERE Id_acti = %s"
    mycursor.execute(query, (activity_id,))
    if mycursor.fetchall() != []:
        print("Vous êtes déjà inscrit à cette activité !")
        sleep(2)
        main_client(cnx, Id_Pers)
    else:
        os.system("cls")
        query = "SELECT Id_acti FROM ACTIVITE WHERE Id_acti = %s"
        mycursor.execute(query, (activity_id,))
        if activity_id == "back":
            main_client(cnx, Id_Pers)
        if activity_id == "exit":
            print("Vous avez quitté l'application")
            sleep(1)
            exit()
        if mycursor.fetchall() == []:
            print("L'Id entré n'est pas valide, veuillez réessayer")
            sleep(2)
            inscrire_activite(cnx, Id_Pers)
        else:
            # On inscrit le client à l'activité
            query = "SELECT Id_cli FROM CLIENT WHERE Id_Pers = %s"
            mycursor.execute(query, (Id_Pers,))
            Id_cli = mycursor.fetchall()[0][0]
            query = "INSERT INTO inscription (Id_cli, Id_acti) VALUES (%s, %s)"
            mycursor.execute(query, (Id_cli, activity_id))
        cnx.commit()
        print("Vous êtes bien inscrit à l'activité !")
        sleep(1)
        main_client(cnx, Id_Pers)


def inscrire_tournoi(cnx, Id_Pers):
    """
    NE FONCTIONNE PAS ENCORE !!!!
    Cette fonction permet d'inscrire un client à un tournoi.

    """
    # On vérifie si le client possède une équipe
    mycursor = cnx.cursor(prepared=True)
    query = "SELECT Id_equipe FROM CLIENT WHERE Id_Pers = %s"
    mycursor.execute(query, (Id_Pers,))
    Id_equipe = mycursor.fetchall()[0][0]
    if Id_equipe == None:
        print("Vous n'avez pas d'équipe, veuillez en créer une")
        sleep(2)
        rejoindre_equipe(cnx, Id_Pers)
    else:
        # On récupère les tournois disponibles
        mycursor = cnx.cursor(prepared=True)
        query = "SELECT Id_tournoi, Id_acti FROM TOURNOI"
        mycursor.execute(query)
        resultats = mycursor.fetchall()
        os.system("cls")
        print("\nVoici la liste des tournois disponibles: \n")
        for resultat in resultats:
            Id_tournoi = resultat[0]
            Id_acti = resultat[1]
            query = "SELECT Id_type_acti FROM ACTIVITE WHERE Id_acti = %s"
            mycursor.execute(query, (Id_acti,))
            Id_type_acti = mycursor.fetchall()[0][0]
            query = "SELECT Nom FROM TYPE_ACTI WHERE Id_type_acti = %s"
            mycursor.execute(query, (Id_type_acti,))
            Nom = mycursor.fetchall()[0][0]
            print(" Id:", Id_tournoi, "\n", "Nom:", Nom, "\n")

        # Pour obtenir plus d'informations sur un tournoi
        tournoi_id = input(
            "Si vous voulez plus d'informations sur un tournoi, entrez son Id, sinon entrez 'back' pour revenir au menu principal \n")

        # On vérifie que l'Id entré est valide
        query = "SELECT Id_tournoi FROM TOURNOI WHERE Id_tournoi = %s"
        mycursor.execute(query, (tournoi_id,))
        resultats = mycursor.fetchall()
        if not resultats:
            os.system("cls")
            print("L'Id entré n'est pas valide, veuillez réessayer")
            sleep(2)
            inscrire_tournoi(cnx, Id_Pers)

        if tournoi_id == "back":
            main_client(cnx, Id_Pers)
        if tournoi_id == "exit":
            print("Vous avez quitté l'application")
            sleep(1)
            exit()

        else:
            # On affiche le nom du sport
            query = "SELECT Nom FROM TYPE_ACTI WHERE (SELECT Id_acti FROM TOURNOI WHERE Id_tournoi = %s)"
            mycursor.execute(query, (tournoi_id,))
            Nom = mycursor.fetchall()[0][0]
            # On affiche les informations du tournoi
            queryInfo = "SELECT Id_tournoi, Id_acti, Date_tournoi, Heure, Lieu, Prix FROM TOURNOI WHERE Id_tournoi = %s"
            mycursor.execute(queryInfo, (tournoi_id,))
            resultats = mycursor.fetchall()
            for resultat in resultats:
                Id_tournoi = resultat[0]
                Date_tournoi = resultat[2]
                Heure = resultat[3]
                Lieu = resultat[4]
                Prix = resultat[5]
                os.system("cls")
            print(" Id:", Id_tournoi, "\n", "Nom:", Nom, "\n", "Date_tournoi:",
                  Date_tournoi, "\n", "Heure:", Heure, "\n", "Lieu:", Lieu, "\n", "Prix:", Prix)

        # Si le client veut s'inscrire à un tournoi
        tournoi_id = input(
            "\nPour selectionner ce tournoi, entrez son Id, sinon entrez 'back' pour revenir au menu principal \n")
        os.system("cls")
        query = "SELECT Id_tournoi FROM TOURNOI WHERE Id_tournoi = %s"
        mycursor.execute(query, (tournoi_id,))
        resultats = mycursor.fetchall()

        # Si le client veut revenir en arrière
        if tournoi_id == "back":
            inscrire_tournoi(cnx, Id_Pers)

        if tournoi_id == "exit":
            print("Vous avez quitté l'application")
            sleep(1)
            exit()

        # On vérifie que l'Id entré est valide
        query = "SELECT Id_tournoi FROM TOURNOI WHERE Id_tournoi = %s"
        mycursor.execute(query, (tournoi_id,))
        resultats = mycursor.fetchall()
        if not resultats:
            os.system("cls")
            print("L'Id entré n'est pas valide, veuillez réessayer")
            sleep(2)
            inscrire_tournoi(cnx, Id_Pers)

        else:
            # On récupère l'Id de l'équipe du client
            query = "SELECT Id_equipe FROM CLIENT WHERE Id_Pers = %s"
            mycursor.execute(query, (Id_Pers,))
            Id_equipe = mycursor.fetchall()[0][0]

            # On INSERT dans la table PARTICIPE
            query = "INSERT INTO participe (Id_equipe, Id_tournoi) VALUES (%s, %s)"
            mycursor.execute(query, (Id_equipe, tournoi_id))
            cnx.commit()
            print("Vous êtes bien inscrit au tournoi !")


def profil(cnx, Id_Pers):
    """
    Cette fonction permet d'afficher le profil d'un client.

    Parameters
    ----------
    cnx : mysql.connector.connection.MySQLConnection (Object)
    Id_Pers : l'Id de la personne conectée (int)
    """
    mycursor = cnx.cursor(prepared=True)
    os.system("cls")
    # On récupère l'Id_cli
    queryIdCli = "SELECT Id_cli FROM CLIENT WHERE Id_Pers = %s"
    mycursor.execute(queryIdCli, (Id_Pers,))
    Id_cli = mycursor.fetchall()[0][0]
    print("Voici votre profil : \n========================\n")
    print("Données personnelles : \n=========================")
    queryInfos = "SELECT Id_cli, Nom, Age, Pays, Code_postal, Ville, Numero_de_maison, Con_email, Con_telephone FROM view_Client WHERE Id_cli = %s GROUP BY Id_cli"
    mycursor.execute(queryInfos, (Id_cli,))

    for Id_cli, Nom, Age, Pays, Code_postal, Ville, Numero_de_maison, Con_email, Con_telephone in mycursor:
        print("Id:", Id_cli, "\nNom:", Nom, "\nAge:", Age, "ans \nPays:", Pays, "\nCode postal:",
              Code_postal, "\nVille:", Ville, "\nN° de maison:", Numero_de_maison, "\nemail:", Con_email, "\ntéléphone:", Con_telephone, "\n")

    mycursor.fetchall()
    queryIdEmplacement = "SELECT Id_emplacement FROM view_Client WHERE Id_cli = %s"
    mycursor.execute(queryIdEmplacement, (Id_cli,))
    Id_emplacement = mycursor.fetchall()[0][0]
    print("Emplacement : \n=========================")
    if Id_emplacement == None:
        print("Vous n'avez pas encore d'emplacement\n")
    else:
        queryInfosEmplacement = "SELECT Id_emplacement, Type_emplacement, Occupation, Prix, bbq, nbr_places, acces_eau, cuisinier FROM EMPLACEMENT WHERE Id_emplacement = %s GROUP BY Id_emplacement"
        mycursor.execute(queryInfosEmplacement, (Id_emplacement,))
        verif = 0
        for Id_emplacement, Type_emplacement, Occupation, Prix, bbq, nbr_places, acces_eau, cuisinier in mycursor:
            # On convertit tous les booléens en oui/non
            if Occupation == 1:
                Occupation = "Oui"
            if bbq == 0:
                bbq = "Non"
            else:
                bbq = "Oui"
            if acces_eau == 0:
                acces_eau = "Non"
            else:
                acces_eau = "Oui"
            if cuisinier == 0:
                cuisinier = "Non"
            else:
                cuisinier = "Oui"
                if verif == 1:
                    print("\n=========================")
            print("N°:", Id_emplacement, "\nType:", Type_emplacement, "\nOccupation:", Occupation, "\nPrix:", Prix, "\u20ac\nBBQ:",
                  bbq, "\nNombre de places:", nbr_places, "\nAccès à l'eau:", acces_eau, "\nCuisinier:", cuisinier, "\n")
            verif = 1

    # On affiche les infos liées au tournoi et à l'équipe
    queryE = "SELECT Id_equipe, Equipe, Nbr_pers, Nbr_PersMax FROM view_Client WHERE Id_cli = %s Group by Id_equipe"
    mycursor.execute(queryE, (Id_cli,))
    for Id_equipe, Equipe, Nbr_pers, Nbr_PersMax in mycursor:
        print("Equipe : \n=========================")
        if Id_equipe == None:
            print("Vous n'êtes inscrit dans aucune équipe\n")
        else:
            print("Id de l'équipe:", Id_equipe,
                  "\nNom de l'équipe:", Equipe,
                  "\nNombre de personnes:", str(Nbr_pers)+"/"+str(Nbr_PersMax), "\n")
    mycursor.fetchall()
    print("Tournoi : \n=========================")
    queryIdTournoi = "SELECT Id_tournoi FROM view_Client WHERE Id_cli = %s GROUP BY Id_tournoi"
    mycursor.execute(queryIdTournoi, (Id_cli,))
    Id_tournoi = mycursor.fetchall()[0][0]
    if Id_tournoi == None:
        print("Vous n'êtes inscrit à aucun tournoi\n")
    else:
        queryTournoi = "SELECT Id_tournoi, Date_tournoi, Heure, Lieu, Prix FROM TOURNOI WHERE Id_tournoi = %s"
        mycursor.execute(queryTournoi, (Id_tournoi,))
        verif2 = 0
        for Id_tournoi, Date_tournoi, Heure, Lieu, Prix in mycursor:
            if verif2 == 1:
                print("\n=========================")
            print("Id du tournoi:", Id_tournoi, "\nDate du tournoi:", Date_tournoi,
                  "\nHeure du tournoi:", Heure, "\nLieu du tournoi:", Lieu, "\nPrix:", Prix, "\u20ac\n")
            verif2 = 1
    mycursor.fetchall()
    # On affiche les infos liées aux activités
    queryIdActi = "SELECT Id_acti FROM view_Client WHERE Id_cli = %s GROUP BY Id_acti"
    mycursor.execute(queryIdActi, (Id_cli,))
    maListe = mycursor.fetchall()

    print("Activité : \n=========================")
    for answers in maListe:
        for Id_acti in answers:
            if Id_acti == None:
                print("Vous n'avez pas encore d'activité\n")
            else:
                queryInfosActi = "SELECT Id_acti, Date_acti, Heure, Lieu, TA.Nom, A.Id_type_acti FROM ACTIVITE A, TYPE_ACTI TA WHERE A.Id_type_acti = TA.Id_type_acti AND Id_acti = %s GROUP BY Id_acti"
                mycursor.execute(queryInfosActi, (Id_acti,))
                verif = 0
                for Id_acti, Date_acti, Heure, Lieu, Nom, Id_type_acti in mycursor:
                    if verif == 1:
                        print("\n=========================")
                    print("Id:", Id_acti, "\nDate de l'activité:", Date_acti,
                          "\nHeure de l'activité:", Heure, "\nLieu de l'activité:", Lieu, "\nNom de l'activité:", Nom, "\n")
                    verif = 1
    mycursor.fetchall()
    # On affiche les infos liées à la location de matériel
    # Ici on doit définir un 2 ème curseur car on ne peut pas faire deux requêtes sur le même curseur en même temps
    queryIdMat = "SELECT Id_mat FROM view_Client WHERE Id_cli = %s GROUP BY Id_mat"
    mycursor.execute(queryIdMat, (Id_cli,))
    print("Votre matériel loué: \n=========================")
    maListe = mycursor.fetchall()

    verif = 0
    for answers in maListe:
        for Id_mat in answers:
            if Id_mat == None:
                print("Vous n'avez pas encore loué de matériel\n")
            else:
                queryInfosMat = "SELECT LM.Id_mat, Date_loc, Nom, Type_mat, Prix, Etat FROM MATERIEL M, Loue_mat LM WHERE M.Id_mat = LM.Id_mat AND LM.Id_mat = %s"
                mycursor.execute(queryInfosMat, (Id_mat,))

                # Ici on aura toujours que un seul tuple dans la liste mycursor.fetchall()
                for Id_mat, Date_loc, Nom, Type_mat, Prix, Etat in mycursor:
                    if verif == 1:
                        print("\n=========================")
                    print("Id:", Id_mat, "\nDate de location:", Date_loc,
                          "\nNom du matériel:", Nom, "\nType du matériel:", Type_mat, "\nPrix:", Prix, "\u20ac\nEtat:", Etat, "\n")
            verif = 1
    mycursor.fetchall()
    choix = ""
    while choix not in ("modif", "back"):
        choix = input(
            "\nSi vous voulez modifier votre profil, tapez 'modif', sinon tapez 'back' pour revenir au menu principal \n")
    if choix == "modif":
        champ = ""
        while champ not in ("Pays", "Code postal", "Ville", "N° de maison", "Nom", "Age", "email", "téléphone", "exit"):
            champ = input(
                "Quel champ voulez-vous modifier (dans vos informations personnelles ?\n")

            if champ == "exit":
                print("Vous avez quitté l'application")
                sleep(1)
                exit()
        if champ == "Code postal":
            champ = "Code_postal"
        elif champ == "N° de maison":
            champ = "Numero_de_maison"
        elif champ == "email":
            champ = "Con_email"
        elif champ == "téléphone":
            champ = "Con_telephone"

        valeur = input("Quelle valeur voulez-vous mettre ?\n")
        query = "UPDATE CLIENT SET {} = %s WHERE Id_cli = %s".format(champ)
        mycursor.execute(query, (valeur, Id_cli))
        cnx.commit()
        print("Votre profil a bien été modifié !")
        sleep(2)
        main_client(cnx, Id_Pers)
    elif choix == "back":
        main_client(cnx, Id_Pers)
    else:
        print("Vous avez quitté l'application")
        sleep(1)
        exit()
