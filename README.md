# Reserva Natural 🌿

Proyecto académico desarrollado en SQL Server para la administración integral de reservas naturales y biodiversidad.

## 📝 Descripción
Este sistema permite la gestión automatizada de parques naturales, controlando desde la logística del personal y la seguridad, hasta el monitoreo de especies y el registro de visitantes. El diseño sigue un enfoque sistémico y está normalizado en **Tercera Forma Normal (3FN)**.

## ✨ Características
*   **Gestión de Parques y Áreas:** Administración de subdivisiones geográficas protegidas.
*   **Biodiversidad:** Registro taxonómico con optimización de búsqueda por nombre científico.
*   **Control de Personal:** Gestión especializada de vigilancia (con asignación de vehículos), conservación y administración.
*   **Seguridad e Integridad:** Implementación de triggers para validación biológica y auditoría de cambios.
*   **Reportes Avanzados:** Vistas multi-tabla para análisis de población y flujos de visitantes.

## 🛠️ Tecnologías
*   **Motor de Base de Datos:** SQL Server
*   **Modelado:** Visual Paradigm
*   **Control de Versiones:** Git & GitHub
*   **Automatización:** Python (Capa de aplicación)

## 📂 Estructura del Proyecto SQL
*   **Vistas:** 
    *   `Vista_ReporteEntradas` (4 tablas)
    *   `Vista_AsignacionVigilancia` (5 tablas)
    *   `Vista_PoblacionEspecies` (3 tablas + Índice)
*   **Triggers:**
    *   Validación de Cadena Alimenticia (Inserción)
    *   Auditoría de Personal (Actualización)
    *   Log de Seguridad de Entradas (Seguimiento)
*   **Índices:** `idx_especie_cientifico` para alto rendimiento.

## 👥 Autores
*   **Arturo Abella**

---
*Proyecto desarrollado para la asignatura de Bases de Datos - Universidad del Magdalena (2026).*
