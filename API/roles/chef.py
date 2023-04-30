from time import sleep


def main_chef(user_state, cnx):

    print("Bienvenue dans la partie Chef de l'application !")

    if user_state == "Admin":
        user_state = 'ADMINISTRATION'
    elif user_state == "Cuisinier":
        user_state = "CUISINIER"
    elif user_state == "Animateur":
        user_state = 'ANIMATEUR'
    elif user_state == "Technicien":
        user_state = "TECHNICIEN"
    choix = "basic"

    while choix not in ("liste_employees", "supprimer_employee", "rajouter_employee", "exit"):
        choix = input(
            "Que voulez vous faire ? (liste_employees, supprimer_employee, rajouter_employee, exit) ")
        sleep(1)
    myCursor = cnx.cursor(prepared=True)
    if choix == "liste_employees":
        queryList = "SELECT P.Nom, Pre.Prenom, P.Age FROM PERSONNE P JOIN Prenom Pre ON P.Id_Pers = Pre.Id_Pers JOIN STAFF S ON P.Id_Pers = S.Id_Pers JOIN {} J ON S.Id_staff = J.Id_staff".format(
            user_state)
        myCursor.execute(queryList)
        print(myCursor.fetchall())
    else:
        print("Vous avez quitté l'application")
        sleep(1)
        exit()
