import mysql.connector

cnx = mysql.connector.connect(
    user='root',
    password='rootpassword',
    host='127.0.0.1',
    database='obligatorio')

cursor = cnx.cursor()
query = ("SELECT * FROM Usuario")

cursor.execute(query)

for el in cursor:
    print(el)

cnx.close()