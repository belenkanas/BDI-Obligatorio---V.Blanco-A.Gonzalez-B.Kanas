-- Este script une lo ya hecho en Creacion de Base e Inserción Tablas.
-- La idea es que se corra como script cuando se levante el contenedor

DROP DATABASE IF EXISTS obligatorio;
CREATE DATABASE obligatorio CHARACTER SET utf8 COLLATE utf8_spanish_ci;
USE obligatorio;

-- Creacion de tablas:
CREATE TABLE login(
  correo VARCHAR(255) NOT NULL,
  contraseña VARCHAR(255) NOT NULL,
  PRIMARY KEY (correo)
);

CREATE TABLE participante(
  ci VARCHAR(8) NOT NULL,
  nombre VARCHAR(50) NOT NULL,
  apellido VARCHAR(50) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  PRIMARY KEY (ci),
  FOREIGN KEY (email) REFERENCES login(correo)
);

CREATE TABLE facultad(
  id_facultad INT AUTO_INCREMENT,
  nombre VARCHAR(255) NOT NULL,
  PRIMARY KEY (id_facultad)
);

CREATE TABLE programa_academico(
  id_programa INT AUTO_INCREMENT,
  nombre_programa VARCHAR(50) NOT NULL,
  id_facultad INT NOT NULL,
  tipo ENUM('grado', 'posgrado') NOT NULL,
  PRIMARY KEY (id_programa),
  FOREIGN KEY (id_facultad) REFERENCES facultad(id_facultad),
  UNIQUE (nombre_programa, id_facultad)
);

CREATE TABLE participante_programa_academico(
  id_alumno_programa INT AUTO_INCREMENT,
  ci_participante VARCHAR(8) NOT NULL,
  id_programa INT NOT NULL,
  rol ENUM('alumno', 'docente', 'admin') NOT NULL,
  PRIMARY KEY (id_alumno_programa),
  FOREIGN KEY (ci_participante) REFERENCES participante(ci),
  FOREIGN KEY (id_programa) REFERENCES programa_academico(id_programa)
);

CREATE TABLE edificio(
  id_edificio INT AUTO_INCREMENT,
  nombre_edificio VARCHAR(255) NOT NULL,
  direccion VARCHAR(255) NOT NULL,
  departamento VARCHAR(255),
  PRIMARY KEY (id_edificio)
);

CREATE TABLE sala(
  id_sala INT AUTO_INCREMENT,
  nombre_sala VARCHAR(255) NOT NULL,
  id_edificio INT NOT NULL,
  capacidad INT NOT NULL,
  tipo_sala ENUM('libre', 'posgrado', 'docente') NOT NULL,
  PRIMARY KEY (id_sala),
  FOREIGN KEY (id_edificio) REFERENCES edificio(id_edificio),
  UNIQUE (nombre_sala, id_edificio)
);

CREATE TABLE turno(
  id_turno INT AUTO_INCREMENT,
  hora_inicio TIME NOT NULL,
  hora_fin TIME NOT NULL,
  PRIMARY KEY (id_turno)
);

CREATE TABLE reserva(
  id_reserva INT AUTO_INCREMENT,
  id_sala INT NOT NULL,
  fecha DATE NOT NULL,
  id_turno INT NOT NULL,
  estado ENUM('activa', 'cancelada', 'sin_asistencia', 'finalizada') NOT NULL,
  PRIMARY KEY (id_reserva),
  FOREIGN KEY (id_sala) REFERENCES sala(id_sala),
  FOREIGN KEY (id_turno) REFERENCES turno(id_turno),
  UNIQUE KEY uq_reserva_activa (id_sala, fecha, id_turno, estado)
);

CREATE TABLE reserva_participante(
  ci_participante VARCHAR(8) NOT NULL,
  id_reserva INT NOT NULL,
  fecha_solicitud_reserva DATETIME NOT NULL,
  asistencia BOOLEAN DEFAULT FALSE,
  PRIMARY KEY (ci_participante, id_reserva),
  FOREIGN KEY (ci_participante) REFERENCES participante(ci),
  FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva)
);

CREATE TABLE sancion_participante(
  id_sancion INT AUTO_INCREMENT,
  ci_participante VARCHAR(8) NOT NULL,
  fecha_inicio DATE NOT NULL,
  fecha_fin DATE NOT NULL,
  PRIMARY KEY (id_sancion),
  FOREIGN KEY (ci_participante) REFERENCES participante(ci)
);

-- Inserciones de tabla

INSERT INTO login (correo, contraseña) VALUES
('valentina.blanco@correo.ucu.edu.uy', 'valentina123'),
('mariabelen.kanas@correo.ucu.edu.uy', '12345678765'),
('andrea.gonzalez@correo.ucu.edu.uy', 'irry834dj'),
('juan.perez@correo.ucu.edu.uy', 'njre74382p'),
('ana.lopez@correo.ucu.edu.uy', '12345678'),
('maria.gomez@correo.ucu.edu.uy', 'njergiuw325'),
('paz.garcia@correo.ucu.edu.uy', '6734vbibgiw'),
('pedro.silva@correo.ucu.edu.uy', 'ucu8932ohwel'),
('jose.martinez@correo.ucu.edu.uy', 'hureik213'),
('luis.sanchez@correo.ucu.edu.uy', 'fre2y89w'),
('admin@correo.ucu.edu.uy', 'admin123');

-- PARTICIPANTE
INSERT INTO participante (ci, nombre, apellido, email)
VALUES
('55910880', 'Valentina', 'Blanco', 'valentina.blanco@correo.ucu.edu.uy'),
('55667788', 'María Belén', 'Kanas', 'mariabelen.kanas@correo.ucu.edu.uy'),
('55788998', 'Andrea', 'González', 'andrea.gonzalez@correo.ucu.edu.uy'),
('55938753', 'Juan', 'Pérez', 'juan.perez@correo.ucu.edu.uy'),
('58902345', 'Ana', 'López', 'ana.lopez@correo.ucu.edu.uy'),
('45676543', 'María', 'Gómez', 'maria.gomez@correo.ucu.edu.uy'),
('57876550', 'Paz', 'García', 'paz.garcia@correo.ucu.edu.uy'),
('57541231', 'Pedro', 'Silva', 'pedro.silva@correo.ucu.edu.uy'),
('53234567', 'José', 'Martínez', 'jose.martinez@correo.ucu.edu.uy'),
('55875921', 'Luis', 'Sánchez', 'luis.sanchez@correo.ucu.edu.uy'),
('11111111', 'Administrador', 'Ucu', 'admin@correo.ucu.edu.uy');

-- FACULTADES
INSERT INTO facultad (nombre) VALUES
('Facultad de Ciencias Empresariales'),
('Facultad de Derecho y Ciencias Humanas'),
('Facultad de Ingeniería y Tecnologías'),
('Facultad de Ciencias de la Salud'),
('Facultad de Humanidades y Artes Liberales'),
('Facultad de Psicología y Bienestar Humano');

-- PROGRAMAS
INSERT INTO programa_academico (nombre_programa, id_facultad, tipo)
VALUES
('Ingeniería en Informática', 3, 'grado'),
('Administración de Empresas', 1, 'grado'),
('Psicología Clínica', 6, 'grado'),
('Derecho', 2, 'grado'),
('Licenciatura en Comunicación', 5, 'grado'),
('Maestría en Ingeniería de Software', 3, 'posgrado'),
('Maestría en Administración (MBA)', 1, 'posgrado'),
('Especialización en Neuropsicología', 6, 'posgrado');

-- PARTICIPANTE_PROGRAMA
INSERT INTO participante_programa_academico (ci_participante, id_programa, rol)
VALUES
('55910880', 1, 'alumno'),
('55667788', 5, 'alumno'),
('55788998', 4, 'alumno'),
('55938753', 6, 'alumno'),
('58902345', 7, 'alumno'),
('45676543', 3, 'docente'),
('57876550', 8, 'alumno'),
('57541231', 1, 'docente'),
('53234567', 2, 'docente'),
('55875921', 4, 'docente'),
('11111111', 1, 'admin');

-- EDIFICIOS
INSERT INTO edificio (nombre_edificio, direccion, departamento) VALUES
('Edificio San José', 'Av. 8 de Octubre 2733', 'Departamento de Medicina'),
('Edificio Semprún', 'Estero Bellaco 2771', 'Departamento de Economía y Negocios'),
('Edificio Mullin', 'Comandante Braga 2715', 'Departamento de Ingeniería'),
('Edificio San Ignacio', 'Cornelio Cantera 2733', 'Departamento de Ciencias Sociales'),
('Edificio Athanasius', 'Gral. Urquiza 2871', 'Departamento de Humanidades y Comunicación'),
('Edificio Madre Marta', 'Av. Garibaldi 2831', 'Departamento de Psicología'),
('Edificio Sacré Coeur', 'Av. 8 de Octubre 2738', 'Departamento de Derecho');

-- SALAS
INSERT INTO sala (nombre_sala, id_edificio, capacidad, tipo_sala) VALUES
('Aula Magna', 7, 200, 'libre'),
('Sala Zoom', 2, 50, 'posgrado'),
('Cowork de Ludus', 7, 35, 'docente'),
('Laboratorio', 3, 100, 'libre'),
('TI3', 7, 50, 'libre'),
('Sala del silencio', 4, 5, 'libre'),
('Sala de docentes', 1, 20, 'docente'),
('Sala de postgrados', 6, 40, 'posgrado'),
('Sala de grabación', 5, 40, 'libre');

-- TURNOS
INSERT INTO turno (hora_inicio, hora_fin) VALUES
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
('21:00:00', '22:00:00'),
('22:00:00', '23:00:00');

-- RESERVAS
INSERT INTO reserva (id_sala, fecha, id_turno, estado) VALUES
(1, '2025-10-28', 3, 'activa'),
(2, '2025-10-28', 4, 'finalizada'),
(4, '2025-10-29', 6, 'cancelada'),
(6, '2025-10-29', 8, 'activa'),
(8, '2025-10-30', 10, 'sin_asistencia'),
(5, '2025-11-21', 1, 'sin_asistencia'),
(5, '2025-11-21', 2, 'sin_asistencia');

-- RESERVA_PARTICIPANTE
INSERT INTO reserva_participante (ci_participante, id_reserva, fecha_solicitud_reserva, asistencia) VALUES
('55910880', 1, '2025-10-25 10:00:00', TRUE),
('55667788', 2, '2025-10-25 11:30:00', TRUE),
('55788998', 3, '2025-10-26 09:00:00', FALSE),
('55938753', 4, '2025-10-26 10:45:00', TRUE),
('58902345', 5, '2025-10-27 08:00:00', FALSE),
('55788998', 6, '2025-11-21 08:00:00', FALSE),
('55788998', 7, '2025-11-21 09:00:00', FALSE);

-- SANCIONES
INSERT INTO sancion_participante (ci_participante, fecha_inicio, fecha_fin) VALUES
('55788998', '2025-10-27', '2025-11-03'),
('58902345', '2025-10-30', '2025-11-06'),
('57876550', '2025-09-15', '2025-09-22'),
('57541231', '2025-10-10', '2025-10-17'),
('53234567', '2025-10-20', '2025-10-27'),
('55788998', '2025-11-21', '2026-01-21');

ALTER TABLE obligatorio.login CHANGE COLUMN contraseña contrasena VARCHAR(255);