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
    while choix not in ("Reserver du matériel", "Louer un emplacement", "Rejoindre/Créer une équipe", "Voir la liste des activités", "S'inscrire à une activité", "S'inscrire à un tournoi" "profil", "exit", "1", "2", "3", "4", "5", "6", "7"):
        choix = input("\nQue voulez vous faire ?\n 1: Reservé du matériel\n 2: Loué un emplacement\n 3: Rejoindre/Créer une équipe\n 4: Voir la liste des activités\n 5: S'inscrire à une activité\n 6: S'inscrire à un tournoi\n 7: profil\n 8: exit\n")
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
        liste_activités(cnx, Id_pers)

    elif choix == "S'inscrire à une activité" or choix == "5":
        inscrire_activite(cnx, Id_pers)

    elif choix == "S'inscrire à un tournoi" or choix == "6":
        inscrire_tournoi(cnx, Id_pers)

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
        sleep(2)
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
    query = "SELECT Id_type_acti, Nom FROM TYPE_ACTI"
    mycursor.execute(query)
    resultats = mycursor.fetchall()
    # On affiche les activités disponibles
    os.system("cls")
    print("\nVoici la liste des activités disponibles: \n")
    for resultat in resultats:
        Id_type_acti = resultat[0]
        Nom = resultat[1]
        print(" Id:", Id_type_acti, "\n", "Nom:", Nom, "\n")

    # Pour obtenir plus d'informations sur une activité
    type_activity_id = input("Si vous voulez plus d'informations sur une activité, entrez son Id, sinon entrez 'back' pour revenir au menu principal \n")
    # Si le client veut revenir au menu principal
    if type_activity_id == "back":
        main_client(cnx, Id_pers)
    if type_activity_id == "exit":
        print("Vous avez quitté l'application")
        sleep(1)
        exit()
    # Si le client veut plus d'informations sur une activité
    else:
        queryInfo = "SELECT Id_type_acti, Nom, Prix, Taille_min_, Age_min FROM TYPE_ACTI WHERE Id_type_acti = %s"
        mycursor.execute(queryInfo, (type_activity_id,))
        resultats = mycursor.fetchall()
        for resultat in resultats:
            Id_type_acti = resultat[0]
            Nom = resultat[1]
            Prix = resultat[2]
            Taille_min_ = resultat[3]
            Age_min = resultat[4]
            os.system("cls")
            print(" Id:",Id_type_acti,"\n", "Nom:",Nom,"\n", "Prix:",Prix,"\n", "Taille minimum:",Taille_min_,"\n", "Age minimum:",Age_min)        
        # On affiche les informations sur l'activité
        queryInfo = "SELECT Date_acti, Heure, Lieu FROM ACTIVITE WHERE Id_type_acti = %s"
        mycursor.execute(queryInfo, (type_activity_id,))
        resultatInfo = mycursor.fetchall()
        for resultat in resultatInfo:
            Date = resultat[0]
            Heure = resultat[1]
            Lieu = resultat[2]
            print(" Date:",Date,"\n", "Heure:",Heure, "\n", "Lieu:",Lieu, "\n")

    # Si le client veut s'inscrire à une activité
    activity_id = input("Pour selectionner cette activité, entrez son Id, sinon entrez 'back' pour revenir au menu principal \n")
    os.system("cls")
    query = "SELECT Id_acti FROM ACTIVITE WHERE Id_type_acti = %s"
    mycursor.execute(query, (activity_id,))
    resultats = mycursor.fetchall()
    if activity_id == "back":
        main_client(cnx, Id_pers)
    if activity_id == "exit":
        print("Vous avez quitté l'application")
        sleep(1)
        exit()
    if activity_id not in resultats:
        print("L'Id entré n'est pas valide, veuillez réessayer")
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

def inscrire_tournoi(cnx, Id_pers):
    """
    NE FONCTIONNE PAS ENCORE !!!!
    Cette fonction permet d'inscrire un client à un tournoi.

    """
    # On vérifie si le client possède une équipe
    mycursor = cnx.cursor(prepared=True)
    query = "SELECT Id_equipe FROM CLIENT WHERE Id_Pers = %s"
    mycursor.execute(query, (Id_pers,))
    Id_equipe = mycursor.fetchall()[0][0]
    if Id_equipe == None:
        print("Vous n'avez pas d'équipe, veuillez en créer une")
        sleep(2)
        rejoindre_equipe(cnx, Id_pers)
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
        tournoi_id = input("Si vous voulez plus d'informations sur un tournoi, entrez son Id, sinon entrez 'back' pour revenir au menu principal \n")
                
        # On vérifie que l'Id entré est valide
        query = "SELECT Id_tournoi FROM TOURNOI WHERE Id_tournoi = %s"
        mycursor.execute(query, (tournoi_id,))
        resultats = mycursor.fetchall()
        if not resultats:
            os.system("cls")
            print("L'Id entré n'est pas valide, veuillez réessayer")
            sleep(2)
            inscrire_tournoi(cnx, Id_pers)   
        
        if tournoi_id == "back":
            main_client(cnx, Id_pers)
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
            print(" Id:",Id_tournoi,"\n","Nom:",Nom,"\n","Date_tournoi:",Date_tournoi,"\n", "Heure:",Heure,"\n", "Lieu:",Lieu,"\n", "Prix:",Prix)    

        # Si le client veut s'inscrire à un tournoi
        tournoi_id = input("\nPour selectionner ce tournoi, entrez son Id, sinon entrez 'back' pour revenir au menu principal \n")
        os.system("cls")
        query = "SELECT Id_tournoi FROM TOURNOI WHERE Id_tournoi = %s"
        mycursor.execute(query,(tournoi_id,))
        resultats = mycursor.fetchall()

        # Si le client veut revenir en arrière
        if tournoi_id == "back":
            inscrire_tournoi(cnx, Id_pers)

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
            inscrire_tournoi(cnx, Id_pers)  
        
        else:
            # On récupère l'Id de l'équipe du client
            query = "SELECT Id_equipe FROM CLIENT WHERE Id_Pers = %s"
            mycursor.execute(query, (Id_pers,))
            Id_equipe = mycursor.fetchall()[0][0]

            # On INSERT dans la table PARTICIPE
            query = "INSERT INTO participe (Id_equipe, Id_tournoi) VALUES (%s, %s)"
            mycursor.execute(query, (Id_equipe, tournoi_id))
            cnx.commit()
            print("Vous êtes bien inscrit au tournoi !")
            
def profil(cnx, Id_pers):
    """
    A MODIFIER AVEC LES VUES
    Cette fonction permet d'afficher le profil d'un client.
    """
    # Si le client veut modifier son profil
    os.system("cls")
    print("Si vous voulez modifier votre profil, entrez 'modif', sinon entrez 'back' pour revenir au menu principal")
    choix = input()
    query = "SELECT ... FROM VIEW .... WHERE Id_Pers = %s"
    mycursor.execute(query, (Id_pers,))
    resultats = mycursor.fetchall()
    if choix == "modif":
        print("Quel champ voulez-vous modifier ?")
        for resultat in resultats:
            print(resultat)
        champ = input()
        print("Quelle valeur voulez-vous mettre ?")
        valeur = input()
        query = "UPDATE CLIENT SET %s = %s WHERE Id_Pers = %s"
        mycursor.execute(query, (champ, valeur, Id_pers))
        cnx.commit()
        print("Votre profil a bien été modifié !")
        sleep(2)
        main_client(cnx, Id_pers)
