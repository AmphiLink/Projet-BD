# Partie Deploy
from auth.authentification import login
from __init__ import initialisation


def main():
    cnx = initialisation()
    print("Bienvenue sur notre API Camping. Vous pouvez quitter à nimporte quel moment en tapant 'exit'\n")
    Authorized = login(cnx)
    if Authorized != False:
        Operation = input("Que voulez-vous faire ?")
    print("Hate de vous revoir prochainement")
    return False


main()
