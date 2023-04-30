from mysql.connector import (connection)


def initialisation():
    """
    Cette fonction permet d'initialiser la connexion à la base de données.

    Returns:
    --------
    cnx: mysql.connector.connection.MySQLConnection (Object)
    """
    cnx = connection.MySQLConnection(user='admin', password='admin',
                                     host='127.0.0.1',
                                     database='camping_physique')
    print("Connection ok")
    return cnx
