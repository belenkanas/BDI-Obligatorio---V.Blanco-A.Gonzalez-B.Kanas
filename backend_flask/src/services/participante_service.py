from database.obligatorio import conexion

def listar_participantes():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM participante")
    
    participantes = cursor.fetchall()
    conn.close()
    
    return participantes


def obtener_participante(ci):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM participante WHERE ci = %s", (ci,))
    
    participante = cursor.fetchone()
    conn.close()
    
    return participante


def agregar_participante(ci, nombre, apellido, email):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM participante WHERE ci = %s", (ci,))

    if cursor.fetchone():
        conn.close()
        return None, "El participante ya existe"

    cursor.execute("""INSERT INTO participante (ci, nombre, apellido, email) 
                        VALUES (%s, %s, %s, %s)""", (ci, nombre, apellido, email))
    
    conn.commit()
    conn.close()

    return {"ci": ci, "nombre": nombre, "apellido": apellido, "email": email}, "Participante creado exitosamente"


def eliminar_participante(ci):
    conn = conexion()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM participante WHERE ci = %s", (ci,))
    
    conn.commit()
    filas = cursor.rowcount
    conn.close()

    return filas > 0