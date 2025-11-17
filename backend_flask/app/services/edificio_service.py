from app.database.conexion_db import conexion

def listar_edificios():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM edificio")

    edificios = cursor.fetchall()
    conn.close()

    return edificios


def obtener_edificio(nombre_edificio):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM edificio WHERE nombre_edificio = %s",
                   (nombre_edificio,))

    edificio = cursor.fetchone()
    conn.close()

    return edificio


def agregar_edificio(nombre_edificio, direccion, departamento):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM edificio WHERE nombre_edificio = %s",
                   (nombre_edificio,))

    if cursor.fetchone():
        conn.close()
        return None, "El edificio ya existe"

    cursor.execute("""
        INSERT INTO edificio (nombre_edificio, direccion, departamento)
        VALUES (%s, %s, %s)
    """, (nombre_edificio, direccion, departamento))

    conn.commit()
    conn.close()

    return {
        "nombre_edificio": nombre_edificio,
        "direccion": direccion,
        "departamento": departamento
    }, "Edificio creado exitosamente"


def eliminar_edificio(nombre_edificio):
    conn = conexion()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM edificio WHERE nombre_edificio = %s",
                   (nombre_edificio,))

    conn.commit()
    filas = cursor.rowcount
    conn.close()

    return filas > 0
