from mysql.connector import (connection)

cnx = connection.MySQLConnection(user='admin', password='admin',
                                 host='127.0.0.1',
                                 database='camping_physique')
print("Connection ok")
cursor = cnx.cursor()
query = ("SELECT * FROM FICHE_COMPTA")
cursor.execute(query)
for (Id_fiche_compta, Date, Prix_total) in cursor:
    print("{}, {} , {}".format(
        Id_fiche_compta, Date, Prix_total))
cnx.close()
