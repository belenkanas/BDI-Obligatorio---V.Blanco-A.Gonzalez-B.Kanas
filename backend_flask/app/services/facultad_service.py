from app.database.conexion_db import conexion

def listar_facultades():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM facultad")

    facultades = cursor.fetchall()
    conn.close()

    return facultades


def obtener_facultad(id_facultad):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM facultad WHERE id_facultad = %s", (id_facultad,))

    facultad = cursor.fetchone()
    conn.close()

    return facultad


def agregar_facultad(nombre):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM facultad WHERE nombre = %s", (nombre,))

    if cursor.fetchone():
        conn.close()
        return None, "La facultad ya existe"

    cursor.execute("""
        INSERT INTO facultad (nombre)
        VALUES (%s)
    """, (nombre,))

    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()

    return {"id_facultad": nuevo_id, "nombre": nombre}, "Facultad creada exitosamente"


def eliminar_facultad(id_facultad):
    conn = conexion()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM facultad WHERE id_facultad = %s", (id_facultad,))

    conn.commit()
    filas = cursor.rowcount
    conn.close()

    return filas > 0
