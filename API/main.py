# Partie Deploy
from auth.authentification import main_auth
from __init__ import initialisation


def main():
    cnx = initialisation()
    print("Bienvenue sur notre API Camping.\n")
    Authorized = main_auth(cnx, Authorized=False)
    cnx.close()


main()
