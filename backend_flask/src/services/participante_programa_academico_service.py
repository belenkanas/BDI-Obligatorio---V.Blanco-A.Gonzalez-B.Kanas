from backend_flask.src.database.conexion_db import conexion

def listar_registros():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""SELECT ppa.id_alumno_programa, ppa.ci_participante, ppa.id_programa, ppa.rol, pa.nombre_programa
                        FROM participante_programa_academico ppa
                        JOIN programa_academico pa ON ppa.id_programa = pa.id_programa""")
    
    registros = cursor.fetchall()
    conn.close()
    
    return registros


def obtener_registro(id_alumno_programa):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""SELECT ppa.*, pa.nombre_programa
                        FROM participante_programa_academico ppa
                        JOIN programa_academico pa ON ppa.id_programa = pa.id_programa
                        WHERE ppa.id_alumno_programa = %s""", (id_alumno_programa,))
    
    registro = cursor.fetchone()
    conn.close()
    
    return registro


def crear_registro(ci_participante, id_programa, rol):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("INSERT INTO participante_programa_academico (ci_participante, id_programa, rol) VALUES (%s, %s, %s)",(ci_participante, id_programa, rol))
    
    conn.commit()
    nuevo_id = cursor.lastrowid
    conn.close()
    
    return {
        "id_alumno_programa": nuevo_id,
        "ci_participante": ci_participante,
        "id_programa": id_programa,
        "rol": rol
    }, "Registro creado exitosamente"


def eliminar_registro(id_alumno_programa):
    conn = conexion()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM participante_programa_academico WHERE id_alumno_programa = %s", (id_alumno_programa,))
    
    conn.commit()
    filas = cursor.rowcount
    conn.close()
    
    return filas > 0