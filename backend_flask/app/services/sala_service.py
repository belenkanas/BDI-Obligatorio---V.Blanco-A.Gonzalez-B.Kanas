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


def agregar_sala(nombre_sala, id_edificio, capacidad, tipo_sala):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM sala WHERE nombre_sala = %s AND id_edificio = %s",
                   (nombre_sala, id_edificio))

    if cursor.fetchone():
        conn.close()
        return None, "La sala ya existe en ese edificio"

    cursor.execute("""
        INSERT INTO sala (nombre_sala, id_edificio, capacidad, tipo_sala)
        VALUES (%s, %s, %s, %s)
    """, (nombre_sala, id_edificio, capacidad, tipo_sala))

    conn.commit()
    conn.close()

    return {
        "nombre_sala": nombre_sala,
        "id_edificio": id_edificio,
        "capacidad": capacidad,
        "tipo_sala": tipo_sala
    }, "Sala creada exitosamente"


def eliminar_sala(id_sala):
    conn = conexion()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE rp FROM reserva_participante rp
            JOIN reserva r ON rp.id_reserva = r.id_reserva
            WHERE r.id_sala = %s
        """, (id_sala,))

        cursor.execute("DELETE FROM reserva WHERE id_sala = %s", (id_sala,))

        cursor.execute("DELETE FROM sala WHERE id_sala = %s", (id_sala,))

        conn.commit()
        return cursor.rowcount > 0

    except Exception as e:
        conn.rollback()
        print("ERROR al borrar sala:", e)
        return False

    finally:
        conn.close()
