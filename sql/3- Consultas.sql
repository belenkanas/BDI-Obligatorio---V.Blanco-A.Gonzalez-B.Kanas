USE obligatorio;

/*    salas más reservadas    */
SELECT s.nombre_sala, COUNT(r.id_reserva) AS masReservada
FROM obligatorio.reserva r
JOIN obligatorio.sala s ON r.id_sala = s.id_sala
GROUP BY s.nombre_sala
ORDER BY masReservada DESC;

/*    turnos más demandados    */
SELECT t.id_turno, t.hora_inicio, t.hora_fin, COUNT(r.id_reserva) AS masDemandados
FROM obligatorio.turno t
JOIN obligatorio.reserva r ON t.id_turno = r.id_turno
GROUP BY t.id_turno, t.hora_inicio, t.hora_fin
ORDER BY masDemandados DESC;

/*    promedio de participantes por sala    */
SELECT s.nombre_sala, AVG(subQuery.cantidad_participantes) AS promedio_participantes
FROM (SELECT r.id_sala, COUNT(rp.ci_participante) AS cantidad_participantes
      FROM obligatorio.reserva r
      JOIN obligatorio.reserva_participante rp ON r.id_reserva = rp.id_reserva
      GROUP BY r.id_reserva, r.id_sala) AS subQuery
JOIN obligatorio.sala s ON subQuery.id_sala = s.id_sala
GROUP BY s.nombre_sala
ORDER BY promedio_participantes DESC;

/*    cantidad de reservas por carrera y facultad    */
SELECT f.nombre, pa.nombre_programa, COUNT(DISTINCT r.id_reserva) AS cantidad_reservas
FROM obligatorio.reserva r
JOIN obligatorio.reserva_participante rp ON r.id_reserva = rp.id_reserva
JOIN obligatorio.participante_programa_academico ppa ON rp.ci_participante = ppa.ci_participante
JOIN obligatorio.programa_academico pa ON ppa.id_programa = pa.id_programa
JOIN obligatorio.facultad f ON pa.id_facultad = f.id_facultad
GROUP BY f.nombre, pa.nombre_programa
ORDER BY cantidad_reservas DESC;

/*    porcentaje de ocupación de salas por edificio    */
SELECT e.nombre_edificio, (SUM(reservas_sala.participantes) / SUM(s.capacidad)) * 100 AS porcentaje_ocupacion
FROM (
      SELECT r.id_sala, COUNT(rp.ci_participante) AS participantes
      FROM obligatorio.reserva r
      JOIN obligatorio.reserva_participante rp ON r.id_reserva = rp.id_reserva
      GROUP BY r.id_sala
      ) AS reservas_sala
JOIN obligatorio.sala s ON reservas_sala.id_sala = s.id_sala
JOIN obligatorio.edificio e ON s.id_edificio = e.id_edificio
GROUP BY e.nombre_edificio
ORDER BY porcentaje_ocupacion DESC;

/*    cantidad de reservas y asistencias de profesores y alumnos (grado y posgrado)    */
SELECT ppa.rol, pa.tipo, COUNT(DISTINCT rp.id_reserva) AS reservas, SUM(rp.asistencia) AS asistencias
FROM obligatorio.reserva_participante rp
JOIN obligatorio.participante_programa_academico ppa ON ppa.ci_participante = rp.ci_participante
JOIN obligatorio.programa_academico pa ON pa.id_programa = ppa.id_programa
GROUP BY ppa.rol, pa.tipo
ORDER BY ppa.rol, pa.tipo;

/*    cantidad de sanciones para profesores y alumnos (grado y posgrado)    */
SELECT ppa.rol, pa.tipo, COUNT(*) AS sanciones
FROM obligatorio.sancion_participante sp
JOIN obligatorio.participante_programa_academico ppa ON sp.ci_participante = ppa.ci_participante
JOIN obligatorio.programa_academico pa ON ppa.id_programa = pa.id_programa
GROUP BY ppa.rol, pa.tipo
ORDER BY ppa.rol, pa.tipo;

/*    porcentaje de reservas efectivamente utilizadas vs. canceladas/no asistidas    */
SELECT ((SELECT COUNT(*)
         FROM obligatorio.reserva r
         WHERE r.estado = 'activa' OR r.estado = 'finalizada') / (SELECT COUNT(*) FROM obligatorio.reserva) * 100) AS porcentaje_utilizadas,
        ((SELECT COUNT(*)
          FROM obligatorio.reserva r
          WHERE r.estado = 'cancelada' OR r.estado = 'sin_asistencia') / (SELECT COUNT(*) FROM obligatorio.reserva) * 100) AS porcentaje_canceladas;

/*     Agregadas    */

/*    salas sin ninguna reserva   */
SELECT s.nombre_sala, e.nombre_edificio
FROM obligatorio.sala s
JOIN obligatorio.edificio e ON s.id_edificio = e.id_edificio
LEFT JOIN obligatorio.reserva r ON r.id_sala= s.id_sala
WHERE r.id_reserva IS NULL
ORDER BY e.nombre_edificio, s.nombre_sala;

/*    Participantes que más cancelan(se podrían aplicar sanciones más severas) */
SELECT rp.ci_participante, COUNT(*) AS reservas_totales, SUM(r.estado IN ('cancelada','sin_asistencia')) AS no_efectivas, ROUND(100 * SUM(r.estado IN ('cancelada','sin_asistencia')) / COUNT(*), 1) AS cuanta_cancelacion
FROM obligatorio.reserva r
JOIN obligatorio.reserva_participante rp ON rp.id_reserva = r.id_reserva
GROUP BY rp.ci_participante
HAVING COUNT(*) >= 3
ORDER BY cuanta_cancelacion DESC, reservas_totales DESC;

/*    Programas que más usan los edificios   */
SELECT pa.nombre_programa, COUNT(DISTINCT e.id_edificio) AS edificios_usados
FROM obligatorio.reserva r
JOIN obligatorio.sala s ON r.id_sala = s.id_sala
JOIN obligatorio.edificio e ON s.id_edificio = e.id_edificio
JOIN obligatorio.reserva_participante rp ON rp.id_reserva = r.id_reserva
JOIN obligatorio.participante_programa_academico ppa ON ppa.ci_participante = rp.ci_participante
JOIN obligatorio.programa_academico pa ON pa.id_programa = ppa.id_programa
GROUP BY pa.nombre_programa
ORDER BY edificios_usados DESC, pa.nombre_programa;