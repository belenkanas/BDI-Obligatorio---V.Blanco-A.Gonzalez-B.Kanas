from database.obligatorio import conexion
from datetime import datetime, timedelta
from services.sancion_participante_service import sancionar_participantes_sin_asistencia


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
    Se verifica tambien que:
    --> No se supere la capacidad de la sala
    --> No se pueda participar en más de 3 reservas activas en una semana
    --> No se pueda estar más de 2 horas diarias en el mismo edificio
    Hacer excepción con docentes y estudiantes de posgrado
    Se verifica también que personas sancionadas no puedan reservar
    """
    conection = conexion()
    cursor = conection.cursor(dictionary=True)

    try:
        # Validar sala
        cursor.execute("""
            SELECT s.id_sala, s.capacidad, s.tipo_sala, e.id_edificio
            FROM sala s
            JOIN edificio e ON s.id_edificio = e.id_edificio
            WHERE s.id_sala = %s
        """, (id_sala,))
        sala = cursor.fetchone()
        if not sala:
            conection.close()
            return None, "La sala especificada no existe"

        # Validar turno
        cursor.execute("SELECT id_turno FROM turno WHERE id_turno = %s", (id_turno,))
        if not cursor.fetchone():
            conection.close()
            return None, "El turno especificado no existe"

        #Validar capacidad de la sala
        if participantes and len(participantes) > sala['capacidad']:
            conection.close()
            return None, f"La sala tiene capacidad para {sala['capacidad']} personas, pero se intentan registrar {len(participantes)}."

        #Validar sanciones
        for ci in participantes or []:
            cursor.execute("""
                SELECT * FROM sancion_participante
                WHERE ci_participante = %s
                AND NOW() BETWEEN fecha_inicio AND fecha_fin
            """, (ci,))
            sancion = cursor.fetchone()
            if sancion:
                conection.close()
                return None, f"El participante {ci} tiene una sanción vigente y no puede realizar reservas hasta {sancion['fecha_fin']}."

        #Revisar restricciones según los roles, tipo de programa y tipo de sala
        cursor.execute("""
            SELECT ppa.ci_participante, ppa.rol, pa.tipo
            FROM participante_programa_academico ppa
            JOIN programa_academico pa ON ppa.id_programa = pa.id_programa
            WHERE ppa.ci_participante IN (%s)
        """ % ','.join(['%s'] * len(participantes)), tuple(participantes))
        roles = cursor.fetchall()
        participantes_roles = {r['ci_participante']: (r['rol'], r['tipo']) for r in roles}

        for ci in participantes or []:
            rol, tipo = participantes_roles.get(ci, (None, None))
            tipo_sala = sala['tipo_sala']

            # Excepción: docente o posgrado en sala exclusiva
            if (rol == 'docente' and tipo_sala == 'docente') or (tipo == 'postgrado' and tipo_sala == 'postgrado'):
                continue  # sin restricciones

            # Validar reservas activas en la misma semana (no se pueden superar 3)
            cursor.execute("""
                SELECT COUNT(*) AS reservas_activas
                FROM reserva_participante rp
                JOIN reserva r ON rp.id_reserva = r.id_reserva
                WHERE rp.ci_participante = %s
                AND r.estado = 'activa'
                AND YEARWEEK(r.fecha, 1) = YEARWEEK(%s, 1)
            """, (ci, fecha))
            activas_semana = cursor.fetchone()['reservas_activas']
            if activas_semana >= 3:
                conection.close()
                return None, f"El participante {ci} ya tiene 3 reservas activas esta semana."

            # Validar horas diarias (2 turnos máximo por día y edificio)
            cursor.execute("""
                SELECT COUNT(*) AS reservas_dia
                FROM reserva_participante rp
                JOIN reserva r ON rp.id_reserva = r.id_reserva
                JOIN sala s ON r.id_sala = s.id_sala
                WHERE rp.ci_participante = %s
                AND r.fecha = %s
                AND s.id_edificio = %s
            """, (ci, fecha, sala['id_edificio']))
            reservas_dia = cursor.fetchone()['reservas_dia']
            if reservas_dia >= 2:
                conection.close()
                return None, f"El participante {ci} ya tiene 2 reservas en este edificio en la fecha {fecha}."

        #Crear la reserva
        cursor.execute("""
            INSERT INTO reserva (id_sala, fecha, id_turno, estado)
            VALUES (%s, %s, %s, %s)
        """, (id_sala, fecha, id_turno, estado))
        nueva_id = cursor.lastrowid

        # Si se proporcionan participantes, se insertan
        if participantes and len(participantes) > 0:
            fecha_solicitud = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for ci_participante in participantes:
                cursor.execute("""
                    INSERT INTO reserva_participante (ci_participante, id_reserva, fecha_solicitud_reserva, asistencia)
                    VALUES (%s, %s, %s, %s)
                """, (ci_participante, nueva_id, fecha_solicitud, None))

        conection.commit()
        conection.close()

        return {
            "id_reserva": nueva_id,
            "id_sala": id_sala,
            "fecha": fecha,
            "id_turno": id_turno,
            "estado": estado,
            "participantes": participantes or []
        }, "Reserva creada exitosamente"

    except Exception as e:
        conection.rollback()
        conection.close()
        return None, f"Error al crear la reserva: {str(e)}"



def actualizar_estado_reserva(id_reserva, nuevo_estado):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM reserva WHERE id_reserva = %s", (id_reserva,))
    reserva = cursor.fetchone()
    if not reserva:
        conn.close()
        return None, "La reserva no existe"

    cursor.execute("UPDATE reserva SET estado = %s WHERE id_reserva = %s", (nuevo_estado, id_reserva))
    conn.commit()
    conn.close()

    # Ejecutar sanción automática (de sancion_participante_service)
    if nuevo_estado == "sin asistencia":
        sancionados, mensaje_sancion = sancionar_participantes_sin_asistencia(id_reserva)
        if sancionados:
            return {
                "id_reserva": id_reserva,
                "nuevo_estado": nuevo_estado,
                "sancionados": sancionados
            }, f"Estado actualizado y {len(sancionados)} participantes sancionados"
        else:
            return {"id_reserva": id_reserva, "nuevo_estado": nuevo_estado}, mensaje_sancion

    return {"id_reserva": id_reserva, "nuevo_estado": nuevo_estado}, "Estado actualizado correctamente"


def cancelar_reserva(id_reserva):
    return actualizar_estado_reserva(id_reserva, "cancelada")