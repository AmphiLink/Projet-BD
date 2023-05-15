from time import sleep
from datetime import datetime
import os


def main_admin(cnx, Id_Pers):
    choix = "basic"
    while choix not in ("gérer une fiche compta", "rajouter un matériel", "gérer un matériel", "liste des clients", "supprimer un client", "profil", "regarder la compta de l'année", "Evolution de la compta annuelle", "exit"):
        choix = input(
            "Que voulez vous faire ? (gérer une fiche compta, rajouter un matérie, gérer un matériel, liste des clients, supprimer un client, profil, regarder la compta de l'année, Evolution de la compta annuelle ,exit) \n")
        sleep(1)

    myCursor = cnx.cursor(prepared=True)
    # On récupère l'Id_staff
    queryIdStaf = ("SELECT Id_staff FROM STAFF WHERE Id_pers = %s")
    myCursor.execute(queryIdStaf, (Id_Pers,))
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

        if myCursor.fetchall() == []:
            print("Cette fiche n'existe pas où est déjà gérée !")
        else:
            # On insère l'Id_admin dans la table FICHE_COMPTA
            queryGereFiche = "UPDATE FICHE_COMPTA SET Id_admin = %s WHERE Id_fiche_compta = %s"
            myCursor.execute(queryGereFiche, (Id_admin, Id_fiche_compta))
            cnx.commit()
            print("Vous gérez maintenant cette fiche !")
        sleep(1)
        os.system("cls")

    elif choix == "rajouter un matériel":
        myCursor = cnx.cursor(prepared=True)
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
        myCursor = cnx.cursor(prepared=True)
        # On sélectionne tous les matériels non-gérés
        queryMateriel = ("SELECT * FROM MATERIEL WHERE Id_admin is null")
        myCursor.execute(queryMateriel)
        materiel = myCursor.fetchall()

        # On affiche les matériels non-gérés
        for i in range(len(materiel)):
            print(materiel[i], "\n")

        Id_mat = input(
            "Quel matériel voulez-vous gérer ? (Tapez le numéro du matériel)\n")

        # On vérifie que le numéro est bon
        queryVerifIdMateriel = "SELECT Id_mat FROM MATERIEL WHERE Id_mat = %s"
        myCursor.execute(queryVerifIdMateriel, (Id_mat,))

        if myCursor.fetchall() == []:
            print("Ce matériel n'existe pas !")
        else:
            # Si il existe on vérifie qu'il n'est pas déjà géré par un admin

            queryVerifIdMateriel = "SELECT Id_admin FROM MATERIEL WHERE Id_mat = %s"
            myCursor.execute(queryVerifIdMateriel, (Id_mat,))
            Id_admin = myCursor.fetchall()[0][0]

            if Id_admin != None:
                print("Ce matériel est déjà géré par un admin !")
            else:
                # On met à jour l'Id_admin dans la table MATERIEL
                queryGereMateriel = "UPDATE MATERIEL SET Id_admin = %s WHERE Id_mat = %s"
                myCursor.execute(queryGereMateriel, (Id_admin, Id_mat))
                cnx.commit()
                print("Vous gérez maintenant ce matériel !")
        sleep(1)
        os.system("cls")

    elif choix == "liste des clients":
        myCursor = cnx.cursor(prepared=True)
        # Pour chaque client, on affiche son nom, prénom, numéro de téléphone son mail, son pays et sa ville
        queryListeClient = "SELECT Id_cli, Nom, Con_Telephone, Con_Email, Pays, Ville FROM view_Client GROUP BY Id_Cli"
        myCursor.execute(queryListeClient)
        listeClient = myCursor.fetchall()

        # On affiche chaque info de chaque client
        for i in range(len(listeClient)):
            print("\nNom : ", listeClient[i][1])
            print("Numéro de téléphone : ", listeClient[i][2])
            print("Mail : ", listeClient[i][3])
            print("Pays : ", listeClient[i][4])
            print("Ville : ", listeClient[i][5], "\n")
            if i != len(listeClient)-1:
                print("=========================================")
        skip = input("Appuyez sur entrée pour continuer")
        if skip == "":
            os.system("cls")

    elif choix == "regarder la compta de l'année":
        myCursor = cnx.cursor(prepared=True)
        année = input(
            "De quelle année voulez-vous regarder la compta ? (YYYY)\n")

        # Nous allons récupérer les Prix de chaque table et les mettre dans fiche_compta
        # Compta_emplacement
        queryComptaEmplacement = "SELECT SUM(Prix) FROM view_Comptabilite_EMPLACEMENT WHERE Date_debut LIKE %s"
        queryComptaMateriel = "SELECT SUM(Prix) FROM view_Comptabilite_MATERIEL WHERE Date_loc LIKE %s"
        queryComptaStaff = "SELECT SUM(Salaire) FROM view_Comptabilite_STAFFEmploye"
        queryComptaChef = "SELECT SUM(Salaire + Bonus) FROM view_Comptabilite_STAFFChef"

        # On récupère les résultats
        TodayDate = datetime.today()
        # On récupère les prix des emplacements
        myCursor.execute(queryComptaEmplacement, (année + "%",))
        comptaEmplacement = myCursor.fetchall()[0][0]

        # On récupère les prix des matériels
        myCursor.execute(queryComptaMateriel, (année + "%",))
        comptaMateriel = myCursor.fetchall()[0][0]

        # On récupère les salaires du staff et des chefs pour chaque mois écoulé de l'année
        année = int(année)
        if TodayDate.year > année:
            myCursor.execute(queryComptaStaff)
            comptaStaff = myCursor.fetchall()[0][0] * 12
            myCursor.execute(queryComptaChef)
            comptaChef = myCursor.fetchall()[0][0] * 12
        else:
            # On récupère le mois actuel
            mois = TodayDate.month
            myCursor.execute(queryComptaStaff)
            comptaStaff = myCursor.fetchall()[0][0] * mois
            myCursor.execute(queryComptaChef)
            comptaChef = myCursor.fetchall()[0][0] * mois

        ComptaTotal = float(comptaEmplacement) + float(comptaMateriel) - \
            float(comptaStaff) - float(comptaChef)

        # On insère les résultats dans la table FICHE_COMPTA
        # On vérifie si il n'y a pas déjà une fiche de compta pour cette année
        queryCheckFichesCompta = "SELECT SUM(Prix_total) FROM  FICHE_COMPTA WHERE Date_fiche LIKE %s"
        myCursor.execute(queryCheckFichesCompta, (str(année) + "%",))
        myCursor.fetchall()

        if myCursor != []:
            # Si il en existe déjà une on la met à jour
            queryInsertCompta = "UPDATE FICHE_COMPTA SET Prix_total = %s,  Date_fiche = %s WHERE Date_fiche LIKE %s"
            myCursor.execute(queryInsertCompta, (ComptaTotal,
                             datetime.today().strftime('%Y-%m-%d'), str(année) + "%"))
        else:
            # Sinon on en crée une nouvelle
            queryInsertCompta = "INSERT INTO FICHE_COMPTA (Prix_total, Date_fiche) VALUES (%s, %s)"
            myCursor.execute(queryInsertCompta, (ComptaTotal,
                             datetime.today().strftime('%Y-%m-%d')))
        cnx.commit()

        # On affiche la compta
        print("La compta de l'année ", année, " est de ", ComptaTotal, "€")

        skip = "helo"
        while skip != "":
            skip = input("Appuyez sur enter pour continuer")

    elif choix == "Evolution de la compta annuelle":
        myCursor = cnx.cursor(prepared=True)

        année = input(
            "De quelle année voulez-vous regarder l'évolution de la compta ? (YYYY)\n")

        TodayDate = datetime.today()
        if TodayDate.year > int(année):
            mois = 12
        else:
            mois = TodayDate.month
        # Nous allons récupérer les Prix de chaque table et les mettre dans fiche_compta
        # Compta_emplacement
        queryComptaEmplacement = "SELECT SUM(Prix), MONTH(Date_debut) FROM view_Comptabilite_EMPLACEMENT WHERE Date_debut LIKE '{}' AND DATE_FORMAT(Date_debut, '%m') < {} GROUP BY MONTH(Date_debut)".format(
            année + "%", mois+1)
        queryComptaMateriel = "SELECT SUM(Prix), MONTH(Date_loc) FROM view_Comptabilite_MATERIEL WHERE Date_loc LIKE '{}' AND DATE_FORMAT(Date_loc, '%m') < {} GROUP BY MONTH(Date_loc)".format(
            année + "%", mois+1)
        queryComptaStaff = "SELECT SUM(Salaire) FROM view_Comptabilite_STAFFEmploye"
        queryComptaChef = "SELECT SUM(Salaire + Bonus) FROM view_Comptabilite_STAFFChef"

        # On récupère les résultats
        # On récupère les prix des emplacements de chaque mois de l'année
        ListePrixMATERIEL = []
        # On récupère les prix des Matériaux
        myCursor.execute(queryComptaMateriel)
        if myCursor.fetchall() == []:
            for i in range(1, mois+1):
                ListePrixMATERIEL.append(0)
        else:
            myCursor.execute(queryComptaMateriel)
            for row in myCursor:
                for i in range(1, mois+1):
                    ListePrixMATERIEL.append(0)
                    if row[1] == i:
                        ListePrixMATERIEL[i-1] = row[0]
        myCursor.fetchall()
        ListePrixEmplacement = []

        # On vérifie que

        myCursor.execute(queryComptaEmplacement)
        if myCursor.fetchall() == []:
            for i in range(1, mois+1):
                ListePrixEmplacement.append(0)
        else:
            myCursor.execute(queryComptaEmplacement)
            for row in myCursor:
                for i in range(1, mois+1):
                    ListePrixEmplacement.append(0)
                    if row[1] == i:
                        ListePrixEmplacement[i-1] = row[0]
        myCursor.fetchall()
        # On récupère les salaires du staff et des chefs pour chaque mois écoulé de l'année
        myCursor.execute(queryComptaStaff)
        comptaStaff = myCursor.fetchall()[0][0]
        myCursor.execute(queryComptaChef)
        comptaChef = myCursor.fetchall()[0][0]

        ListeComptaTotal = []
        for i in range(1, mois+1):
            ListeComptaTotal.append(ListePrixMATERIEL[i-1])
            ListeComptaTotal[i-1] += ListePrixEmplacement[i-1]
            ListeComptaTotal[i-1] = float(ListeComptaTotal[i-1])
            ListeComptaTotal[i-1] -= (
                float(comptaStaff) + float(comptaChef))

        # On affiche les
        print("Bénéfices :\n================================================")
        for i in range(1, mois+1):
            ListeMois = ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                         "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
            print(ListeMois[i-1], ":", ListeComptaTotal[i-1], "€\n")
            if i != len(ListeMois):
                print("-------------")

        skip = "helo"
        while skip != "":
            skip = input("Appuyez sur enter pour continuer")

    elif choix == "profil":
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

        queryInfos = "SELECT Id_staff, Nom, Age, Salaire FROM view_Administration WHERE Id_staff = %s GROUP BY Id_staff"
        myCursor.execute(queryInfos, (Id_staff,))

        for Id_staff, Nom, Age, Salaire in myCursor:
            print("Id : %s\nNom : %s" % (Id_staff, Nom))
            # On affiche les prénoms stockés dans la liste prenomsListe en ligne
            print("Prénom(s) : %s" % (", ".join(prenomsListe)))
            print("Age : %s\nSalaire : %s \u20ac\n" % (Age, Salaire))
        myCursor.fetchall()

        print("Vos matériaux gérés : \n=========================")
        # On vérifie si l'admin gère un matériel
        queryMatériel = "SELECT Id_admin FROM MATERIEL WHERE Id_admin = %s"
        myCursor.execute(queryMatériel, (Id_admin,))
        if myCursor.fetchall() == []:
            print("Vous ne gérez aucun matériel\n")
        else:
            queryMatériel = "SELECT Id_mat, Materiel, Type_mat, Prix_mat, Etat FROM view_Administration WHERE Id_staff = %s GROUP BY Id_mat"
            myCursor.execute(queryMatériel, (Id_staff,))
            verif = 0
            for Id_mat, Materiel, Type_mat, Prix_mat, Etat in myCursor:
                if verif == 1:
                    print("\n=========================")
                print("Id : %s\nNom : %s\nPrix : %s \u20ac\nType : %s\nEtat : %s\n" %
                      (Id_mat, Materiel, Prix_mat, Type_mat, Etat))
                verif = 1
            myCursor.fetchall()

        print("Vos fiches_compta gérées : \n=========================")
        # On vérifie si l'admin gère une fiche_compta
        queryVerifFicheCompta = "SELECT Id_admin FROM FICHE_COMPTA WHERE Id_admin = %s"
        myCursor.execute(queryVerifFicheCompta, (Id_admin,))
        if myCursor.fetchall() == []:
            print("Vous ne gérez aucune fiche_compta\n")
        else:
            queryFicheCompta = "SELECT Id_fiche_compta, Date_fiche, Prix_total FROM view_Administration WHERE Id_staff = %s GROUP BY Id_fiche_compta"
            myCursor.execute(queryFicheCompta, (Id_staff,))
            verif = 0
            for Id_fiche_compta, Date_fiche, Prix_total in myCursor:
                if verif == 1:
                    print("\n=========================")
                print("Id : %s\nDate : %s\nBénéfices : %s \n" %
                      (Id_fiche_compta, Date_fiche, Prix_total))
                verif = 1
            myCursor.fetchall()

        skip = "helo"
        while skip != "":
            skip = input("Appuyez sur enter pour continuer")
        os.system("cls")

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
            main_admin(cnx, Id_Pers)

        # On vérifie que le client n'a pas de réservation en cours

        queryVerifResa = "SELECT Id_cli FROM loue_emplacement WHERE Id_cli = %s"
        myCursor.execute(queryVerifResa, (Id_cli,))

        if myCursor.fetchall() != []:
            # On update la date de fin de location à aujourd'hui
            queryUpdateDateFin = "UPDATE loue_emplacement SET Date_fin = CURDATE() WHERE Id_cli = %s"
            myCursor.execute(queryUpdateDateFin, (Id_cli,))
            cnx.commit()

        # On supprime l'équipe dont la personne fait partie
        # D'abord on récupère son Id_equipe
        queryGetIdEquipe = "SELECT Id_equipe FROM CLIENT WHERE Id_cli = %s"
        myCursor.execute(queryGetIdEquipe, (Id_cli,))
        Id_equipe = myCursor.fetchall()[0][0]

        if Id_equipe != None:

            # On vérifie si l'équipe est inscrite à un tournoi
            queryVerifTournoi = "SELECT Id_equipe FROM participe WHERE Id_equipe = %s"
            myCursor.execute(queryVerifTournoi, (Id_equipe,))

            if myCursor.fetchall() != []:
                # On supprime l'équipe du tournoi
                queryDeleteTournoi = "DELETE FROM participe WHERE Id_equipe = %s"
                myCursor.execute(queryDeleteTournoi, (Id_equipe,))
                cnx.commit()

            # On update tout sauf Id_cli et Id_pers à NULL
            querydeleteInfos = "UPDATE CLIENT SET Pays = 'Anonimized', Code_postal = -1, Con_Telephone = -1, Con_Email = 'Anonimized', Ville = 'Anonimized', Numero_de_maison = -1, Id_equipe = Null WHERE Id_cli = %s"
            myCursor.execute(querydeleteInfos, (Id_cli,))

            # On supprime l'équipe
            queryDeleteEquipe = "DELETE FROM EQUIPE WHERE Id_equipe = %s"
            myCursor.execute(queryDeleteEquipe, (Id_equipe,))
        else:
            querydeleteInfos = "UPDATE CLIENT SET Pays = 'Anonimized', Code_postal = -1, Con_Telephone = -1, Con_Email = 'Anonimized', Ville = 'Anonimized', Numero_de_maison = -1 WHERE Id_cli = %s"
            myCursor.execute(querydeleteInfos, (Id_cli,))

        cnx.commit()

        queryIdPers = "SELECT Id_pers FROM CLIENT WHERE Id_cli = %s"
        myCursor.execute(queryIdPers, (Id_cli,))
        Id_Pers = myCursor.fetchall()[0][0]
        # On supprime le client de la table PERSONNE donc tout sauf Id_pers à NULL
        querydeleteClient = "UPDATE PERSONNE SET Nom = 'Anonimized', Age = -1, Mot_de_passe = 'Anonimized' WHERE Id_Pers = %s"
        myCursor.execute(querydeleteClient, (Id_Pers,))
        cnx.commit()

        # On supprime le client de la table PRENOM donc tout sauf Id_pers à NULL
        querydeletePrenom = "UPDATE Prenom SET Prenom = 'Anonimized' WHERE Id_Pers = %s"
        myCursor.execute(querydeletePrenom, (Id_Pers,))
        cnx.commit()

        print("Le client a bien été supprimé !")
    main_admin(cnx, Id_Pers)
