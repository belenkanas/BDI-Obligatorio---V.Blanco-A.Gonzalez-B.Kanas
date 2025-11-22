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


def eliminar_sala(id_sala):
    conn = conexion()
    cursor = conn.cursor()

    try:
        # 1) Borrar asistencias
        cursor.execute("""
            DELETE a FROM asistencia a
            JOIN reserva r ON a.id_reserva = r.id_reserva
            WHERE r.id_sala = %s
        """, (id_sala,))

        # 2) Borrar reservas y participantes
        cursor.execute("""
            DELETE rp FROM reserva_participante rp
            JOIN reserva r ON rp.id_reserva = r.id_reserva
            WHERE r.id_sala = %s
        """, (id_sala,))

        # 3) Borrar reservas
        cursor.execute("DELETE FROM reserva WHERE id_sala = %s", (id_sala,))

        # 4) Borrar sala
        cursor.execute("DELETE FROM sala WHERE id_sala = %s", (id_sala,))

        conn.commit()
        return cursor.rowcount > 0

    except Exception as e:
        conn.rollback()
        print("ERROR al borrar sala:", e)
        return False, "La sala no se puede eliminar porque tiene reservas o registros asociados."

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