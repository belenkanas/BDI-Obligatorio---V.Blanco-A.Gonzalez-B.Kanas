use obligatorio;

/*Login*/
INSERT INTO obligatorio.login(correo, contraseña)
VALUES ('valentina.blanco@correo.ucu.edu.uy', 'valentina123'),
       ('mariabelen.kanas@correo.ucu.edu.uy', '12345678765'),
       ('andrea.gonzalez@correo.ucu.edu.uy', 'irry834dj'),
       ('juan.perez@correo.ucu.edu.uy', 'njre74382p'),
       ('ana.lopez@correo.ucu.edu.uy', '12345678'),
       ('maria.gomez@correo.ucu.edu.uy', 'njergiuw325'),
       ('paz.garcia@correo.ucu.edu.uy', '6734vbibgiw'),
       ('pedro.silva@correo.ucu.edu.uy', 'ucu8932ohwel'),
       ('jose.martinez@correo.ucu.edu.uy', 'hureik213'),
       ('luis.sanchez@correo.ucu.edu.uy', 'fre2y89w');

/*Participante*/
INSERT INTO obligatorio.participante(ci, nombre, apellido, email)
VALUES
('55910880', 'Valentina', 'Blanco', (SELECT correo FROM login WHERE correo='valentina.blanco@correo.ucu.edu.uy')),
('55667788', 'María Belén', 'Kanas', (SELECT correo FROM login WHERE correo='mariabelen.kanas@correo.ucu.edu.uy')),
('55788998', 'Andrea', 'González', (SELECT correo FROM login WHERE correo='andrea.gonzalez@correo.ucu.edu.uy')),
('55938753', 'Juan', 'Pérez', (SELECT correo FROM login WHERE correo='juan.perez@correo.ucu.edu.uy')),
('58902345', 'Ana', 'López', (SELECT correo FROM login WHERE correo='ana.lopez@correo.ucu.edu.uy')),
('45676543', 'María', 'Gómez', (SELECT correo FROM login WHERE correo='maria.gomez@correo.ucu.edu.uy')),
('57876550', 'Paz', 'García', (SELECT correo FROM login WHERE correo='paz.garcia@correo.ucu.edu.uy')),
('57541231', 'Pedro', 'Silva', (SELECT correo FROM login WHERE correo='pedro.silva@correo.ucu.edu.uy')),
('53234567', 'José', 'Martínez', (SELECT correo FROM login WHERE correo='jose.martinez@correo.ucu.edu.uy')),
('55875921', 'Luis', 'Sánchez', (SELECT correo FROM login WHERE correo='luis.sanchez@correo.ucu.edu.uy'));

/*Facultad*/
INSERT INTO obligatorio.facultad (nombre) VALUES
('Facultad de Ciencias Empresariales'),
('Facultad de Derecho y Ciencias Humanas'),
('Facultad de Ingeniería y Tecnologías'),
('Facultad de Ciencias de la Salud'),
('Facultad de Humanidades y Artes Liberales'),
('Facultad de Psicología y Bienestar Humano');

/*Programa académico*/
INSERT INTO obligatorio.programa_academico (nombre_programa, id_facultad, tipo)
VALUES
('Ingeniería en Informática', (SELECT id_facultad FROM facultad WHERE nombre = 'Facultad de Ingeniería y Tecnologías'), 'grado'),
('Administración de Empresas', (SELECT id_facultad FROM facultad WHERE nombre = 'Facultad de Ciencias Empresariales'), 'grado'),
('Psicología Clínica', (SELECT id_facultad FROM facultad WHERE nombre = 'Facultad de Psicología y Bienestar Humano'), 'grado'),
('Derecho', (SELECT id_facultad FROM facultad WHERE nombre = 'Facultad de Derecho y Ciencias Humanas'), 'grado'),
('Licenciatura en Comunicación', (SELECT id_facultad FROM facultad WHERE nombre = 'Facultad de Humanidades y Artes Liberales'), 'grado'),
('Maestría en Ingeniería de Software', (SELECT id_facultad FROM facultad WHERE nombre = 'Facultad de Ingeniería y Tecnologías'), 'postgrado'),
('Maestría en Administración (MBA)', (SELECT id_facultad FROM facultad WHERE nombre = 'Facultad de Ciencias Empresariales'), 'postgrado'),
('Especialización en Neuropsicología', (SELECT id_facultad FROM facultad WHERE nombre = 'Facultad de Psicología y Bienestar Humano'), 'postgrado');


/*Participante Programa Académico*/
INSERT INTO obligatorio.participante_programa_academico (ci_participante, nombre_programa, rol)
VALUES
((SELECT ci FROM participante WHERE nombre='Valentina' AND apellido='Blanco'), 'Ingeniería en Informática', 'alumno'),
((SELECT ci FROM participante WHERE nombre='María Belén' AND apellido='Kanas'), 'Licenciatura en Comunicación', 'alumno'),
((SELECT ci FROM participante WHERE nombre='Andrea' AND apellido='González'), 'Derecho', 'alumno'),
((SELECT ci FROM participante WHERE nombre='Juan' AND apellido='Pérez'), 'Maestría en Ingeniería de Software', 'alumno'),
((SELECT ci FROM participante WHERE nombre='Ana' AND apellido='López'), 'Maestría en Administración (MBA)', 'alumno'),
((SELECT ci FROM participante WHERE nombre='María' AND apellido='Gómez'), 'Psicología Clínica', 'docente'),
((SELECT ci FROM participante WHERE nombre='Paz' AND apellido='García'), 'Especialización en Neuropsicología', 'alumno'),
((SELECT ci FROM participante WHERE nombre='Pedro' AND apellido='Silva'), 'Ingeniería en Informática', 'docente'),
((SELECT ci FROM participante WHERE nombre='José' AND apellido='Martínez'), 'Administración de Empresas', 'docente'),
((SELECT ci FROM participante WHERE nombre='Luis' AND apellido='Sánchez'), 'Derecho', 'docente');

/*Edificios*/
INSERT INTO obligatorio.edificio(nombre_edificio, direccion, departamento)
VALUES ('Edificio San José', 'Av. 8 de Octubre 2733', 'Departamento de Medicina'),
       ('Edificio Semprún', 'Estero Bellaco 2771', 'Departamento de Economía y Negocios'),
       ('Edificio Mullin', 'Comandante Braga 2715', 'Departamento de Ingeniería'),
       ('Edificio San Ignacio', 'Cornelio Cantera 2733', 'Departamento de Ciencias Sociales'),
       ('Edificio Athanasius', 'Gral. Urquiza 2871', 'Departamento de Humanidades y Comunicación'),
       ('Edificio Madre Marta', 'Av. Garibaldi 2831', 'Departamento de Psicología'),
       ('Edificio Sacré Coeur', 'Av. 8 de Octubre 2738', 'Departamento de Derecho');

/*Salas*/
INSERT INTO obligatorio.sala (nombre_sala, edificio, capacidad, tipo_sala)
VALUES
('Aula Magna', 'Edificio Sacré Coeur', 200, 'libre'),
('Sala Zoom', 'Edificio Semprún', 50, 'postgrado'),
('Cowork de Ludus', 'Edificio Sacré Coeur', 35, 'docente'),
('Laboratorio', 'Edificio Mullin', 100, 'libre'),
('TI3', 'Edificio Sacré Coeur', 50, 'libre'),
('Sala del silencio', 'Edificio San Ignacio', 5, 'libre'),
('Sala de docentes', 'Edificio San José', 20, 'docente'),
('Sala de postgrados', 'Edificio Madre Marta', 40, 'postgrado'),
('Sala de grabación', 'Edificio Athanasius', 40, 'libre');

/*Turnos*/
INSERT INTO obligatorio.turno (hora_inicio, hora_fin) VALUES
('08:00:00', '09:00:00'),
('09:00:00', '10:00:00'),
('10:00:00', '11:00:00'),
('11:00:00', '12:00:00'),
('12:00:00', '13:00:00'),
('13:00:00', '14:00:00'),
('14:00:00', '15:00:00'),
('15:00:00', '16:00:00'),
('16:00:00', '17:00:00'),
('17:00:00', '18:00:00'),
('18:00:00', '19:00:00'),
('19:00:00', '20:00:00'),
('20:00:00', '21:00:00'),
('21:00:00', '22:00:00');

/*Reservas*/
INSERT INTO obligatorio.reserva (nombre_sala, edificio, fecha, id_turno, estado)
VALUES
('Aula Magna', 'Edificio Sacré Coeur', '2025-10-28 00:00:00', 3, 'activa'),
('Sala Zoom', 'Edificio Semprún', '2025-10-28 00:00:00', 4, 'finalizada'),
('Laboratorio', 'Edificio Mullin', '2025-10-29 00:00:00', 6, 'cancelada'),
('Sala del silencio', 'Edificio San Ignacio', '2025-10-29 00:00:00', 8, 'activa'),
('Sala de postgrados', 'Edificio Madre Marta', '2025-10-30 00:00:00', 10, 'sin asistencia');


/*Reservas por participante*/
INSERT INTO obligatorio.reserva_participante (ci_participante, id_reserva, fecha_solicitud_reserva, asistencia)
VALUES
((SELECT ci FROM participante WHERE nombre='Valentina' AND apellido='Blanco'), 1, '2025-10-25 10:00:00', TRUE),
((SELECT ci FROM participante WHERE nombre='María Belén' AND apellido='Kanas'), 2, '2025-10-25 11:30:00', TRUE),
((SELECT ci FROM participante WHERE nombre='Andrea' AND apellido='González'), 3, '2025-10-26 09:00:00', FALSE),
((SELECT ci FROM participante WHERE nombre='Juan' AND apellido='Pérez'), 4, '2025-10-26 10:45:00', TRUE),
((SELECT ci FROM participante WHERE nombre='Ana' AND apellido='López'), 5, '2025-10-27 08:00:00', FALSE);

/*Sanciones*/
INSERT INTO obligatorio.sancion_participante(ci_participante, fecha_inicio, fecha_fin)
VALUES
((SELECT ci FROM participante WHERE nombre='Andrea' AND apellido='González'), '2025-10-27 00:00:00', '2025-11-03 00:00:00'),
((SELECT ci FROM participante WHERE nombre='Ana' AND apellido='López'), '2025-10-30 00:00:00', '2025-11-06 00:00:00'),
((SELECT ci FROM participante WHERE nombre='Paz' AND apellido='García'), '2025-09-15 00:00:00', '2025-09-22 00:00:00'),
((SELECT ci FROM participante WHERE nombre='Pedro' AND apellido='Silva'), '2025-10-10 00:00:00', '2025-10-17 00:00:00'),
((SELECT ci FROM participante WHERE nombre='José' AND apellido='Martínez'), '2025-10-20 00:00:00', '2025-10-27 00:00:00');