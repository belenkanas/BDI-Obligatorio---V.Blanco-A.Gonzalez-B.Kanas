# BDI-Obligatorio — V. Blanco · A. González · B. Kanas  
**Trabajo Obligatorio - Segundo Semestre 2025 - Base de Datos I**  
**Docentes:** Prof. Juan Kosut | Sofía Guerrico  

---

## 📘 Sistema para la Gestión de Reserva de Salas de Estudio

El objetivo del trabajo obligatorio es diseñar e implementar un **sistema de información** para la gestión de las **salas de estudio** de la Universidad Católica del Uruguay (UCU).  
El sistema permite la **reserva**, **control de asistencia** y **generación de reportes**, apoyando la gestión académica y la toma de decisiones institucionales.

---

## 🏫 Descripción General

Las *Salas de Estudio* son espacios utilizados por estudiantes y docentes para diversas actividades:  
- Reuniones de grupo  
- Videoconferencias  
- Actividades académicas 

Actualmente, las reservas se registran manualmente en planillas de papel.  
El sistema propuesto busca **unificar y digitalizar** este proceso, facilitando el control, la trazabilidad y el uso equilibrado de las salas en todos los edificios de la universidad.

---

## 🕒 Reglas de Reserva

- Los turnos comienzan a las **08:00** y finalizan a las **23:00**.  
- Las reservas se realizan **por bloques de 1 hora**.  
  > Ejemplo: para reservar de 08:30 a 10:00, se deben solicitar los bloques 08:00–09:00 y 09:00–10:00.
- Las salas tienen una **capacidad máxima** que no puede ser excedida.  
- Cada reserva incluye los **participantes** (alumnos y/o docentes) que ocuparán la sala.  

---

## 👥 Tipos de Usuarios y Salas

### Usuarios
- **Estudiantes de grado**
- **Estudiantes de posgrado**
- **Docentes**

### Tipos de Salas
1. **Uso libre** → pueden reservarlas estudiantes de grado, posgrado y docentes.  
2. **Exclusivas de posgrado** → solo para estudiantes de posgrado y docentes.  
3. **Exclusivas de docentes** → uso restringido a docentes.

---

## ⏳ Restricciones de Uso

- Un **usuario no puede ocupar más de 2 horas diarias** en cualquiera de los edificios.  
- Un **usuario no puede tener más de 3 reservas activas por semana**.  
- **Docentes** y **estudiantes de posgrado** **no tienen estas limitaciones** cuando usan salas exclusivas para ellos.

---

## ✅ Control de Asistencia

- El sistema registrará la **asistencia de cada participante**.  
- Si **ningún participante asiste** en el día y horario de la reserva, los involucrados serán **notificados y sancionados**.  
- La sanción consiste en **2 meses sin poder realizar reservas**.

---

## 📊 Funcionalidades Principales

- Gestión de usuarios y tipos de salas  
- Creación, modificación y cancelación de reservas  
- Registro de asistencia por reserva  
- Control de restricciones y sanciones  

---

## 🛠️ Tecnologías Utilizadas

- **Lenguaje:** SQL / MySQL
- **Herramientas de Backend:** Python    

---

## 🧩 Entregables
 
- Script de creación de tablas  
- Script de inserción de datos de prueba  
- Consultas SQL (simulando reportes y casos de uso)  
- Instructivo completo para correr la aplicación de forma local 
- Documento con explicaciones y decisiones de diseño  

---

## 📅 Facultad de Ingeniería y Tecnologías  
**Universidad Católica del Uruguay — 2025**
