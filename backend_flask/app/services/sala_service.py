from app.database.conexion_db import conexion

def listar_salas():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            s.id_sala,
            s.nombre_sala,
            s.capacidad,
            s.tipo_sala,
            e.id_edificio,
            e.nombre_edificio
        FROM sala s
        JOIN edificio e ON s.id_edificio = e.id_edificio
    """)

    salas = cursor.fetchall()
    conn.close()

    return salas



def obtener_sala(nombre_sala):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM sala WHERE nombre_sala = %s", (nombre_sala,))

    sala = cursor.fetchone()
    conn.close()

    return sala


def agregar_sala(nombre_sala, id_edificio, capacidad, tipo_sala):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM sala 
        WHERE nombre_sala = %s AND id_edificio = %s
    """, (nombre_sala, id_edificio))

    if cursor.fetchone():
        conn.close()
        return None, "La sala ya existe en ese edificio"

    cursor.execute("""
        INSERT INTO sala (nombre_sala, id_edificio, capacidad, tipo_sala)
        VALUES (%s, %s, %s, %s)
    """, (nombre_sala, id_edificio, capacidad, tipo_sala))

    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()

    return {
        "id_sala": nuevo_id,
        "nombre_sala": nombre_sala,
        "id_edificio": id_edificio,
        "capacidad": capacidad,
        "tipo_sala": tipo_sala
    }, "Sala creada exitosamente"



def eliminar_sala(nombre_sala):
    conn = conexion()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM sala WHERE nombre_sala = %s", (nombre_sala,))

    conn.commit()
    filas = cursor.rowcount
    conn.close()

    return filas > 0
