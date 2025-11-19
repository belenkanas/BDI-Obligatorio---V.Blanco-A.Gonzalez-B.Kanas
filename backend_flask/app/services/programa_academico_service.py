from app.database.conexion_db import conexion

def listar_programas():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM programa_academico")
    
    programas = cursor.fetchall()
    conn.close()
    
    return programas


def obtener_programa(id_programa):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM programa_academico WHERE id_programa = %s", (id_programa,))
    
    programa = cursor.fetchone()
    conn.close()
    
    return programa


def crear_programa(nombre_programa, id_facultad, tipo):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM programa_academico WHERE nombre_programa = %s", (nombre_programa,))
    
    if cursor.fetchone():
        conn.close()
        return None, "El programa académico ya existe"

    cursor.execute("INSERT INTO programa_academico (nombre_programa, id_facultad, tipo) VALUES (%s, %s, %s)", (nombre_programa, id_facultad, tipo))
    
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()
    
    return {"id_programa": nuevo_id, "nombre_programa": nombre_programa, "id_facultad": id_facultad, "tipo": tipo}, "Programa creado exitosamente"


def eliminar_programa(id_programa):
    conn = conexion()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT id_programa FROM programa_academico WHERE id_programa = %s", (id_programa,))

        if cursor.fetchone() is None:
            conn.close()
            return False  
        
        cursor.execute("DELETE FROM participante_programa_academico WHERE id_programa = %s", (id_programa,))

        cursor.execute("DELETE FROM programa_academico WHERE id_programa = %s", (id_programa,))

        conn.commit()
        return True

    except Exception as e:
        conn.rollback()
        print("ERROR al borrar programa:", e)
        return False

    finally:
        conn.close()