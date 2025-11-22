from app.database.conexion_db import conexion

def listar_edificios():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM edificio")

    edificios = cursor.fetchall()
    conn.close()

    return edificios


def obtener_edificio(id_edificio):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM edificio WHERE id_edificio = %s",
                   (id_edificio,))

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


def eliminar_edificio(id_edificio):
    conn = conexion()
    cursor = conn.cursor()

    try:
        # 1) Obtener salas
        cursor.execute("SELECT id_sala FROM sala WHERE id_edificio = %s", (id_edificio,))
        salas = cursor.fetchall()

        for (id_sala,) in salas:

            # 1a) Borrar asistencias
            cursor.execute("""
                DELETE a FROM asistencia a
                JOIN reserva r ON a.id_reserva = r.id_reserva
                WHERE r.id_sala = %s
            """, (id_sala,))

            # 1b) Borrar rp
            cursor.execute("""
                DELETE rp FROM reserva_participante rp
                JOIN reserva r ON rp.id_reserva = r.id_reserva
                WHERE r.id_sala = %s
            """, (id_sala,))

            # 1c) Borrar reservas
            cursor.execute("DELETE FROM reserva WHERE id_sala = %s", (id_sala,))

        # 2) Borrar salas
        cursor.execute("DELETE FROM sala WHERE id_edificio = %s", (id_edificio,))

        # 3) Borrar edificio
        cursor.execute("DELETE FROM edificio WHERE id_edificio = %s", (id_edificio,))

        conn.commit()
        return True, None

    except Exception as e:
        conn.rollback()
        print("ERROR eliminando edificio:", e)
        return False, "El edificio no se puede eliminar debido a dependencias."

    finally:
        conn.close()

