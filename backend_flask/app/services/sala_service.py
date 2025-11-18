from app.database.conexion_db import conexion

def listar_salas():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM sala")

    salas = cursor.fetchall()
    conn.close()

    return salas


def obtener_sala(id_sala):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM sala WHERE id_sala = %s", (id_sala,))

    sala = cursor.fetchone()
    conn.close()

    return sala


def agregar_sala(nombre_sala, edificio, capacidad, tipo_sala):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM sala WHERE nombre_sala = %s AND edificio = %s",
                   (nombre_sala, edificio))

    if cursor.fetchone():
        conn.close()
        return None, "La sala ya existe en ese edificio"

    cursor.execute("""
        INSERT INTO sala (nombre_sala, edificio, capacidad, tipo_sala)
        VALUES (%s, %s, %s, %s)
    """, (nombre_sala, edificio, capacidad, tipo_sala))

    conn.commit()
    conn.close()

    return {
        "nombre_sala": nombre_sala,
        "edificio": edificio,
        "capacidad": capacidad,
        "tipo_sala": tipo_sala
    }, "Sala creada exitosamente"


def eliminar_sala(id_sala):
    conn = conexion()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM sala WHERE id_sala = %s", (id_sala,))

    conn.commit()
    filas = cursor.rowcount
    conn.close()

    return filas > 0
