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


def eliminar_sala(id_sala, force=False):
    conn = conexion()
    cursor = conn.cursor()

    try:
        # 1) Buscar reservas asociadas a esa sala
        cursor.execute("SELECT id_reserva FROM reserva WHERE id_sala = %s", (id_sala,))
        reservas = cursor.fetchall()  # Lista de tuplas [(9,), (10,), ...]

        # Si tiene reservas y no es eliminación forzada --> avisar al frontend
        if reservas and not force:
            return False, True, "La sala tiene reservas asociadas."

        # 2) Si es forzado --> eliminar reservas y sus relaciones
        for (id_reserva,) in reservas:

            # Ver si la reserva tiene participantes
            cursor.execute("""
                SELECT COUNT(*) 
                FROM reserva_participante 
                WHERE id_reserva = %s
            """, (id_reserva,))
            (cant_participantes,) = cursor.fetchone()

            # Si tiene participantes → eliminarlos primero
            if cant_participantes > 0:
                cursor.execute("""
                    DELETE FROM reserva_participante
                    WHERE id_reserva = %s
                """, (id_reserva,))

            # Ahora sí borrar la reserva
            cursor.execute("""
                DELETE FROM reserva
                WHERE id_reserva = %s
            """, (id_reserva,))

        # 3) Borrar la sala finalmente
        cursor.execute("DELETE FROM sala WHERE id_sala = %s", (id_sala,))

        conn.commit()
        return True, False, None

    except Exception as e:
        conn.rollback()
        print("ERROR al eliminar sala:", e)
        return False, False, "Error interno al eliminar sala."

    finally:
        conn.close()

def obtener_salas_permitidas_para_usuario(ci, id_edificio):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    # Obtener rol y programa del usuario
    cursor.execute("""
        SELECT ppa.rol, pa.tipo AS tipo_programa
        FROM participante_programa_academico ppa
        JOIN programa_academico pa ON ppa.id_programa = pa.id_programa
        WHERE ppa.ci_participante = %s
        LIMIT 1
    """, (ci,))
    datos = cursor.fetchone()

    if datos is None:
        conn.close()
        return []

    rol = datos["rol"]
    tipo_programa = datos["tipo_programa"]

    # Obtener salas SOLO del edificio elegido
    cursor.execute("""
        SELECT *
        FROM sala
        WHERE id_edificio = %s
    """, (id_edificio,))
    todas_salas = cursor.fetchall()

    salas_permitidas = []

    for sala in todas_salas:
        tipo_sala = sala["tipo_sala"]

        # DOCENTE → docente + libre
        if rol == "docente":
            if tipo_sala in ["docente", "libre"]:
                salas_permitidas.append(sala)

        # ALUMNO POSGRADO → posgrado + libre
        elif rol == "alumno" and tipo_programa == "posgrado":
            if tipo_sala in ["posgrado", "libre"]:
                salas_permitidas.append(sala)

        # ALUMNO GRADO → solo libre
        elif rol == "alumno" and tipo_programa == "grado":
            if tipo_sala == "libre":
                salas_permitidas.append(sala)

    conn.close()
    return salas_permitidas