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
        SELECT f.nombre AS facultad,
            pa.nombre_programa AS programa,
            COUNT(DISTINCT r.id_reserva) AS cantidad_reservas
        FROM obligatorio.reserva r
        JOIN obligatorio.reserva_participante rp 
            ON r.id_reserva = rp.id_reserva
        JOIN obligatorio.participante_programa_academico ppa 
            ON rp.ci_participante = ppa.ci_participante
        JOIN obligatorio.programa_academico pa 
            ON ppa.id_programa = pa.id_programa
        JOIN obligatorio.facultad f 
            ON pa.id_facultad = f.id_facultad
        GROUP BY f.nombre, pa.nombre_programa
        ORDER BY cantidad_reservas DESC
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

#Cantidad de sanciones por tipo de persona
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

def porcentajes_tipos_reservas():
    conn = conexion()
    cursor= conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT ((SELECT COUNT(*)
         FROM reserva r
         WHERE r.estado = 'activa' OR r.estado = 'finalizada') / (SELECT COUNT(*) FROM reserva) * 100) AS porcentaje_utilizadas,
        ((SELECT COUNT(*)
          FROM reserva r
          WHERE r.estado = 'cancelada' OR r.estado = 'sin_asistencia') / (SELECT COUNT(*) FROM reserva) * 100) AS porcentaje_canceladas;

                   """
                   )
    
    datos = cursor.fetchall()
    conn.close()
    return datos

#Consultas agregadas
def salas_sin_reservas():
    conn = conexion()
    cursor= conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT s.nombre_sala, e.nombre_edificio
        FROM obligatorio.sala s
        JOIN obligatorio.edificio e ON s.id_edificio = e.id_edificio
        LEFT JOIN obligatorio.reserva r ON r.id_sala= s.id_sala
        WHERE r.id_reserva IS NULL
        ORDER BY e.nombre_edificio, s.nombre_sala;
                   """
                   )
    
    datos = cursor.fetchall()
    conn.close()
    return datos

def participantes_que_mas_cancelan():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT rp.ci_participante,
               COUNT(*) AS reservas_totales,
               SUM(r.estado IN ('cancelada','sin asistencia')) AS no_efectivas,
               ROUND(100 * SUM(r.estado IN ('cancelada','sin asistencia')) / COUNT(*), 1) AS porcentaje_cancelacion
        FROM reserva r
        JOIN reserva_participante rp ON rp.id_reserva = r.id_reserva
        GROUP BY rp.ci_participante
        HAVING COUNT(*) >= 3
        ORDER BY porcentaje_cancelacion DESC, reservas_totales DESC
    """)

    resultados = cursor.fetchall()
    conn.close()
    return resultados

def programas_que_mas_usan_los_edificios():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT pa.nombre_programa, COUNT(DISTINCT e.id_edificio) AS edificios_usados
        FROM reserva r
        JOIN sala s ON r.id_sala = s.id_sala
        JOIN edificio e ON s.id_edificio = e.id_edificio
        JOIN reserva_participante rp ON rp.id_reserva = r.id_reserva
        JOIN participante_programa_academico ppa ON ppa.ci_participante = rp.ci_participante
        JOIN programa_academico pa ON pa.id_programa = ppa.id_programa
        GROUP BY pa.nombre_programa
        ORDER BY edificios_usados DESC, pa.nombre_programa;
    """)

    resultados = cursor.fetchall()
    conn.close()
    return resultados