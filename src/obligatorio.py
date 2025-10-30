import mysql.connector

def conexion():
  return mysql.connector.connect(user='root', 
                                 password='rootpassword',
                                 host='127.0.0.1',
                                 database='obligatorio')


def listar_participantes():
  cnx = conexion()
  cursor = cnx.cursor()

  query = ("SELECT * FROM participante")

  cursor.execute(query)
  print("\n--- Lista de Usuarios ---")
  for (ci, nombre, apellido, email) in cursor:
        print(f"{ci} - {nombre} {apellido} ({email})")
  cursor.close()
  cnx.close()

def menu():
    while True:
        print("\nSeleccione una opción:")
        print("1. Listar Participantes")
        opcion = input("Ingrese el número de la opción deseada: ")
        if opcion == '1':
            listar_participantes()
        else:
                print("Opción inválida, intenta de nuevo.")

if __name__ == "__main__":
    menu()