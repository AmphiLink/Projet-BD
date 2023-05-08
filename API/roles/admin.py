from time import sleep


def main_admin(cnx, Id_pers):
    choix = "basic"
    while choix not in ("gérer une fiche compta", "rajouter un matériel", "gérer un matériel", "liste des clients", "profil", "exit"):
        choix = input(
            "Que voulez vous faire ? (gérer une fiche compta, rajouter un matérieL? gérer un matériel, liste des clients, profil, exit) ")
        sleep(1)

    myCursor = cnx.cursor()
    # On récupère l'Id_staff
    queryIdStaf = ("SELECT Id_staff FROM STAFF WHERE Id_pers = %s")
    myCursor.execute(queryIdStaf, (Id_pers,))
    Id_staff = myCursor.fetchall()[0][0]

    # On récupère l'IdAdmin
    queryIdAdmin = ("SELECT Id_admin FROM ADMIN WHERE Id_staff = %s")
    myCursor.execute(queryIdAdmin, (Id_staff,))
    Id_admin = myCursor.fetchall()[0][0]

    if choix == "gérer une fiche compta":
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
        queryVerifIdFiche = "SELECT Id_fiche_compta WHERE Id_fiche_compta = %s"
        myCursor.execute(queryVerifIdFiche, (Id_fiche_compta,))
        myCursor.fetchall()

        if myCursor == []:
            print("Cette fiche n'existe pas où est déjà gérée !")
            main_admin(cnx, Id_pers)

        # On insère l'Id_admin dans la table FICHE_COMPTA
        queryGereFiche = "INSERT INTO FICHE_COMPTA (Id_admin) VALUES (%s) WHERE Id_fiche_compta = %s"
        myCursor.execute(queryGereFiche, (Id_admin, Id_fiche_compta))
        cnx.commit()
    return 0
