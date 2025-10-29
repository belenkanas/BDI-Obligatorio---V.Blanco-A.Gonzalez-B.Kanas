use obligatorio;

/*    salas más reservadas    */
SELECT r.nombre_sala, COUNT(r.id_reserva) AS masReservada
FROM reserva r
GROUP BY r.nombre_sala
ORDER BY masReservada DESC;

/*    turnos más demandados    */
SELECT t.id_turno, t.hora_inicio, t.hora_fin, COUNT(t.id_turno) AS masDemandados
FROM turno t
GROUP BY t.id_turno, t.hora_inicio, t.hora_fin
ORDER BY masDemandados DESC;

/*    promedio de participantes por sala    */
SELECT subQuery.nombre_sala, AVG(subQuery.cantidad_participantes) AS promedio
FROM (SELECT r.nombre_sala, COUNT(rp.ci_participante) AS cantidad_participantes
      FROM reserva r
      JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
      GROUP BY r.id_reserva, r.nombre_sala) AS subQuery
GROUP BY subQuery.nombre_sala
ORDER BY promedio DESC;

/*    cantidad de reservas por carrera y facultad    */
SELECT f.nombre, pa.nombre_programa, COUNT(DISTINCT r.id_reserva) AS cantidad_reservas
FROM reserva r
JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
JOIN participante_programa_academico ppa ON rp.ci_participante = ppa.ci_participante
JOIN programa_academico pa ON ppa.nombre_programa = pa.nombre_programa
JOIN facultad f ON pa.id_facultad = f.id_facultad
GROUP BY f.nombre, pa.nombre_programa
ORDER BY cantidad_reservas DESC;

/*    porcentaje de ocupación de salas por edificio    */
SELECT s.edificio, (SUM(participantes) / SUM(s.capacidad)) * 100 AS porcentaje
FROM (SELECT r.nombre_sala, r.edificio, COUNT(rp.ci_participante) AS participantes
      FROM reserva r
      JOIN reserva_participante rp ON r.id_reserva = rp.id_reserva
      GROUP BY r.nombre_sala, r.edificio) AS reservas_sala
JOIN sala s ON reservas_sala.edificio = s.edificio AND reservas_sala.nombre_sala = s.nombre_sala
GROUP BY s.edificio
ORDER BY porcentaje DESC;

/*    cantidad de reservas y asistencias de profesores y alumnos (grado y posgrado)    */
SELECT ppa.rol, pa.tipo, COUNT(DISTINCT rp.id_reserva) AS reservas, SUM(rp.asistencia) AS asistencias
FROM reserva_participante rp
JOIN participante_programa_academico ppa ON ppa.ci_participante = rp.ci_participante
JOIN programa_academico pa ON pa.nombre_programa = ppa.nombre_programa
GROUP BY ppa.rol, pa.tipo
ORDER BY ppa.rol, pa.tipo;

/*    cantidad de sanciones para profesores y alumnos (grado y posgrado)    */
SELECT ppa.rol, pa.tipo, COUNT(*) AS sanciones
FROM sancion_participante sp
JOIN participante_programa_academico ppa ON sp.ci_participante = ppa.ci_participante
JOIN programa_academico pa ON ppa.nombre_programa = pa.nombre_programa
GROUP BY ppa.rol, pa.tipo
ORDER BY ppa.rol, pa.tipo;

/*    porcentaje de reservas efectivamente utilizadas vs. canceladas/no asistidas    */
SELECT ((SELECT COUNT(*)
         FROM reserva r
         WHERE r.estado = 'activa' OR r.estado = 'finalizada') / (SELECT COUNT(*) FROM reserva) * 100) AS porcentaje_utilizadas,
        ((SELECT COUNT(*)
          FROM reserva r
          WHERE r.estado = 'cancelada' OR r.estado = 'sin asistencia') / (SELECT COUNT(*) FROM reserva) * 100) AS porcentaje_canceladas;
