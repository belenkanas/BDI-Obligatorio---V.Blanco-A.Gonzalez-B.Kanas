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
        # 1) Buscar TODOS los programas académicos asociados a la facultad
        cursor.execute("""
            SELECT id_programa 
            FROM programa_academico 
            WHERE id_facultad = %s
        """, (id_facultad,))
        
        programas = cursor.fetchall()  
        
        # Si no hay programas, simplemente se borra la facultad
        if not programas:
            cursor.execute("DELETE FROM facultad WHERE id_facultad = %s", (id_facultad,))
            conn.commit()
            return True
        
        # Convertir los resultados en números
        ids_programas = [p[0] for p in programas]

        # 2) Borrar relaciones participante-programa
        cursor.executemany("""
            DELETE FROM participante_programa_academico 
            WHERE id_programa = %s
        """, [(pid,) for pid in ids_programas])

        # 3) Borrar los programas académicos
        cursor.executemany("""
            DELETE FROM programa_academico
            WHERE id_programa = %s
        """, [(pid,) for pid in ids_programas])

        # 4) Borrar la facultad
        cursor.execute("DELETE FROM facultad WHERE id_facultad = %s", (id_facultad,))

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print("ERROR al borrar facultad:", e)
        return False

    finally:
        conn.close()
