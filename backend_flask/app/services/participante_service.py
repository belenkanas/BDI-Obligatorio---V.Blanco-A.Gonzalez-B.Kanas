from app.database.conexion_db import conexion

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


def obtener_participantes_permitidos(id_sala):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT tipo_sala FROM sala WHERE id_sala = %s", (id_sala,))
    sala = cursor.fetchone()
    tipo_sala = sala["tipo_sala"]

    if tipo_sala == "docente":
        query = """
            SELECT p.*
            FROM participante p
            JOIN participante_programa_academico ppa ON p.ci = ppa.ci_participante
            WHERE ppa.rol = 'docente'
        """
    elif tipo_sala == "posgrado":
        query = """
            SELECT p.*
            FROM participante p
            JOIN participante_programa_academico ppa ON p.ci = ppa.ci_participante
            JOIN programa_academico pa ON ppa.id_programa = pa.id_programa
            WHERE ppa.rol = 'alumno'
              AND pa.tipo = 'posgrado'
        """
    else:
        query = "SELECT * FROM participante"

    cursor.execute(query)
    participantes = cursor.fetchall()

    conn.close()
    return participantes