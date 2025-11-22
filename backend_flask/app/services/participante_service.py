from app.database.conexion_db import conexion

def listar_participantes():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM participante")

    participantes = cursor.fetchall()
    conn.close()

    # Siempre devolver una lista
    return participantes if participantes else []



def obtener_participante(ci):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM participante WHERE ci = %s", (ci,))
    
    participante = cursor.fetchone()
    conn.close()
    
    return participante


def agregar_participante(ci, nombre, apellido, email):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM participante WHERE ci = %s", (ci,))

    if cursor.fetchone():
        conn.close()
        return None, "El participante ya existe"

    cursor.execute("""INSERT INTO participante (ci, nombre, apellido, email) 
                        VALUES (%s, %s, %s, %s)""", (ci, nombre, apellido, email))
    
    conn.commit()
    conn.close()

    return {"ci": ci, "nombre": nombre, "apellido": apellido, "email": email}, "Participante creado exitosamente"


def eliminar_participante(ci, force=False):
    conn = conexion()
    cursor = conn.cursor()

    try:
        # 1) Verificar si el participante existe y obtener email
        cursor.execute("""
            SELECT email
            FROM participante
            WHERE ci = %s
        """, (ci,))
        row = cursor.fetchone()
        if not row:
            return False, False, "El participante no existe."
        
        email = row[0]

        # 2) Buscar sanciones asociadas
        cursor.execute("""
            SELECT id_sancion
            FROM sancion_participante
            WHERE ci_participante = %s
        """, (ci,))
        sanciones = cursor.fetchall()

        # 3) Buscar reservas en las que participa
        cursor.execute("""
            SELECT id_reserva
            FROM reserva_participante
            WHERE ci_participante = %s
        """, (ci,))
        reservas = cursor.fetchall()

        # Si tiene reservas y NO es force → no borrar
        if reservas and not force:
            return False, True, "El participante está asociado a reservas."

        # 4) Borrar sanciones directamente
        cursor.execute("""
            DELETE FROM sancion_participante
            WHERE ci_participante = %s
        """, (ci,))

        # 5) Procesar reservas
        for (id_reserva,) in reservas:
            # Contar participantes de esa reserva
            cursor.execute("""
                SELECT COUNT(*)
                FROM reserva_participante
                WHERE id_reserva = %s
            """, (id_reserva,))
            (cant,) = cursor.fetchone()

            if cant > 1:
                # Tiene más participantes → solo lo desvinculamos
                cursor.execute("""
                    DELETE FROM reserva_participante
                    WHERE ci_participante = %s AND id_reserva = %s
                """, (ci, id_reserva))
            else:
                # Es el único → eliminar reserva entera
                cursor.execute("""
                    DELETE FROM reserva_participante
                    WHERE id_reserva = %s
                """, (id_reserva,))
                cursor.execute("""
                    DELETE FROM reserva
                    WHERE id_reserva = %s
                """, (id_reserva,))

        # 6) Borrar su relación con programas académicos
        cursor.execute("""
            DELETE FROM participante_programa_academico
            WHERE ci_participante = %s
        """, (ci,))

        # 7) Eliminar participante
        cursor.execute("""
            DELETE FROM participante
            WHERE ci = %s
        """, (ci,))

        # 8) Eliminar login vinculado
        cursor.execute("""
            DELETE FROM login
            WHERE correo = %s
        """, (email,))

        conn.commit()
        return True, False, None

    except Exception as e:
        conn.rollback()
        print("ERROR al eliminar participante:", e)
        return False, False, "Error interno al eliminar."

    finally:
        conn.close()


def obtener_participantes_permitidos(id_sala):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT tipo_sala FROM sala WHERE id_sala = %s", (id_sala,))
    sala = cursor.fetchone()
    tipo_sala = sala["tipo_sala"]

    if tipo_sala == "docente":
        query = """
            SELECT p.*
            FROM participante p
            JOIN participante_programa_academico ppa ON p.ci = ppa.ci_participante
            WHERE ppa.rol = 'docente'
        """
    elif tipo_sala == "posgrado":
        query = """
            SELECT p.*
            FROM participante p
            JOIN participante_programa_academico ppa ON p.ci = ppa.ci_participante
            JOIN programa_academico pa ON ppa.id_programa = pa.id_programa
            WHERE ppa.rol = 'alumno'
              AND pa.tipo = 'posgrado'
        """
    else:
        query = """
            SELECT p.*, ppa.rol
            FROM participante p
            LEFT JOIN participante_programa_academico ppa 
            ON p.ci = ppa.ci_participante
        """

    cursor.execute(query)
    participantes = cursor.fetchall()

    participantes = [
        p for p in participantes
        if p.get("rol") != "admin"
    ]

    conn.close()
    return participantes