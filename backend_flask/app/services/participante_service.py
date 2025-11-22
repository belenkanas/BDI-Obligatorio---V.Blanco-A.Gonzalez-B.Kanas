from app.database.conexion_db import conexion

def listar_participantes():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM participante")
    
    participantes = cursor.fetchall()
    conn.close()
    
    return participantes


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


def eliminar_participante(ci):
    conn = conexion()
    cursor = conn.cursor()

    try:
        # 1) Borrar programas asociados
        cursor.execute("""
            DELETE FROM participante_programa_academico 
            WHERE ci_participante = %s
        """, (ci,))

        # 2) Obtener reservas donde participa
        cursor.execute("""
            SELECT r.id_reserva
            FROM reserva r
            JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
            WHERE rp.ci = %s
        """, (ci,))
        reservas = cursor.fetchall()

        for (id_reserva,) in reservas:
            # Cantidad de participantes
            cursor.execute("""
                SELECT COUNT(*) 
                FROM reserva_participante 
                WHERE id_reserva = %s
            """, (id_reserva,))
            (cant,) = cursor.fetchone()

            if cant > 1:
                cursor.execute("""
                    DELETE FROM reserva_participante
                    WHERE ci = %s AND id_reserva = %s
                """, (ci, id_reserva))
            else:
                # Borrar asistencias
                cursor.execute("DELETE FROM asistencia WHERE id_reserva = %s", (id_reserva,))
                # Borrar participantes
                cursor.execute("DELETE FROM reserva_participante WHERE id_reserva = %s", (id_reserva,))
                # Borrar reserva
                cursor.execute("DELETE FROM reserva WHERE id_reserva = %s", (id_reserva,))

        # 3) Borrar participante
        cursor.execute("DELETE FROM participante WHERE ci = %s", (ci,))

        conn.commit()
        return True, None

    except Exception as e:
        conn.rollback()
        print("ERROR al eliminar participante:", e)
        return False, "No se puede eliminar el participante porque tiene datos asociados."

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