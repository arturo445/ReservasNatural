# Reserva Natural

Sistema de administración y monitoreo de reservas naturales desarrollado en SQL Server como proyecto académico para la gestión integral de biodiversidad, personal y visitantes.

---

## Descripción

Este proyecto permite administrar parques naturales, áreas protegidas, especies biológicas, visitantes y personal operativo mediante una base de datos relacional normalizada en **Tercera Forma Normal (3FN)**.

El sistema integra componentes de seguridad, monitoreo ambiental y automatización de procesos utilizando procedimientos almacenados, vistas, índices y triggers.

---

## Objetivos del Proyecto

- Gestionar reservas naturales y sus subdivisiones.
- Controlar el acceso de visitantes a los parques.
- Administrar personal de vigilancia, conservación y gestión.
- Monitorear especies y poblaciones biológicas.
- Implementar mecanismos de auditoría y validación automática.
- Aplicar optimización mediante índices y consultas avanzadas.

---

## Características Principales

### Gestión de Parques y Áreas
- Administración de parques naturales.
- División en áreas protegidas.
- Relación geográfica entre parques y zonas de conservación.

### Biodiversidad
- Registro taxonómico de especies.
- Asociación entre especies y áreas.
- Control de cantidades poblacionales.
- Índice optimizado por nombre científico.

### Gestión de Personal
- Personal de vigilancia.
- Personal de conservación.
- Personal administrativo.
- Asignación de vehículos y áreas.

### Gestión de Visitantes
- Registro automático de visitantes.
- Control de entradas por parque.
- Relación entre visitantes y personal administrativo.

### Seguridad e Integridad
- Triggers de validación biológica.
- Auditoría de modificaciones.
- Registro de actividades críticas.

### Consultas y Reportes
- Vistas multi-tabla.
- Reportes de vigilancia.
- Reportes poblacionales.
- Seguimiento de visitantes.

---

## Tecnologías Utilizadas

- **SQL Server**
- **Visual Paradigm**
- **Git & GitHub**
- **Python** (automatización y generación de datos)

---
## Componentes SQL Implementados

### Vistas

- `Vista_ReporteEntradas`
- `Vista_AsignacionVigilancia`
- `Vista_PoblacionEspecies`

### Procedimientos Almacenados

- Cálculo de ingresos por parque.

### Triggers

- Validación de cadena alimenticia.
- Auditoría de cambios de personal.
- Log de seguridad de entradas.

### Índices

- `idx_especie_cientifico`

---

## Modelo Relacional

El modelo relacional fue diseñado en Visual Paradigm siguiendo principios de normalización y consistencia referencial.

---

## Cómo Ejecutar el Proyecto

1. Crear la base de datos en SQL Server.
2. Ejecutar los scripts de creación de tablas.
3. Ejecutar inserts de datos.
4. Crear vistas, triggers y procedimientos almacenados.
5. Ejecutar consultas y pruebas.
---

## Autor

**Arturo Abella**
**Juldailis Cassares**
**DIego Rivera**

*Proyecto desarrollado para la asignatura de Bases de Datos - Universidad del Magdalena (2026).*
