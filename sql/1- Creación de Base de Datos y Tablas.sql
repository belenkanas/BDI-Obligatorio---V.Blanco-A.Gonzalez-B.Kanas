DROP DATABASE IF EXISTS `obligatorio`;
CREATE DATABASE `obligatorio` DEFAULT CHARACTER SET utf8 COLLATE utf8_spanish_ci;

use obligatorio;

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
  rol ENUM('alumno', 'docente') NOT NULL,
  PRIMARY KEY (id_alumno_programa),
  FOREIGN KEY (ci_participante) REFERENCES participante(ci),
  FOREIGN KEY (id_programa) REFERENCES programa_academico(id_programa)
);

CREATE TABLE edificio(
    id_edificio INT AUTO_INCREMENT,
    nombre_edificio VARCHAR(255) UNIQUE NOT NULL,
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
  fecha DATE NOT NULL, #El turno ya está indicado en su respectiva tabla
  id_turno INT NOT NULL,
  estado ENUM('activa', 'cancelada', 'sin_asistencia', 'finalizada') NOT NULL,
  PRIMARY KEY (id_reserva),
  FOREIGN KEY (id_sala) REFERENCES sala(id_sala),
  FOREIGN KEY (id_turno) REFERENCES turno(id_turno)
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