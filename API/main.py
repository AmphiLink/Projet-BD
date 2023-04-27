# Partie Deploy
from auth.authentification import login
from __init__ import initialisation


def main():
    cnx = initialisation()
    print("Bienvenue sur notre API Camping.\n")
    Authorized = login(cnx)
    cnx.close()


main()
