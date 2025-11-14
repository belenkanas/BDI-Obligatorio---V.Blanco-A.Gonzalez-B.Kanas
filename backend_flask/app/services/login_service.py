from app.database.conexion_db import conexion

def login(correo, password):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM login WHERE correo = %s AND contraseña = %s", (correo, password))
    usuario = cursor.fetchone()
    conn.close()

    return usuario


def register_user(correo, password):
    conn = conexion()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM login WHERE correo = %s", (correo,))
    if cursor.fetchone():
        conn.close()
        return None, "El usuario ya existe"

    cursor.execute("INSERT INTO login (correo, contraseña) VALUES (%s, %s)", (correo, password))
    conn.commit()
    conn.close()
    return {"correo": correo}, "Usuario registrado exitosamente"
