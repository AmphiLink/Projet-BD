from time import sleep


def main_cuisinier(cnx, Id_Pers):
    """
    Cette fonction permet d'utiliser les différentes fonctionnnalités de l'application en tant que cuisinier.

    Parameters:
    -----------
    cnx : mysql.connector.connection.MySQLConnection (Object)
    Id_Pers : l'Id de la personne conectée (int)
    """

    choix = "basic"
    while choix not in ("Cuisiner pour un tournoi", "Cuisiner pour un emplacement", "Arrêter de cuisiner pour un emplacement", "profil", "exit"):
        choix = input(
            "Que voulez vous faire ? (Cuisinier pour un tournoi, Cuisiner pour un emplacement, Arrêter de cuisiner pour un emplacement, profil, exit)\n ")
        sleep(1)

    if choix == "exit":
        print("Vous avez quitté l'application !")
        sleep(1)
        exit()

    myCursor = cnx.cursor(prepared=True)
    # On récupère l'IdStaff
    queryIdStaff = "Select Id_staff FROM STAFF where Id_Pers = %s"
    myCursor.execute(queryIdStaff, (Id_Pers,))
    Id_staff = myCursor.fetchall()[0][0]

    # On récupère l'id_cuis
    queryIdCuis = "SELECT Id_cuis FROM CUISINIER WHERE Id_staff = %s"
    myCursor.execute(queryIdCuis, (Id_staff,))
    Id_cuis = myCursor.fetchall()[0][0]

    if choix == "Cuisiner pour un tournoi":
        myCursor = cnx.cursor(prepared=True)
        Date_tournoi = input("Quelle est la date du tournoi ? (AAAA-MM-JJ) ")
        Heure = input("Quelle est l'heure du tournoi ? (HH:MM) ")
        Lieu = input("Quel est le lieu du tournoi ? ")

        if Date_tournoi == "exit" or Heure == "exit" or Lieu == "exit":
            print("Vous avez quitté l'application")
            sleep(1)
            exit()

        # On récupère l'id du tournoi en question
        queryIdTournoi = "SELECT Id_tournoi FROM TOURNOI WHERE Date_tournoi = %s AND Heure = %s AND Lieu = %s"
        myCursor.execute(queryIdTournoi, (Date_tournoi, Heure, Lieu))
        Id_tournoi = myCursor.fetchall()

        if Id_tournoi == []:
            print("Ce tournoi n'existe pas !")
            sleep(1)
            main_cuisinier(cnx, Id_Pers)
        Id_tournoi = Id_tournoi[0][0]

        # On vérifie si un cuisinier est présent dans la table cuisine en général
        queryIdCuis = "SELECT Id_cuis FROM cuisine WHERE Id_cuis = %s"
        myCursor.execute(queryIdCuis, (Id_cuis,))
        VerifIdCuis = myCursor.fetchall()
        if VerifIdCuis == []:
            # Si non pas de souci à se faire on insère les données
            queryAddCuisTournoi = "INSERT INTO cuisine (Id_cuis, Id_tournoi) VALUES(%s, %s)"
            myCursor.execute(queryAddCuisTournoi, (Id_cuis, Id_tournoi))
        else:
            # Si oui il faut vérifier si ce cuisine pour des tournois
            query = "SELECT Id_tournoi FROM cuisine WHERE Id_cuis = %s"
            myCursor.execute(query, (Id_cuis,))
            VerifIdTournoi = myCursor.fetchall()[0][0]

            if VerifIdTournoi == None:
                # Si non cela veut dire que le cuisinier cuisine pour un emplacement on fait donc un update
                queryAddCuisTournoi = "UPDATE cuisine SET Id_tournoi = %s WHERE Id_cuis = %s"
                myCursor.execute(queryAddCuisTournoi)
            else:
                # Si oui on insère une nouvelle colonne en reprenant l'id de l'emplacement pour lequel le cuisinier cuisine
                queryIdEmplacement = "SELECT Id_emplacement FROM cuisine WHERE Id_cuis = %s"
                myCursor.execute(queryIdEmplacement, (Id_cuis,))
                Id_emplacement = myCursor.fetchall()[0][0]

                queryAddCuisTournoi = "INSERT INTO cuisine (Id_emplacement, Id_cuis, Id_tournoi) VALUES(%s, %s, %s)"
                myCursor.execute(queryAddCuisTournoi,
                                 (Id_emplacement, Id_cuis, Id_tournoi))
        cnx.commit()
        main_cuisinier(cnx, Id_Pers)

    elif choix == "Cuisiner pour un emplacement":
        myCursor = cnx.cursor(prepared=True)
        bungalow = input(
            "Pour quel emplacement voulez-vous cuisiner (N° d'emplacement) ? ")
        if bungalow == "exit":
            print("Vous avez quitté l'application")
            sleep(1)
            exit()

        # On récupère l'id de l'emplacement en question
        queryIdEmplacement = "SELECT Id_emplacement from EMPLACEMENT WHERE Id_emplacement = %s"
        myCursor.execute(queryIdEmplacement, (bungalow,))
        Id_emplacement = myCursor.fetchall()[0][0]

        # On vérifie si un cuisinier est présent dans la table cuisine en général
        queryIdCuis = "SELECT Id_cuis FROM cuisine WHERE Id_cuis = %s"
        myCursor.execute(queryIdCuis, (Id_cuis,))
        VerifIdCuis = myCursor.fetchall()
        if VerifIdCuis == []:
            # Si non pas de souci à se faire on insère les données
            queryAddCuisEmplacement = "INSERT INTO cuisine (Id_cuis, Id_emplacement) VALUES(%s, %s)"
        else:
            # Si oui il faut vérifier si ce cuisininier cuisine pour des tournois
            query = "SELECT Id_tournoi FROM cuisine WHERE Id_cuis = %s"
            myCursor.execute(query, (Id_cuis,))
            VerifIdTournoi = myCursor.fetchall()[0][0]

            if VerifIdTournoi == None:
                # Si non cela veut dire que le cuisinier cuisine pour un emplacement or il ne peut pas
                print("Vous cuisinez déjà pour un emplacement !")
                sleep(1)
                main_cuisinier(cnx, Id_Pers)
            else:
                # On vérifie quand même si le cuisinier cuisine pour un emplacement
                queryIdEmplacement = "SELECT Id_emplacement FROM cuisine WHERE Id_cuis = %s"
                myCursor.execute(queryIdEmplacement, (Id_cuis,))
                VerifIdEmplacement = myCursor.fetchall()[0][0]
                if VerifIdEmplacement == None:
                    # Si non cela veut dire que le cuisinier cuisine pour un tournoi on fait donc un update
                    queryAddCuisEmplacement = "UPDATE cuisine SET Id_emplacement = %s WHERE Id_cuis = %s"
                else:
                    # Si oui cela veut dire que le cuisinier cuisine pour un emplacement or il ne peut pas
                    print("Vous cuisinez déjà pour un emplacement !")
                    sleep(1)
                    main_cuisinier(cnx, Id_Pers)
        myCursor.execute(queryAddCuisEmplacement,
                         (Id_emplacement, Id_cuis))
        cnx.commit()

        # On met à jour l'emplacement
        queryUpdateEmplacement = "UPDATE EMPLACEMENT SET Cuisinier = true"
        myCursor.execute(queryUpdateEmplacement)
        cnx.commit()
        main_cuisinier(cnx, Id_Pers)

    elif choix == "Arrêter de cuisiner pour un emplacement":
        myCursor = cnx.cursor(prepared=True)

        # On vérifie si un cuisinier est présent dans la table cuisine en général
        queryIdCuis = "SELECT Id_cuis FROM cuisine WHERE Id_cuis = %s"
        myCursor.execute(queryIdCuis, (Id_cuis,))
        VerifIdCuis = myCursor.fetchall()

        if VerifIdCuis != []:
            # On vérifie si le cuisinier travaille bien dans un emplacement
            queryId_cuis = "SELECT Id_cuis FROM cuisine WHERE Id_cuis = %s AND Id_emplacement != 'None'"
            myCursor.execute(queryId_cuis, (Id_cuis,))

            if myCursor.fetchall() == []:
                print("Vous ne travaillez pour aucun emplacement !")
                main_cuisinier(cnx, Id_Pers)
            else:
                print("Veuillez vérifier votre profil afin de regarder le numéro d'identification de l'emplacement pour lequel vous travaillez")
                Id_emplacement = input(
                    "Saisissez le numéro du bungalow pour lequel vous arrêtez de cuisiner ")

                # On cast l'Id_emplacement en int
                Id_emplacement = int(Id_emplacement)
                if Id_emplacement == "exit":
                    print("Vous avez quitté l'application")
                    sleep(1)
                    exit()

                # On vérifie si l'Id_emplacement existe bien
                queryIdEmplacement = "SELECT Id_emplacement FROM EMPLACEMENT WHERE Id_emplacement = %s"
                myCursor.execute(queryIdEmplacement, (Id_emplacement,))
                VerifIdEmplacement = myCursor.fetchall()

                if VerifIdEmplacement == []:
                    print("Cet emplacement n'existe pas !")
                    main_cuisinier(cnx, Id_Pers)

                # On vérifie si le cuisinier cuisine pour un tournoi
                myCursor = cnx.cursor(prepared=True)
                query = "SELECT Id_tournoi FROM cuisine WHERE Id_cuis = %s"
                myCursor.execute(query, (Id_cuis,))
                VerifIdTournoi = myCursor.fetchall()[0][0]

                if VerifIdTournoi == None:

                    # On supprime la cuisine
                    queryDelCuis = "DELETE Id_cuisine FROM cuisine WHERE Id_emplacement = %s"
                else:
                    # On supprime seulement l'emplacement
                    queryDelCuis = "UPDATE cuisine SET Id_emplacement = NULL where Id_emplacement = %s"

                myCursor.execute(
                    queryDelCuis, (Id_emplacement,))
                cnx.commit()

                # On met à jour l'emplacement
                queryUpdateEmplacement = "UPDATE EMPLACEMENT SET Cuisinier = false"
                myCursor.execute(queryUpdateEmplacement)
                cnx.commit()
                print(
                    "Vous avez arrêté de cuisiner pour cet emplacement et le statut de l'emplacement a été mis à jour")
                main_cuisinier(cnx, Id_Pers)
        else:
            print("Vous ne travaillez pour aucun emplacement !")
            main_cuisinier(cnx, Id_Pers)
