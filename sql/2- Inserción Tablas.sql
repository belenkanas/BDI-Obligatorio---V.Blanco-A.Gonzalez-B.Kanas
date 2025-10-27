INSERT INTO login(correo, contraseña)
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

INSERT INTO participante(ci, nombre, apellido, email)
VALUES ('55910880', 'Valentina', 'Blanco', 'valentina.blanco@correo.ucu.edu.uy'),
       ('55667788', 'María Belén', 'Kanas', 'mariabelen.kanas@correo.ucu.edu.uy'),
       ('55788998', 'Andrea', 'González', 'andrea.gonzalez@correo.ucu.edu.uy'),
       ('55938753', 'Juan', 'Pérez', 'juan.perez@correo.ucu.edu.uy'),
       ('58902345', 'Ana', 'López', 'ana.lopez@correo.ucu.edu.uy'),
       ('45676543', 'María', 'Gómez', 'maria.gomez@correo.ucu.edu.uy'),
       ('57876550', 'Paz', 'García', 'paz.garcia@correo.ucu.edu.uy'),
       ('57541231', 'Pedro', 'Silva', 'pedro.silva@correo.ucu.edu.uy'),
       ('53234567', 'José', 'Martínez', 'jose.martinez@correo.ucu.edu.uy'),
       ('55875921', 'Luis', 'Sánchez', 'luis.sanchez@correo.ucu.edu.uy');

INSERT INTO facultad(id_facultad, nombre)
VALUES (1, 'Facultad de Ciencias Empresariales'),
       (2, 'Facultad de Derecho y Ciencias Humanas'),
       (3, 'Facultad de Ingeniería y Tecnologías'),
       (4, 'Facultad de Ciencias de la Salud'),
       (5, 'Facultad de Humanidades y Artes Liberales'),
       (6, 'Facultad de Psicología y Bienestar Humano');

INSERT INTO edificio(nombre_edificio, direccion, departamento)
VALUES ('Edificio San José', 'Av. 8 de Octubre 2733', 'Departamento de Medicina'),
       ('Edificio Semprún', 'Estero Bellaco 2771', 'Departamento de Economía y Negocios'),
       ('Edificio Mullin', 'Comandante Braga 2715', 'Departamento de Ingeniería'),
       ('Edificio San Ignacio', 'Cornelio Cantera 2733', 'Departamento de Ciencias Sociales'),
       ('Edificio Athanasius', 'Gral. Urquiza 2871', 'Departamento de Humanidades y Comunicación'),
       ('Edificio Madre Marta', 'Av. Garibaldi 2831', 'Departamento de Psicología'),
       ('Edificio Sacré Coeur', 'Av. 8 de Octubre 2738', 'Departamento de Derecho');

INSERT INTO sala(nombre_sala, edificio, capacidad, tipo_sala)
VALUES ('Aula Magna', 'Edificio Sacré Coeur', 200, 'libre'),
       ('Sala Zoom', 'Edificio Semprún', 50, 'postgrado'),
       ('Cowork de Ludus', 'Edificio Sacré Coeur', 35, 'docente'),
       ('Laboratorio', 'Edificio Mullin', 100, 'libre'),
       ('TI3', 'Edificio Sacré Coeur', 50, 'libre'),
       ('Sala del silencio', 'Edificio San Ignacio', 5, 'libre'),
       ('Sala de docentes', 'Edificio San José',  20, 'docente'),
       ('Sala de postgrados', 'Edificio Madre Marta', 40, 'postgrado'),
       ('Sala de grabación', 'Edificio Athanasius', 40, 'libre');

INSERT INTO turno(id_turno, hora_inicio, hora_fin)
VALUES (1, '08:00:00', '09:00:00'),
       (2, '09:00:00', '10:00:00'),
       (3, '10:00:00', '11:00:00'),
       (4, '11:00:00', '12:00:00'),
       (5, '12:00:00', '13:00:00'),
       (6, '13:00:00', '14:00:00'),
       (7, '14:00:00', '15:00:00'),
       (8, '15:00:00', '16:00:00'),
       (9, '16:00:00', '17:00:00'),
       (10, '17:00:00', '18:00:00'),
       (11, '18:00:00', '19:00:00'),
       (12, '19:00:00', '20:00:00'),
       (13, '20:00:00', '21:00:00'),
       (14, '21:00:00', '22:00:00');