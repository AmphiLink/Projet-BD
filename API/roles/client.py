import os
from time import sleep


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
    while choix not in ("Reservé matériel", "Loué un emplacement", "Rejoindre une équipe", "Voir la liste des activités", "S'inscrire à une activité",  "profil", "exit", "1", "2", "3"):
        choix = input(
            "\nQue voulez vous faire ?\n (1: , 2: profil, 3: exit)\n ")
        os.system("cls")

    if choix == "exit" or choix == "3":
        print("Vous avez quitté l'application !")
        sleep(1)
        exit()
