from database.obligatorio import conexion

def listar_reservas():
    conn = conexion()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM reserva")
    
    reservas = cursor.fetchall()
    conn.close()
    
    return reservas


def obtener_reserva(id_reserva):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM reserva WHERE id_reserva = %s", (id_reserva,))
    
    reserva = cursor.fetchone()
    conn.close()
    
    return reserva


'''
def crear_reserva(nombre_programa, id_facultad, tipo):
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
'''

def cancelar_reserva(id_programa):
    conn = conexion()
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM programa_academico WHERE id_programa = %s", (id_programa,))
    
    conn.commit()
    filas = cursor.rowcount
    conn.close()
    
    return filas > 0