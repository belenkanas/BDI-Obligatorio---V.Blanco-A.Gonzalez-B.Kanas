from app.database.conexion_db import conexion

def login(correo, password):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    # 1. Verificar login
    cursor.execute(
        "SELECT correo FROM login WHERE correo = %s AND contrasena = %s",
        (correo, password)
    )
    existe = cursor.fetchone()

    if not existe:
        conn.close()
        return None

    # 2. Obtener participante (CI, nombre, apellido)
    cursor.execute(
        "SELECT ci, nombre, apellido, email FROM participante WHERE email = %s",
        (correo,)
    )
    participante = cursor.fetchone()

    if not participante:
        conn.close()
        return None

    # Guardamos el CI para buscar su rol/programa
    ci = participante["ci"]

    # 3. Obtener rol y tipo de programa
    cursor.execute("""
        SELECT ppa.rol, pa.tipo AS tipo_programa
        FROM participante_programa_academico ppa
        JOIN programa_academico pa ON ppa.id_programa = pa.id_programa
        WHERE ppa.ci_participante = %s
    """, (ci,))
    academico = cursor.fetchone()

    conn.close()

    # 4. Construimos el usuario completo
    return {
        "ci": participante["ci"],
        "nombre": participante["nombre"],
        "apellido": participante["apellido"],
        "email": participante["email"],
        "rol": academico["rol"],                 # alumno / docente
        "tipo_programa": academico["tipo_programa"]  # grado / posgrado
    }


def register_user(correo, password):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM login WHERE correo = %s", (correo,))
    if cursor.fetchone():
        conn.close()
        return None, "El usuario ya existe"

    cursor.execute("INSERT INTO login (correo, contrasena) VALUES (%s, %s)", (correo, password))
    conn.commit()
    conn.close()
    return {"correo": correo}, "Usuario registrado exitosamente"
