from time import sleep


def main_cuisinier(cnx, Id_Pers):
    """
    Cette fonction permet d'utiliser les différentes fonctionnnalités de l'application en tant que cuisinier.
    Ce rôle est reservé aux FEMMES (Alexis tu claques)

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
        Id_tournoi = myCursor.fetchall()[0][0]

        # On récupère le potentiel Id_emplacement
        queryIdEmplacementPrime = "SELECT Id_emplacement FROM cuisine WHERE Id_cuis = %s"
        myCursor.execute(queryIdEmplacementPrime, (Id_cuis,))
        Id_emplacement = myCursor.fetchall[0][0]

        queryCusinierVerif = "SELECT Id_cuis FROM cuisine WHERE Id_cuis = %s"
        myCursor.execute(queryCusinierVerif, (Id_cuis,))
        VerifIdCuis = myCursor.fetchall()[0][0]
        # On vérifie si un cuisinier cuisine déjà pour un tournoi OU un emplacement
        if VerifIdCuis == None:
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
                queryAddCuisTournoi = "INSERT INTO cuisine (Id_emplacement, Id_cuis, Id_tournoi) VALUES(%s, %s, %s)"
                myCursor.execute(queryAddCuisTournoi,
                                 (Id_emplacement, Id_cuis, Id_tournoi))
        cnx.commit()

    elif choix == "Cuisiner pour un emplacement":
        myCursor = cnx.cursor(prepared=True)

        # On vérifie si le cuisinier ne travaille pas déjà pour un emplacement
        queryIdEmplacementPrime = "SELECT Id_emplacement FROM cuisine WHERE Id_cuis = %s"
        myCursor.execute(queryIdEmplacementPrime, (Id_cuis,))
        Id_emplacementPrime = myCursor.fetchall()[0][0]
        queryIdEmplacementPrime = "SELECT Id_emplacement FROM cuisine WHERE Id_cuis = %s AND  Id_tournoi = None"
        myCursor.execute(queryIdEmplacementPrime, (Id_cuis,))
        Id_emplacementPrimeTournoi = myCursor.fetchall()[0][0]
        if Id_emplacementPrime == None and Id_emplacementPrimeTournoi == None:
            bungalow = input(
                "Pour quel emplacement voulez-vous cuisiner (N° d'emplacement) ? ")
            if bungalow == "exit":
                print("Vous avez quitté l'application")
                sleep(1)
                exit()

            # On récupère l'id de l'emplacement en question
            queryIdEmplacement = "SELECT Id_emplacement from EMPLACEMENT WHERE Id_emplacement = %s"
            myCursor.execute(queryIdEmplacement, (bungalow,))
            Id_emplacement = myCursor.fetchall[0][0]

            # On vérifie si le cuisinier cuisine déjà pour un tournoi
            queryVerifTournoi = "SELECT Id_tournoi FROM cuisine WHERE Id_cuis = %s"
            myCursor.execute(queryVerifTournoi, (Id_tournoi,))
            IdVerifTournoi = myCursor.fetchall()[0][0]
            if IdVerifTournoi == None:
                # Si non pas de problème on insère les données
                queryAddCuisEmplacement = "INSERT INTO cuisine (Id_emplacement, Id_cuis) VALUES(%s, %s)"
            else:
                # Si oui on update la table cuisine
                queryAddCuisEmplacement = "UPDATE cuisine SET Id_emplacement = %s WHERE Id_cuis = %s"
            myCursor.execute(queryAddCuisEmplacement,
                             (Id_emplacement, Id_cuis))
            cnx.commit()

            # On met à jour l'emplacement
            queryUpdateEmplacement = "UPDATE EMPLACEMENT SET Cuisinier = True"
            myCursor.execute(queryUpdateEmplacement)
            cnx.commit()
        else:
            print("Vous cuisinez déjà pour un emplacement ! Vous ne pouvez cuisiner que pour un emplacement à la fois")
            main_cuisinier(cnx, Id_Pers)

    else:
        print("Vous avez quitté l'application")
        sleep(1)
        exit()
