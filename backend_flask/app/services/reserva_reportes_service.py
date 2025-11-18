from app.database.conexion_db import conexion

def salas_mas_reservadas():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT s.nombre_sala, COUNT(*) AS total_reservas
        FROM reserva r
        JOIN sala s ON r.id_sala = s.id_sala
        GROUP BY s.id_sala
        ORDER BY total_reservas DESC
        LIMIT 10
    """)

    datos = cursor.fetchall()
    conn.close()
    return datos

def turnos_mas_demandados():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT t.hora_inicio, t.hora_fin, COUNT(*) AS total_reservas
        FROM reserva r
        JOIN turno t ON r.id_turno = t.id_turno
        GROUP BY t.id_turno
        ORDER BY total_reservas DESC
    """)

    datos = cursor.fetchall()
    conn.close()
    return datos

def promedio_participantes_por_sala():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT s.nombre_sala,
               AVG(cnt.cantidad) AS promedio_participantes
        FROM sala s
        JOIN (
            SELECT id_reserva, COUNT(*) AS cantidad
            FROM reserva_participante
            GROUP BY id_reserva
        ) cnt ON s.id_sala = (SELECT id_sala FROM reserva WHERE id_reserva = cnt.id_reserva)
        GROUP BY s.id_sala
    """)

    datos = cursor.fetchall()
    conn.close()
    return datos

def reservas_por_carrera():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT pa.nombre_programa,
               pa.facultad,
               COUNT(*) AS total_reservas
        FROM reserva_participante rp
        JOIN participante_programa_academico ppa ON rp.ci_participante = ppa.ci_participante
        JOIN programa_academico pa ON ppa.id_programa = pa.id_programa
        GROUP BY pa.id_programa
        ORDER BY total_reservas DESC
    """)

    datos = cursor.fetchall()
    conn.close()
    return datos

def ocupacion_por_edificio():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT e.nombre_edificio,
               SUM(s.capacidad) AS capacidad_total,
               SUM(cnt.participantes) AS participantes_totales,
               ROUND(SUM(cnt.participantes) / SUM(s.capacidad) * 100, 2) AS porcentaje_ocupacion
        FROM edificio e
        JOIN sala s ON e.id_edificio = s.id_edificio
        LEFT JOIN (
            SELECT rp.id_reserva, COUNT(*) AS participantes
            FROM reserva_participante rp
            GROUP BY rp.id_reserva
        ) cnt ON cnt.id_reserva IN (
            SELECT id_reserva FROM reserva WHERE id_sala = s.id_sala
        )
        GROUP BY e.id_edificio
    """)

    datos = cursor.fetchall()
    conn.close()
    return datos

def actividad_participantes():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT ppa.rol,
               pa.tipo AS programa_tipo,
               COUNT(rp.id_reserva) AS total_reservas,
               SUM(CASE WHEN rp.asistencia = TRUE THEN 1 ELSE 0 END) AS asistencias
        FROM reserva_participante rp
        JOIN participante_programa_academico ppa ON rp.ci_participante = ppa.ci_participante
        JOIN programa_academico pa ON ppa.id_programa = pa.id_programa
        GROUP BY ppa.rol, pa.tipo
    """)

    datos = cursor.fetchall()
    conn.close()
    return datos

def cantidad_sanciones():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT ppa.rol,
               pa.tipo,
               COUNT(*) AS sanciones
        FROM sancion_participante sp
        JOIN participante_programa_academico ppa ON sp.ci_participante = ppa.ci_participante
        JOIN programa_academico pa ON ppa.id_programa = pa.id_programa
        GROUP BY ppa.rol, pa.tipo
    """)

    datos = cursor.fetchall()
    conn.close()
    return datos
