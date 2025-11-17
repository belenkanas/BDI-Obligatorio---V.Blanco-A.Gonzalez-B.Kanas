from app.database.conexion_db import conexion

def listar_turnos():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM turno")

    turnos = cursor.fetchall()
    conn.close()

    return turnos


def obtener_turno(id_turno):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM turno WHERE id_turno = %s", (id_turno,))

    turno = cursor.fetchone()
    conn.close()

    return turno


def agregar_turno(hora_inicio, hora_fin):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM turno 
        WHERE hora_inicio = %s AND hora_fin = %s
    """, (hora_inicio, hora_fin))

    if cursor.fetchone():
        conn.close()
        return None, "El turno ya existe"

    cursor.execute("""
        INSERT INTO turno (hora_inicio, hora_fin)
        VALUES (%s, %s)
    """, (hora_inicio, hora_fin))

    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()

    return {
        "id_turno": nuevo_id,
        "hora_inicio": hora_inicio,
        "hora_fin": hora_fin
    }, "Turno creado exitosamente"


def eliminar_turno(id_turno):
    conn = conexion()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM turno WHERE id_turno = %s", (id_turno,))

    conn.commit()
    filas = cursor.rowcount
    conn.close()

    return filas > 0
