from app.database.conexion_db import conexion

def listar_facultades():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM facultad")

    facultades = cursor.fetchall()
    conn.close()

    return facultades


def obtener_facultad(id_facultad):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM facultad WHERE id_facultad = %s", (id_facultad,))

    facultad = cursor.fetchone()
    conn.close()

    return facultad


def agregar_facultad(nombre):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM facultad WHERE nombre = %s", (nombre,))

    if cursor.fetchone():
        conn.close()
        return None, "La facultad ya existe"

    cursor.execute("""
        INSERT INTO facultad (nombre)
        VALUES (%s)
    """, (nombre,))

    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()

    return {"id_facultad": nuevo_id, "nombre": nombre}, "Facultad creada exitosamente"


def eliminar_facultad(id_facultad):
    conn = conexion()
    cursor = conn.cursor()
    try:
        #Busco si hay programas académicos asociados
        cursor.execute("select id_programa from programa_academico where id_facultad = %s", (id_facultad,))
        id_programa = cursor.fetchone()
        if cursor.fetchone() is None:
            conn.close()
            return False  
        #Borro las relaciones entre participantes y programas academicos
        cursor.execute("DELETE FROM participante_programa_academico WHERE id_programa = %s", (id_programa,))

        #Borro los programas academicos de dicha facultad
        cursor.execute("DELETE FROM programa_academico WHERE id_programa = %s", (id_programa,))
        
        #Finalmente borrar facultad
        cursor.execute("DELETE FROM facultad WHERE id_facultad = %s", (id_facultad,))
        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print("ERROR al borrar facultad:", e)
        return False

    finally:
        conn.close()