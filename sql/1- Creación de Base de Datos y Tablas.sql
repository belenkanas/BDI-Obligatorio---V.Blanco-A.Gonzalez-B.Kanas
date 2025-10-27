DROP DATABASE IF EXISTS `obligatorio`;
CREATE DATABASE `obligatorio` DEFAULT CHARACTER SET utf8 COLLATE utf8_spanish_ci;

use obligatorio;

CREATE TABLE login(
  correo VARCHAR(255) UNIQUE NOT NULL,
  contraseña VARCHAR(255) NOT NULL,
  PRIMARY KEY (correo)
);

CREATE TABLE participante(
  ci VARCHAR(8) NOT NULL,
  nombre VARCHAR(50) NOT NULL,
  apellido VARCHAR(50) NOT NULL,
  email VARCHAR(255) NOT NULL,
  PRIMARY KEY (ci)
);


CREATE TABLE facultad(
    id_facultad INT NOT NULL,
    nombre VARCHAR(255) NOT NULL,
    PRIMARY KEY (id_facultad)
);

CREATE TABLE programa_academico(
  nombre_programa VARCHAR(50) NOT NULL,
  id_facultad INT NOT NULL,
  tipo ENUM('grado', 'postgrado') NOT NULL,
  PRIMARY KEY (nombre_programa),
  FOREIGN KEY (id_facultad) REFERENCES facultad(id_facultad)
);

CREATE TABLE participante_programa_academico(
  id_alumno_programa INT NOT NULL,
  ci_participante VARCHAR(8) NOT NULL,
  nombre_programa VARCHAR(100) NOT NULL,
  rol ENUM('alumno', 'docente') NOT NULL,
  PRIMARY KEY (id_alumno_programa),
  FOREIGN KEY (ci_participante) REFERENCES participante(ci),
  FOREIGN KEY (nombre_programa) REFERENCES programa_academico(nombre_programa)
);

CREATE TABLE edificio(
    nombre_edificio VARCHAR(255) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    departamento VARCHAR(255),
    PRIMARY KEY (nombre_edificio)
);


CREATE TABLE sala(
    nombre_sala VARCHAR(255) NOT NULL,
    edificio VARCHAR(255) NOT NULL,
    capacidad INT NOT NULL,
    tipo_sala ENUM('libre', 'postgrado', 'docente') NOT NULL,
    PRIMARY KEY (nombre_sala, edificio),
    FOREIGN KEY (edificio) REFERENCES edificio(nombre_edificio)
);


CREATE TABLE turno(
  id_turno INT NOT NULL,
  hora_inicio TIME NOT NULL,
  hora_fin TIME NOT NULL,
  PRIMARY KEY (id_turno)
);

CREATE TABLE reserva(
  id_reserva INT NOT NULL,
  nombre_sala VARCHAR(255) NOT NULL,
  edificio VARCHAR(255) NOT NULL,
  fecha DATETIME NOT NULL,
  id_turno INT NOT NULL,
  estado ENUM('activa', 'cancelada', 'sin asistencia', 'finalizada') NOT NULL,
  PRIMARY KEY (id_reserva),
  FOREIGN KEY (nombre_sala, edificio) REFERENCES sala(nombre_sala, edificio),
  FOREIGN KEY (id_turno) REFERENCES turno(id_turno)
);

CREATE TABLE reserva_participante(
    ci_participante VARCHAR(8) NOT NULL,
    id_reserva INT NOT NULL,
    fecha_solicitud_reserva DATETIME NOT NULL,
    asistencia BOOLEAN,
    PRIMARY KEY (ci_participante, id_reserva),
    FOREIGN KEY (ci_participante) REFERENCES participante(ci),
    FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva)
);

CREATE TABLE sancion_participante(
    ci_participante VARCHAR(8) NOT NULL,
    fecha_inicio DATETIME NOT NULL,
    fecha_fin DATETIME NOT NULL,
    PRIMARY KEY (ci_participante, fecha_inicio, fecha_fin),
    FOREIGN KEY (ci_participante) REFERENCES participante(ci)
);