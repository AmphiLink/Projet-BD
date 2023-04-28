# Partie Deploy
from auth.authentification import main_auth
from __init__ import initialisation


def main():
    cnx = initialisation()
    print("Bienvenue sur notre API Camping.\n")
    chef_state, user_state = main_auth(cnx, Authorized=False)

    print("Vous êtes connecté en tant que {} et vous êtes chef {}.".format(
        user_state, chef_state))
    cnx.close()


main()
