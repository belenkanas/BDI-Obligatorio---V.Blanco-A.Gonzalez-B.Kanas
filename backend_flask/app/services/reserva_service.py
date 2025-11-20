from app.database.conexion_db import conexion
from datetime import datetime, timedelta
from app.services.sancion_participante_service import sancionar_participantes_sin_asistencia


def listar_reservas():
    con = conexion()
    cursor = con.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            r.id_reserva,
            r.fecha,
            r.estado,
            s.nombre_sala,
            t.hora_inicio,
            t.hora_fin
        FROM reserva r
        JOIN sala s ON r.id_sala = s.id_sala
        JOIN turno t ON r.id_turno = t.id_turno
        ORDER BY r.fecha DESC, t.hora_inicio
    """)

    reservas = cursor.fetchall()
    con.close()

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

        # Validar que no exista reserva activa para la misma sala, fecha y turno
        cursor.execute("""
            SELECT * FROM reserva
            WHERE id_sala = %s AND id_turno = %s AND fecha = %s AND estado = 'activa'
        """, (id_sala, id_turno, fecha))
        if cursor.fetchone():
            conection.close()
            return None, "Ya existe una reserva activa para esta sala, fecha y turno."

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
        participantes_roles = {}

        if participantes:
            placeholders = ','.join(['%s'] * len(participantes))
            cursor.execute(f"""
                SELECT ppa.ci_participante, ppa.rol, pa.tipo
                FROM participante_programa_academico ppa
                JOIN programa_academico pa ON ppa.id_programa = pa.id_programa
                WHERE ppa.ci_participante IN ({placeholders})
            """, tuple(participantes))
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



def actualizar_estado_reserva(id_reserva, nuevo_estado, asistencias=None):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    try:
        # Verificar que la reserva exista
        cursor.execute("SELECT * FROM reserva WHERE id_reserva = %s", (id_reserva,))
        reserva = cursor.fetchone()
        if not reserva:
            conn.close()
            return None, "La reserva no existe"

        # Actualizar estado
        cursor.execute("""
            UPDATE reserva
            SET estado = %s
            WHERE id_reserva = %s
        """, (nuevo_estado, id_reserva))
        conn.commit()

        # Si pasa a “sin asistencia”, sancionar automáticamente
        if nuevo_estado == "sin asistencia":
            sancionados, mensaje = sancionar_participantes_sin_asistencia(id_reserva)
            conn.close()
            if sancionados:
                return {
                    "id_reserva": id_reserva,
                    "nuevo_estado": nuevo_estado,
                    "sancionados": sancionados
                }, f"Reserva actualizada y sanción aplicada: {mensaje}"
            else:
                return {"id_reserva": id_reserva, "nuevo_estado": nuevo_estado}, mensaje

        #Si el estado es 'finalizada' y se desean regirstrar asistencias
        if nuevo_estado == "finalizada" and asistencias:
            # Actualizar asistencias uno por uno
            for ci, asistencia in asistencias.items():
                cursor.execute("""
                    UPDATE reserva_participante
                    SET asistencia = %s
                    WHERE id_reserva = %s AND ci_participante = %s
                """, (asistencia, id_reserva, ci))
            conn.commit()

            # Revisar si todos faltaron
            cursor.execute("""
                SELECT COUNT(*) AS total,
                       SUM(CASE WHEN asistencia = TRUE THEN 1 ELSE 0 END) AS presentes
                FROM reserva_participante
                WHERE id_reserva = %s
            """, (id_reserva,))
            data = cursor.fetchone()

            if data['presentes'] == 0:
                sancionados, mensaje = sancionar_participantes_sin_asistencia(id_reserva)
                conn.close()
                return {
                    "id_reserva": id_reserva,
                    "nuevo_estado": nuevo_estado,
                    "sancionados": sancionados
                }, f"Reserva finalizada. Todos faltaron. {mensaje}"

            conn.close()
            return {
                "id_reserva": id_reserva,
                "nuevo_estado": nuevo_estado,
                "asistencias": asistencias
            }, "Reserva finalizada y asistencias registradas correctamente."

        conn.close()
        return {"id_reserva": id_reserva, "nuevo_estado": nuevo_estado}, "Reserva actualizada exitosamente"

    except Exception as e:
        conn.rollback()
        conn.close()
        return None, f"Error al actualizar el estado de la reserva: {str(e)}"


def registrar_asistencias(id_reserva, asistencias):
    """
    Marca la asistencia (True/False) de los participantes de una reserva.
    Si todos faltan, sanciona automáticamente.
    """
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    try:
        # Verificar que la reserva exista
        cursor.execute("SELECT * FROM reserva WHERE id_reserva = %s", (id_reserva,))
        reserva = cursor.fetchone()
        if not reserva:
            conn.close()
            return None, "La reserva no existe"

        # Verificar que tenga participantes
        cursor.execute("""
            SELECT ci_participante FROM reserva_participante
            WHERE id_reserva = %s
        """, (id_reserva,))
        participantes = cursor.fetchall()
        if not participantes:
            conn.close()
            return None, "La reserva no tiene participantes"

        # Actualizar asistencia por participante
        for p in participantes:
            ci = p['ci_participante']
            asistencia = asistencias.get(ci)
            if asistencia is not None:
                cursor.execute("""
                    UPDATE reserva_participante
                    SET asistencia = %s
                    WHERE id_reserva = %s AND ci_participante = %s
                """, (asistencia, id_reserva, ci))

        conn.commit()

        # Verificar si todos faltaron
        cursor.execute("""
            SELECT COUNT(*) AS total,
                   SUM(CASE WHEN asistencia = TRUE THEN 1 ELSE 0 END) AS presentes
            FROM reserva_participante
            WHERE id_reserva = %s
        """, (id_reserva,))
        data = cursor.fetchone()

        if data['presentes'] == 0:
            # Si nadie asistió → aplicar sanciones automáticamente
            sancionados, mensaje = sancionar_participantes_sin_asistencia(id_reserva)
            conn.close()
            return {"sancionados": sancionados}, f"Todos faltaron. {mensaje}"

        conn.close()
        return {"id_reserva": id_reserva, "asistencias_registradas": asistencias}, "Asistencias registradas correctamente"

    except Exception as e:
        conn.rollback()
        conn.close()
        return None, f"Error al registrar asistencias: {str(e)}"

def listar_reservas_con_asistencias_filtro(estado=None, fecha_desde=None, fecha_hasta=None, id_edificio=None, tipo_sala=None):
    """
    Retorna reservas con información completa (sala, edificio, participantes, asistencias),
    aplicando filtros opcionales:
      - estado
      - rango de fechas
      - edificio
      - tipo de sala
    """
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            r.id_reserva,
            r.fecha,
            r.estado,
            t.hora_inicio,
            t.hora_fin,
            s.nombre_sala,
            s.tipo_sala,
            e.nombre_edificio,
            e.direccion,
            p.ci AS ci_participante,
            p.nombre AS nombre_participante,
            p.apellido AS apellido_participante,
            rp.asistencia,
            rp.fecha_solicitud_reserva
        FROM reserva r
        JOIN turno t ON r.id_turno = t.id_turno
        JOIN sala s ON r.id_sala = s.id_sala
        JOIN edificio e ON s.id_edificio = e.id_edificio
        LEFT JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
        LEFT JOIN participante p ON rp.ci_participante = p.ci
        WHERE 1=1
    """

    params = []

    if estado:
        query += " AND r.estado = %s"
        params.append(estado)

    if fecha_desde:
        query += " AND r.fecha >= %s"
        params.append(fecha_desde)

    if fecha_hasta:
        query += " AND r.fecha <= %s"
        params.append(fecha_hasta)

    if id_edificio:
        query += " AND e.id_edificio = %s"
        params.append(id_edificio)

    if tipo_sala:
        query += " AND s.tipo_sala = %s"
        params.append(tipo_sala)

    query += " ORDER BY r.fecha DESC, r.id_reserva DESC"

    cursor.execute(query, tuple(params))
    filas = cursor.fetchall()
    conn.close()

    # Agrupar por reserva
    reservas_dict = {}
    for fila in filas:
        id_reserva = fila["id_reserva"]
        if id_reserva not in reservas_dict:
            reservas_dict[id_reserva] = {
                "id_reserva": id_reserva,
                "fecha": fila["fecha"],
                "estado": fila["estado"],
                "turno": {
                    "hora_inicio": str(fila["hora_inicio"]),
                    "hora_fin": str(fila["hora_fin"])
                },
                "sala": {
                    "nombre_sala": fila["nombre_sala"],
                    "tipo_sala": fila["tipo_sala"],
                    "edificio": fila["nombre_edificio"],
                    "direccion": fila["direccion"]
                },
                "participantes": []
            }

        if fila["ci_participante"]:
            reservas_dict[id_reserva]["participantes"].append({
                "ci": fila["ci_participante"],
                "nombre": fila["nombre_participante"],
                "apellido": fila["apellido_participante"],
                "asistencia": fila["asistencia"],
                "fecha_solicitud_reserva": fila["fecha_solicitud_reserva"]
            })

    return list(reservas_dict.values())

def cancelar_reserva(id_reserva):
    return actualizar_estado_reserva(id_reserva, "cancelada")

def listar_reservas_por_participante(ci):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT 
            r.id_reserva,
            r.fecha,
            r.estado,
            t.hora_inicio,
            t.hora_fin,
            s.nombre_sala,
            e.nombre_edificio,
            rp.asistencia
        FROM reserva_participante rp
        JOIN reserva r ON rp.id_reserva = r.id_reserva
        JOIN turno t ON r.id_turno = t.id_turno
        JOIN sala s ON r.id_sala = s.id_sala
        JOIN edificio e ON s.id_edificio = e.id_edificio
        WHERE rp.ci_participante = %s
        ORDER BY r.fecha DESC, t.hora_inicio
    """, (ci,))

    reservas = cursor.fetchall()
    conn.close()
    return reservas
