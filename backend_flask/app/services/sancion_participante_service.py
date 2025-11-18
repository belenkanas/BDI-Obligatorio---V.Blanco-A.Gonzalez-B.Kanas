from app.database.conexion_db import conexion
from datetime import datetime, timedelta

def listar_sanciones():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT sp.*, p.nombre, p.apellido
        FROM sancion_participante sp
        JOIN participante p ON sp.ci_participante = p.ci
        ORDER BY sp.fecha_inicio DESC
    """)
    sanciones = cursor.fetchall()
    conn.close()
    return sanciones

#Listar sanciones ACTIVAS
def listar_sanciones_activas():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT sp.*, p.nombre, p.apellido
        FROM sancion_participante sp
        JOIN participante p ON sp.ci_participante = p.ci
        WHERE NOW() BETWEEN sp.fecha_inicio AND sp.fecha_fin
        ORDER BY sp.fecha_fin ASC
    """)

    sanciones = cursor.fetchall()
    conn.close()
    return sanciones

def sanciones_por_rol_y_tipo():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT ppa.rol, pa.tipo, COUNT(*) AS sanciones
        FROM sancion_participante sp
        JOIN participante_programa_academico ppa ON sp.ci_participante = ppa.ci_participante
        JOIN programa_academico pa ON ppa.id_programa = pa.id_programa
        GROUP BY ppa.rol, pa.tipo
        ORDER BY ppa.rol, pa.tipo
    """)

    resultados = cursor.fetchall()
    conn.close()
    return resultados

def obtener_sanciones_participante(ci_participante):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM sancion_participante
        WHERE ci_participante = %s
        ORDER BY fecha_inicio DESC
    """, (ci_participante,))
    sanciones = cursor.fetchall()
    conn.close()
    return sanciones

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

def crear_sancion(ci_participante, fecha_inicio=None, fecha_fin=None):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    if fecha_inicio is None:
        fecha_inicio = datetime.now()

    #fecha_fin = fecha_inicio + timedelta(days=60)

    # Validar que el participante exista
    cursor.execute("SELECT ci FROM participante WHERE ci = %s", (ci_participante,))
    if not cursor.fetchone():
        conn.close()
        return None, "El participante no existe"

    # Insertar sanción
    cursor.execute("""
        INSERT INTO sancion_participante (ci_participante, fecha_inicio, fecha_fin)
        VALUES (%s, %s, %s)
    """, (ci_participante, fecha_inicio, fecha_fin))
    conn.commit()
    conn.close()

    return {
        "ci_participante": ci_participante,
        "fecha_inicio": fecha_inicio.strftime("%Y-%m-%d %H:%M:%S"),
        "fecha_fin": fecha_fin.strftime("%Y-%m-%d %H:%M:%S")
    }, "Sanción creada exitosamente"


# Crear sanción automáticamente a los participantes de una reserva sin asistencia
def sancionar_participantes_sin_asistencia(id_reserva):
    """
    Se ejecuta cuando una reserva cambia a estado 'sin asistencia'.
    Si ninguno de los participantes asistió, se sancionan todos.
    """
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    # Verificar si la reserva existe
    cursor.execute("SELECT * FROM reserva WHERE id_reserva = %s", (id_reserva,))
    reserva = cursor.fetchone()
    if not reserva:
        conn.close()
        return None, "La reserva no existe"

    # Obtener participantes y verificar asistencias
    cursor.execute("""
        SELECT rp.ci_participante, rp.asistencia
        FROM reserva_participante rp
        WHERE rp.id_reserva = %s
    """, (id_reserva,))
    participantes = cursor.fetchall()

    if not participantes:
        conn.close()
        return None, "La reserva no tiene participantes"

    # Verificar si todos faltaron o no marcaron asistencia
    todos_faltaron = all(p['asistencia'] in (None, False) for p in participantes)

    if not todos_faltaron:
        conn.close()
        return None, "No se aplican sanciones: hubo participantes con asistencia registrada"

    # Crear sanción para cada participante
    fecha_inicio = datetime.now()
    fecha_fin = fecha_inicio + timedelta(days=60)

    for p in participantes:
        cursor.execute("""
            INSERT INTO sancion_participante (ci_participante, fecha_inicio, fecha_fin)
            VALUES (%s, %s, %s)
        """, (p['ci_participante'], fecha_inicio, fecha_fin))

    conn.commit()
    conn.close()

    return [p['ci_participante'] for p in participantes], "Participantes sancionados correctamente"
