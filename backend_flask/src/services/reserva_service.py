from database.obligatorio import conexion
from datetime import datetime

def listar_reservas():
    conection = conexion()
    cursor = conection.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.id_reserva, r.fecha, r.estado,
               s.nombre_sala, t.hora_inicio, t.hora_fin
        FROM reserva r
        JOIN sala s ON r.id_sala = s.id_sala
        JOIN turno t ON r.id_turno = t.id_turno
        ORDER BY r.fecha DESC, t.hora_inicio
    """)
    reservas = cursor.fetchall()
    conection.close()
    return reservas


def obtener_reserva(id_reserva):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.id_reserva, r.fecha, r.estado,
               s.nombre_sala, s.id_sala,
               t.id_turno, t.hora_inicio, t.hora_fin
        FROM reserva r
        JOIN sala s ON r.id_sala = s.id_sala
        JOIN turno t ON r.id_turno = t.id_turno
        WHERE r.id_reserva = %s
    """, (id_reserva,))
    reserva = cursor.fetchone()
    conn.close()
    return reserva


def crear_reserva(id_sala, fecha, id_turno, estado="activa", participantes=None):
    """
    Crea una reserva y asocia los participantes indicados.
    participantes es una lista de CIs (strings) de los participantes.
    """
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    try:
        # Validar sala
        cursor.execute("SELECT id_sala FROM sala WHERE id_sala = %s", (id_sala,))
        if not cursor.fetchone():
            conn.close()
            return None, "La sala especificada no existe"

        # Validar turno
        cursor.execute("SELECT id_turno FROM turno WHERE id_turno = %s", (id_turno,))
        if not cursor.fetchone():
            conn.close()
            return None, "El turno especificado no existe"

        # Insertar reserva
        cursor.execute("""
            INSERT INTO reserva (id_sala, fecha, id_turno, estado)
            VALUES (%s, %s, %s, %s)
        """, (id_sala, fecha, id_turno, estado))
        nueva_id = cursor.lastrowid

        # Si se proporcionan participantes, se insertan
        if participantes and len(participantes) > 0:
            fecha_solicitud = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for ci_participante in participantes:
                # Verificar que el participante exista
                cursor.execute("SELECT ci FROM participante WHERE ci = %s", (ci_participante,))
                if not cursor.fetchone():
                    conn.rollback()
                    conn.close()
                    return None, f"El participante con CI {ci_participante} no existe"

                cursor.execute("""
                    INSERT INTO reserva_participante (ci_participante, id_reserva, fecha_solicitud_reserva, asistencia)
                    VALUES (%s, %s, %s, %s)
                """, (ci_participante, nueva_id, fecha_solicitud, None))

        
        conn.commit()
        conn.close()

        return {
            "id_reserva": nueva_id,
            "id_sala": id_sala,
            "fecha": fecha,
            "id_turno": id_turno,
            "estado": estado,
            "participantes": participantes or []
        }, "Reserva creada exitosamente"

    except Exception as e:
        conn.rollback()
        conn.close()
        return None, f"Error al crear la reserva: {str(e)}"


def actualizar_estado_reserva(id_reserva, nuevo_estado):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM reserva WHERE id_reserva = %s", (id_reserva,))
    if not cursor.fetchone():
        conn.close()
        return None, "La reserva no existe"

    cursor.execute("UPDATE reserva SET estado = %s WHERE id_reserva = %s", (nuevo_estado, id_reserva))
    conn.commit()
    conn.close()

    return {"id_reserva": id_reserva, "nuevo_estado": nuevo_estado}, "Estado actualizado correctamente"


def cancelar_reserva(id_reserva):
    return actualizar_estado_reserva(id_reserva, "cancelada")