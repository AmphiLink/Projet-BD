from time import sleep


def main_admin(cnx, Id_pers):
    choix = "basic"
    while choix not in ("gérer une fiche compta", "rajouter un matériel", "gérer un matériel", "liste des clients", "supprimer un client", "profil", "exit"):
        choix = input(
            "Que voulez vous faire ? (gérer une fiche compta, rajouter un matérie, gérer un matériel, liste des clients, supprimer un client, profil, exit) \n")
        sleep(1)

    myCursor = cnx.cursor()
    # On récupère l'Id_staff
    queryIdStaf = ("SELECT Id_staff FROM STAFF WHERE Id_pers = %s")
    myCursor.execute(queryIdStaf, (Id_pers,))
    Id_staff = myCursor.fetchall()[0][0]

    # On récupère l'IdAdmin
    queryIdAdmin = (
        "SELECT Id_admin FROM ADMINISTRATION WHERE Id_staff = %s")
    myCursor.execute(queryIdAdmin, (Id_staff,))
    Id_admin = myCursor.fetchall()[0][0]

    if choix == "exit":
        print("Vous avez quitté l'application !")
        sleep(1)
        exit()

    elif choix == "gérer une fiche compta":
        # On sélectionne toutes les fiches compta non-gérées
        queryFicheCompta = ("SELECT * FROM FICHE_COMPTA WHERE Id_admin = NULL")
        myCursor.execute(queryFicheCompta)
        ficheCompta = myCursor.fetchall()

        # On affiche les fiches compta non-gérées
        for i in range(len(ficheCompta)):
            print(ficheCompta[i], "\n")

        Id_fiche_compta = input(
            "Quelle fiche compta voulez-vous gérer ? (Tapez le numéro de la fiche)\n")

        # On vérifie que le numéro est bon
        queryVerifIdFiche = "SELECT Id_fiche_compta FROM FICHE_COMPTA WHERE Id_fiche_compta = %s"
        myCursor.execute(queryVerifIdFiche, (Id_fiche_compta,))
        myCursor.fetchall()

        if myCursor == []:
            print("Cette fiche n'existe pas où est déjà gérée !")
            main_admin(cnx, Id_pers)

        # On insère l'Id_admin dans la table FICHE_COMPTA
        queryGereFiche = "INSERT INTO FICHE_COMPTA (Id_admin) VALUES (%s) WHERE Id_fiche_compta = %s"
        myCursor.execute(queryGereFiche, (Id_admin, Id_fiche_compta))
        cnx.commit()

    elif choix == "rajouter un matériel":
        myCursor = cnx.cursor()
        Nom = input("Nom du matériel ? \n")
        TypeMateriel = input(
            "Type de matériel ? (sportif, bricolage, jardin,...)\n")
        Prix = input("Prix du matériel ? \n")
        Etat = input("Etat du matériel ? (Description de son état général)\n")

        # On insère les données dans la table matériel
        queryInsertMateriel = "INSERT INTO MATERIEL (Nom, TypeMateriel, Prix, Etat) VALUES (%s, %s, %s, %s)"
        myCursor.execute(queryInsertMateriel, (Nom, TypeMateriel, Prix, Etat))
        cnx.commit()

    elif choix == "gérer un matériel":
        myCursor = cnx.cursor()
        # On sélectionne tous les matériels non-gérés
        queryMateriel = ("SELECT * FROM MATERIEL WHERE Id_admin = NULL")
        myCursor.execute(queryMateriel)
        materiel = myCursor.fetchall()

        # On affiche les matériels non-gérés
        for i in range(len(materiel)):
            print(materiel[i], "\n")

        Id_materiel = input(
            "Quel matériel voulez-vous gérer ? (Tapez le numéro du matériel)\n")

        # On vérifie que le numéro est bon
        queryVerifIdMateriel = "SELECT Id_materiel FROM MATERIEL WHERE Id_materiel = %s"
        myCursor.execute(queryVerifIdMateriel, (Id_materiel,))
        myCursor.fetchall()

        if myCursor == []:
            print("Ce matériel n'existe pas où est déjà géré !")
            main_admin(cnx, Id_pers)

        # On insère l'Id_admin dans la table MATERIEL
        queryGereMateriel = "INSERT INTO MATERIEL (Id_admin) VALUES (%s) WHERE Id_materiel = %s"
        myCursor.execute(queryGereMateriel, (Id_admin, Id_materiel))
        cnx.commit()

    elif choix == "liste des clients":
        myCursor = cnx.cursor()
        # Pour chaque client, on affiche son nom, prénom, numéro de téléphone son mail, son pays et sa ville
        queryListeClient = (
            "SELECT Id_Pers, Nom, Prenom, Con_Telephone, Con_Email, Pays, Ville FROM PERSONNE JOIN CLIENT ON PERSONNE.Id_Pers = CLIENT.Id_Pers JOIN Prenom ON PERSONNE.Id_Pers = Prenom.Id_Pers")
        myCursor.execute(queryListeClient)
        listeClient = myCursor.fetchall()

        # On affiche chaque info du client joliement (Nom : .., \n Prénom : .., etc.)
        for i in range(len(listeClient)):
            print("Id : ", listeClient[i][0], "\nNom : ", listeClient[i][1], "\nPrénom : ", listeClient[i][2], "\nNuméro de téléphone : ",
                  listeClient[i][3], "\nEmail : ", listeClient[i][4], "\nPays : ", listeClient[i][5], "\nVille : ", listeClient[i][6], "\n ------------------------------- \n")

    else:
        myCursor = cnx.cursor()
        # On récupère l'Id du client
        Id_cli = input("Quel client voulez-vous supprimer ? (Tapez son Id)\n")

        # On vérifie que l'Id est bon
        queryVerifIdCli = "SELECT Id_cli FROM CLIENT WHERE Id_cli = %s"
        myCursor.execute(queryVerifIdCli, (Id_cli,))
        myCursor.fetchall()

        if myCursor == []:
            print("Ce client n'existe pas !")
            main_admin(cnx, Id_pers)

        # On vérifie que le client n'a pas de réservation en cours

        queryVerifResa = "SELECT Id_cli FROM loue_emplacement WHERE Id_cli = %s"
        myCursor.execute(queryVerifResa, (Id_cli,))
        myCursor.fetchall()

        if myCursor != []:
            # On update la date de fin de location à aujourd'hui
            queryUpdateDateFin = "UPDATE loue_emplacement SET Date_fin = CURDATE() WHERE Id_cli = %s"
            myCursor.execute(queryUpdateDateFin, (Id_cli,))
            cnx.commit()

        # On update tout sauf Id_cli et Id_pers à NULL
        querydeleteInfos = "UPDATE CLIENT SET Pays = NULL, Code_postal = NULL, Con_Telephone = NULL, Con_Email = NULL, Ville = NULL, Numero_de_maison = NULL, Id_equipe = NULL WHERE Id_cli = %s"
        myCursor.execute(querydeleteInfos, (Id_cli,))
        cnx.commit()

        # On supprime le client de la table PERSONNE donc tout sauf Id_pers à NULL
        querydeleteClient = "UPDATE PERSONNE SET Nom = NULL, Age = NULL, Mot_de_passe = NULL WHERE Id_cli = %s"
        myCursor.execute(querydeleteClient, (Id_cli,))
        cnx.commit()

        # On supprime le client de la table PRENOM donc tout sauf Id_pers à NULL
        querydeletePrenom = "UPDATE PRENOM SET Prenom = NULL WHERE Id_cli = %s"
        myCursor.execute(querydeletePrenom, (Id_cli,))
        cnx.commit()

        print("Le client a bien été supprimé !")
    main_admin(cnx, Id_pers)
