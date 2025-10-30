import mysql.connector

def conexion():
  return mysql.connector.connect(user='root', 
                                 password='rootpassword',
                                 host='127.0.0.1',
                                 database='obligatorio')


def listar_participantes():
  cnx = conexion()
  cursor = cnx.cursor()

  query = ("SELECT * FROM participante")

  cursor.execute(query)
  print("\n--- Lista de Usuarios ---")
  for (ci, nombre, apellido, email) in cursor:
        print(f"{ci} - {nombre} {apellido} ({email})")
  cursor.close()
  cnx.close()

def menu():
    while True:
        print("\nSeleccione una opción:")
        print("1. Listar Participantes")
        opcion = input("Ingrese el número de la opción deseada: ")
        if opcion == '1':
            listar_participantes()
        else:
                print("Opción inválida, intenta de nuevo.")

def salasMasReservadas():
    cnx=conexion()
    cursor=cnx.cursor()

    query = ("""SELECT r.nombre_sala, COUNT(r.id_reserva) AS masReservada
                FROM obligatorio.reserva r
                GROUP BY r.nombre_sala
                ORDER BY masReservada DESC""")
    cursor.execute(query)
    resultado = cursor.fetchall()
    print("\n--- Sala con más reservas---")
    nombre_sala, masReservada = resultado
    print(f"{nombre_sala} con {masReservada}")

    cursor.close()
    cnx.close()

def turnosMasDemandados():
    cnx=conexion()
    cursor=cnx.cursor()

    query =("""SELECT t.id_turno, t.hora_inicio, t.hora_fin, COUNT(t.id_turno) AS masDemandados
                FROM obligatorio.turno t
                GROUP BY t.id_turno, t.hora_inicio, t.hora_fin
                ORDER BY masDemandados DESC""")
    
    cursor.execute(query)
    resultado = cursor.fetchone()

    print("\n--- Turnos más demandados ---")
    hora_inicio, hora_fin, masDemandados = resultado
    print(f"{hora_inicio}/{hora_fin} con {masDemandados}")

    cursor.close()
    cnx.close()
    
def promedioParticipantesPorSala():
    cnx=conexion()
    cursor=cnx.cursor()

    query =("""SELECT subQuery.nombre_sala, AVG(subQuery.cantidad_participantes) AS promedio
                FROM (SELECT r.nombre_sala, COUNT(rp.ci_participante) AS cantidad_participantes
                      FROM obligatorio.reserva r
                      JOIN obligatorio.reserva_participante rp ON r.id_reserva = rp.id_reserva
                      GROUP BY r.id_reserva, r.nombre_sala) AS subQuery
                GROUP BY subQuery.nombre_sala
                ORDER BY promedio DESC""")
    
    cursor.execute(query)
    resultado = cursor.fetchall()

    print("\n--- Promedio de participantes por sala ---")
    nombre_sala, promedio = resultado
    print(f"{nombre_sala}: {promedio} personas")

    cursor.close()
    cnx.close()

def cantReservasPorCarreraYFacultad():
    cnx=conexion()
    cursor=cnx.cursor()

    query =("""SELECT f.nombre, pa.nombre_programa, COUNT(DISTINCT r.id_reserva) AS cantidad_reservas
                FROM obligatorio.reserva r
                JOIN obligatorio.reserva_participante rp ON r.id_reserva = rp.id_reserva
                JOIN obligatorio.participante_programa_academico ppa ON rp.ci_participante = ppa.ci_participante
                JOIN obligatorio.programa_academico pa ON ppa.nombre_programa = pa.nombre_programa
                JOIN obligatorio.facultad f ON pa.id_facultad = f.id_facultad
                GROUP BY f.nombre, pa.nombre_programa
                ORDER BY cantidad_reservas DESC""")
    
    cursor.execute(query)
    resultado = cursor.fetchall()

    print("\n--- Cantidad de reservas por carrera y facultad ---")
    nombre, nombre_programa, cantidad_reservas = resultado
    print(f"{nombre}, {nombre_programa}: {cantidad_reservas}")

    cursor.close()
    cnx.close()

def porcentajeOcupacionSalaPorEdificio():
    cnx=conexion()
    cursor=cnx.cursor()

    query =("""SELECT s.edificio, (SUM(participantes) / SUM(s.capacidad)) * 100 AS porcentaje
                FROM (SELECT r.nombre_sala, r.edificio, COUNT(rp.ci_participante) AS participantes
                      FROM obligatorio.reserva r
                      JOIN obligatorio.reserva_participante rp ON r.id_reserva = rp.id_reserva
                      GROUP BY r.nombre_sala, r.edificio) AS reservas_sala
                JOIN obligatorio.sala s ON reservas_sala.edificio = s.edificio AND reservas_sala.nombre_sala = s.nombre_sala
                GROUP BY s.edificio
                ORDER BY porcentaje DESC""")
    
    cursor.execute(query)
    resultado = cursor.fetchall()

    print("\n--- Porcentaje de ocupación de salas por edificio ---")
    edificio, porcentaje = resultado
    print(f"{edificio}: %{porcentaje:.1f}")

    cursor.close()
    cnx.close()

def cantidadReservasAsistencias():
    cnx=conexion()
    cursor=cnx.cursor()

    query =("""SELECT ppa.rol, pa.tipo, COUNT(DISTINCT rp.id_reserva) AS reservas, SUM(rp.asistencia) AS asistencias
                FROM obligatorio.reserva_participante rp
                JOIN obligatorio.participante_programa_academico ppa ON ppa.ci_participante = rp.ci_participante
                JOIN obligatorio.programa_academico pa ON pa.nombre_programa = ppa.nombre_programa
                GROUP BY ppa.rol, pa.tipo
                ORDER BY ppa.rol, pa.tipo""")
    
    cursor.execute(query)
    resultado = cursor.fetchall()

    print("\n--- Cantidad de reservas y asistencias de profesores y alumnos (grado y posgrado) ---")
    rol, tipo, reservas, asistencias= resultado
    print(f"{rol}, {tipo}: {reservas} reservas, {asistencias} asistencias")

    cursor.close()
    cnx.close()

def cantidadSanciones():
    cnx=conexion()
    cursor=cnx.cursor()

    query =("""SELECT ppa.rol, pa.tipo, COUNT(*) AS sanciones
                FROM obligatorio.sancion_participante sp
                JOIN obligatorio.participante_programa_academico ppa ON sp.ci_participante = ppa.ci_participante
                JOIN obligatorio.programa_academico pa ON ppa.nombre_programa = pa.nombre_programa
                GROUP BY ppa.rol, pa.tipo
                ORDER BY ppa.rol, pa.tipo""")
    
    cursor.execute(query)
    resultado = cursor.fetchall()

    print("\n--- Cantidad de sanciones para profesores y alumnos (grado y posgrado) ---")
    rol, tipo, reservas, sanciones= resultado
    print(f"{rol}, {tipo}: {sanciones} sanciones")

    cursor.close()
    cnx.close()

def porcentajeReservasUsadasCanceladas():
    cnx=conexion()
    cursor=cnx.cursor()

    query =("""SELECT ((SELECT COUNT(*)
              FROM obligatorio.reserva r
              WHERE r.estado = 'activa' OR r.estado = 'finalizada') / (SELECT COUNT(*) FROM obligatorio.reserva) * 100) AS porcentaje_utilizadas,
              ((SELECT COUNT(*)
                FROM obligatorio.reserva r
                WHERE r.estado = 'cancelada' OR r.estado = 'sin asistencia') / (SELECT COUNT(*) FROM obligatorio.reserva) * 100) AS porcentaje_canceladas""")
    
    cursor.execute(query)
    resultado = cursor.fetchall()

    print("\n--- Porcentaje de reservas efectivamente utilizadas vs. canceladas/no asistidas ---")
    porcentaje_utilizadas, porcentaje_canceladas = resultado
    print(f"Utilizadas:{porcentaje_utilizadas:.1f}% Canceladas:{porcentaje_canceladas:.1f}")

    cursor.close()
    cnx.close()

def salaSinReserva():
    cnx=conexion()
    cursor=cnx.cursor()

    query =("""SELECT s.nombre_sala, s.edificio
                FROM obligatorio.sala s
                LEFT JOIN obligatorio.reserva r ON r.nombre_sala= s.nombre_sala
                WHERE r.id_reserva IS NULL
                ORDER BY s.edificio, s.nombre_sala""")
    
    cursor.execute(query)
    resultado = cursor.fetchall()

    print("\n--- Salas sin reservas hechas ---")
    nombre_sala, edificio = resultado
    print(f"{nombre_sala}, {edificio}")

    cursor.close()
    cnx.close()

def participantesQueMasCancelan():
    cnx=conexion()
    cursor=cnx.cursor()

    query =("""SELECT rp.ci_participante, COUNT(*) AS reservas_totales, SUM(r.estado IN ('cancelada','sin asistencia')) AS no_efectivas, ROUND(100 * SUM(r.estado IN ('cancelada','sin asistencia')) / COUNT(*), 1) AS cuanta_cancelacion
              FROM obligatorio.reserva r
              JOIN obligatorio.reserva_participante rp ON rp.id_reserva = r.id_reserva
              GROUP BY rp.ci_participante
              HAVING COUNT(*) >= 3
              ORDER BY cuanta_cancelacion DESC, reservas_totales DESC""")
    
    cursor.execute(query)
    resultado = cursor.fetchall()

    print("\n--- Participantes que mas cancelan ---")
    ci_participante, cuanta_cancelacion = resultado
    print(f"{ci_participante} tasa de cancelación: {cuanta_cancelacion}")

    cursor.close()
    cnx.close()

def programasMasUsanEdificios():
    cnx=conexion()
    cursor=cnx.cursor()

    query =("""SELECT pa.nombre_programa, COUNT(DISTINCT r.edificio) AS edificios_usados
                FROM obligatorio.reserva r
                JOIN obligatorio.reserva_participante rp ON rp.id_reserva = r.id_reserva
                JOIN obligatorio.participante_programa_academico ppa ON ppa.ci_participante = rp.ci_participante
                JOIN obligatorio.programa_academico pa ON pa.nombre_programa = ppa.nombre_programa
                GROUP BY pa.nombre_programa
                ORDER BY edificios_usados DESC, pa.nombre_programa""")
    
    cursor.execute(query)
    resultado = cursor.fetchall()

    print("\n--- Programas que más usan los edificios ---")
    nombre_programa, edificios_usados = resultado
    print(f"{nombre_programa}: {edificios_usados} edificios usados")

    cursor.close()
    cnx.close()


if __name__ == "__main__":
    menu()