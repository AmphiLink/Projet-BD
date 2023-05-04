from time import sleep


def main_animateur(cnx, Id_pers):
    """
    Cette fonction permet d'utiliser les différentes fonctionnnalités de l'application en tant qu'animateur.

    Parameters:
    -----------
    user_state: le job de l'utilisateur concerné (str)
    cnx : mysql.connector.connection.MySQLConnection (Object)
    Id_Pers : l'Id de la personne concernée (int)
    """

    choix = "basic"
    while choix not in ("liste_activités", "rajouter une compétence", "profil", "exit"):
        choix = input(
            "Que voulez vous faire ? (liste_activités, rajouter une compétence, profil, exit) ")
        sleep(1)

    if choix == "liste_activités":
        myCursor = cnx.cursor(prepared=True)
        queryList = "SELECT Id_type_acti, Nom, Prix, Taille_min_, Age_min FROM TYPE_ACTI"
        myCursor.execute(queryList)
        for Id_type_acti, Nom, Prix, Taille_min_, Age_min in myCursor:
            print("%s :  %s, Prix : %s, Taille_min : %s, Age_min :  %s" %
                  (Id_type_acti, Nom, Prix, Taille_min_, Age_min))
    elif choix == "rajouter une compétence":
        print("\nChoisissez une compétence à rajouter en tapant le numéro correspondant : ")
        NewJob = input(
            "1 : Basketball 6 : Ski-nautique\n2 : Football   7 : Escalade\n3 :Badminton  8 : Mini-Golf\n4 : Volleyball 9 : Club enfants\n5 : Spa        10 : Plongée\n")
        myCursor = cnx.cursor(prepared=True)
        queryAdd = "INSERT INTO peut_faire (Id_anim, Id_type_acti) VALUES (%s, %s)"
        myCursor.execute(queryAdd, (Id_pers, NewJob))
