from mysql.connector import (connection)


def initialisation():
    cnx = connection.MySQLConnection(user='admin', password='admin',
                                     host='127.0.0.1',
                                     database='camping_physique')
    print("Connection ok")
    return cnx
