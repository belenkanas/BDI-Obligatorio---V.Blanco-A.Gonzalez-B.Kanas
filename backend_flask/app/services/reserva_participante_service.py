from app.database.conexion_db import conexion
from datetime import datetime


# listar todas las reservas con sus participantes
def listar_reservas_participantes():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT rp.ci_participante, p.nombre, p.apellido,
               rp.id_reserva, rp.fecha_solicitud_reserva, rp.asistencia,
               r.fecha, r.estado, s.nombre_sala
        FROM reserva_participante rp
        JOIN participante p ON rp.ci_participante = p.ci
        JOIN reserva r ON rp.id_reserva = r.id_reserva
        JOIN sala s ON r.id_sala = s.id_sala
        ORDER BY rp.fecha_solicitud_reserva DESC
    """)
    registros = cursor.fetchall()
    conn.close()
    return registros


# obtener los participantes de una reserva específica
def obtener_participantes_por_reserva(id_reserva):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT rp.ci_participante, p.nombre, p.apellido,
               rp.fecha_solicitud_reserva, rp.asistencia
        FROM reserva_participante rp
        JOIN participante p ON rp.ci_participante = p.ci
        WHERE rp.id_reserva = %s
    """, (id_reserva,))
    participantes = cursor.fetchall()
    conn.close()
    return participantes


# asociar un participante a una reserva
def crear_reserva_participante(ci_participante, id_reserva, asistencia=None):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    # verificar que exista dicho participante con su reserva
    cursor.execute("SELECT ci FROM participante WHERE ci = %s", (ci_participante,))
    if not cursor.fetchone():
        conn.close()
        return None, "El participante no existe"

    cursor.execute("SELECT id_reserva FROM reserva WHERE id_reserva = %s", (id_reserva,))
    if not cursor.fetchone():
        conn.close()
        return None, "La reserva no existe"

    # Evitar que hayan duplicados
    cursor.execute("""
        SELECT * FROM reserva_participante
        WHERE ci_participante = %s AND id_reserva = %s
    """, (ci_participante, id_reserva))
    if cursor.fetchone():
        conn.close()
        return None, "El participante ya está vinculado a esta reserva"

    fecha_solicitud = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO reserva_participante (ci_participante, id_reserva, fecha_solicitud_reserva, asistencia)
        VALUES (%s, %s, %s, %s)
    """, (ci_participante, id_reserva, fecha_solicitud, asistencia))
    conn.commit()
    conn.close()

    return {
        "ci_participante": ci_participante,
        "id_reserva": id_reserva,
        "fecha_solicitud_reserva": fecha_solicitud,
        "asistencia": asistencia
    }, "Participante vinculado exitosamente a la reserva"


# actualizar asistencia
def actualizar_asistencia(ci_participante, id_reserva, asistencia):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM reserva_participante
        WHERE ci_participante = %s AND id_reserva = %s
    """, (ci_participante, id_reserva))
    if not cursor.fetchone():
        conn.close()
        return None, "La relación participante-reserva no existe"

    cursor.execute("""
        UPDATE reserva_participante
        SET asistencia = %s
        WHERE ci_participante = %s AND id_reserva = %s
    """, (asistencia, ci_participante, id_reserva))
    conn.commit()
    conn.close()

    return {"ci_participante": ci_participante, "id_reserva": id_reserva, "asistencia": asistencia}, "Asistencia actualizada"


# eliminar vínculo participante-reserva
def eliminar_reserva_participante(ci_participante, id_reserva):
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM reserva_participante
        WHERE ci_participante = %s AND id_reserva = %s
    """, (ci_participante, id_reserva))
    conn.commit()
    filas = cursor.rowcount
    conn.close()
    return filas > 0
