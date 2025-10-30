use obligatorio;

/*    salas más reservadas    */
SELECT r.nombre_sala, COUNT(r.id_reserva) AS masReservada
FROM obligatorio.reserva r
GROUP BY r.nombre_sala
ORDER BY masReservada DESC;

/*    turnos más demandados    */
SELECT t.id_turno, t.hora_inicio, t.hora_fin, COUNT(t.id_turno) AS masDemandados
FROM obligatorio.turno t
GROUP BY t.id_turno, t.hora_inicio, t.hora_fin
ORDER BY masDemandados DESC;

/*    promedio de participantes por sala    */
SELECT subQuery.nombre_sala, AVG(subQuery.cantidad_participantes) AS promedio
FROM (SELECT r.nombre_sala, COUNT(rp.ci_participante) AS cantidad_participantes
      FROM obligatorio.reserva r
      JOIN obligatorio.reserva_participante rp ON r.id_reserva = rp.id_reserva
      GROUP BY r.id_reserva, r.nombre_sala) AS subQuery
GROUP BY subQuery.nombre_sala
ORDER BY promedio DESC;

/*    cantidad de reservas por carrera y facultad    */
SELECT f.nombre, pa.nombre_programa, COUNT(DISTINCT r.id_reserva) AS cantidad_reservas
FROM obligatorio.reserva r
JOIN obligatorio.reserva_participante rp ON r.id_reserva = rp.id_reserva
JOIN obligatorio.participante_programa_academico ppa ON rp.ci_participante = ppa.ci_participante
JOIN obligatorio.programa_academico pa ON ppa.nombre_programa = pa.nombre_programa
JOIN obligatorio.facultad f ON pa.id_facultad = f.id_facultad
GROUP BY f.nombre, pa.nombre_programa
ORDER BY cantidad_reservas DESC;

/*    porcentaje de ocupación de salas por edificio    */
SELECT s.edificio, (SUM(participantes) / SUM(s.capacidad)) * 100 AS porcentaje
FROM (SELECT r.nombre_sala, r.edificio, COUNT(rp.ci_participante) AS participantes
      FROM obligatorio.reserva r
      JOIN obligatorio.reserva_participante rp ON r.id_reserva = rp.id_reserva
      GROUP BY r.nombre_sala, r.edificio) AS reservas_sala
JOIN obligatorio.sala s ON reservas_sala.edificio = s.edificio AND reservas_sala.nombre_sala = s.nombre_sala
GROUP BY s.edificio
ORDER BY porcentaje DESC;

/*    cantidad de reservas y asistencias de profesores y alumnos (grado y posgrado)    */
SELECT ppa.rol, pa.tipo, COUNT(DISTINCT rp.id_reserva) AS reservas, SUM(rp.asistencia) AS asistencias
FROM obligatorio.reserva_participante rp
JOIN obligatorio.participante_programa_academico ppa ON ppa.ci_participante = rp.ci_participante
JOIN obligatorio.programa_academico pa ON pa.nombre_programa = ppa.nombre_programa
GROUP BY ppa.rol, pa.tipo
ORDER BY ppa.rol, pa.tipo;

/*    cantidad de sanciones para profesores y alumnos (grado y posgrado)    */
SELECT ppa.rol, pa.tipo, COUNT(*) AS sanciones
FROM obligatorio.sancion_participante sp
JOIN obligatorio.participante_programa_academico ppa ON sp.ci_participante = ppa.ci_participante
JOIN obligatorio.programa_academico pa ON ppa.nombre_programa = pa.nombre_programa
GROUP BY ppa.rol, pa.tipo
ORDER BY ppa.rol, pa.tipo;

/*    porcentaje de reservas efectivamente utilizadas vs. canceladas/no asistidas    */
SELECT ((SELECT COUNT(*)
         FROM obligatorio.reserva r
         WHERE r.estado = 'activa' OR r.estado = 'finalizada') / (SELECT COUNT(*) FROM obligatorio.reserva) * 100) AS porcentaje_utilizadas,
        ((SELECT COUNT(*)
          FROM obligatorio.reserva r
          WHERE r.estado = 'cancelada' OR r.estado = 'sin asistencia') / (SELECT COUNT(*) FROM obligatorio.reserva) * 100) AS porcentaje_canceladas;

/*     Agregadas    */

/*    salas sin ninguna reserva   */
SELECT s.nombre_sala, s.edificio
FROM obligatorio.sala s
LEFT JOIN obligatorio.reserva r ON r.nombre_sala= s.nombre_sala
WHERE r.id_reserva IS NULL
ORDER BY s.edificio, s.nombre_sala;

/*    Participantes que más cancelan  (se podrían aplicar sanciones más severas) */
SELECT rp.ci_participante, COUNT(*) AS reservas_totales, SUM(r.estado IN ('cancelada','sin asistencia')) AS no_efectivas, ROUND(100 * SUM(r.estado IN ('cancelada','sin asistencia')) / COUNT(*), 1) AS cuanta_cancelacion
FROM obligatorio.reserva r
JOIN obligatorio.reserva_participante rp ON rp.id_reserva = r.id_reserva
GROUP BY rp.ci_participante
HAVING COUNT(*) >= 3
ORDER BY cuanta_cancelacion_ DESC, reservas_totales DESC;

/*    Programas que más usan los edificios   */
SELECT pa.nombre_programa, COUNT(DISTINCT r.edificio) AS edificios_usados
FROM obligatorio.reserva r
JOIN obligatorio.reserva_participante rp ON rp.id_reserva = r.id_reserva
JOIN obligatorio.participante_programa_academico ppa ON ppa.ci_participante = rp.ci_participante
JOIN obligatorio.programa_academico pa ON pa.nombre_programa = ppa.nombre_programa
GROUP BY pa.nombre_programa
ORDER BY edificios_usados DESC, pa.nombre_programa;