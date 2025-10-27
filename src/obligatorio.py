import mysql.connector 

def conexion():
  return mysql.connector.connect(user='root', 
                                 password='rootpassword',
                                 host='127.0.0.1',
                                 database='obligatorio')
