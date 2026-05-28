# Diccionario de Datos — ReservaNatural

## Descripción General

La base de datos **ReservaNatural** fue desarrollada en SQL Server con el objetivo de administrar parques naturales, biodiversidad, visitantes y personal operativo.

El modelo relacional se encuentra normalizado y utiliza:

- Llaves primarias y foráneas.
- Índices para optimización.
- Vistas.
- Triggers.
- Procedimientos almacenados.
- Cursores.

---

# Tablas del Sistema

## Tabla: Areas

| Campo          | Tipo de Dato  | Restricción  | Descripción                     |
| -------------- | ------------- | ------------ | ------------------------------- |
| Area\_ID       | INT           | PK, IDENTITY | Identificador único del área    |
| Nombre         | VARCHAR(255)  | NOT NULL     | Nombre del área protegida       |
| ExtensionTotal | DECIMAL(19,2) | NOT NULL     | Extensión total del área        |
| Parque\_ID     | INT           | FK           | Parque al que pertenece el área |

---

## Tabla: Areas\_Especies

| Campo              | Tipo de Dato | Restricción | Descripción                       |
| ------------------ | ------------ | ----------- | --------------------------------- |
| Area               | INT          | FK          | Área donde habita la especie      |
| Especie            | INT          | FK          | Identificador de la especie       |
| CantidadIndividuos | INT          | NOT NULL    | Cantidad registrada de individuos |

---

## Tabla: CadenasAlimenticias

| Campo      | Tipo de Dato | Restricción | Descripción         |
| ---------- | ------------ | ----------- | ------------------- |
| Depredador | INT          | FK          | Especie depredadora |
| Presa      | INT          | FK          | Especie presa       |

---

## Tabla: ComunidadesAutonomas

| Campo  | Tipo de Dato | Restricción  | Descripción                         |
| ------ | ------------ | ------------ | ----------------------------------- |
| CA\_ID | INT          | PK, IDENTITY | Identificador de comunidad autónoma |
| Nombre | VARCHAR(255) | NOT NULL     | Nombre de la comunidad autónoma     |

---

## Tabla: Entradas

| Campo          | Tipo de Dato  | Restricción       | Descripción                         |
| -------------- | ------------- | ----------------- | ----------------------------------- |
| NumeroEntrada  | INT           | PK, IDENTITY      | Identificador de entrada            |
| Fecha          | DATETIME      | DEFAULT GETDATE() | Fecha y hora de ingreso             |
| Parque\_ID     | INT           | FK                | Parque visitado                     |
| Visitante\_DNI | INT           | FK                | Visitante registrado                |
| Gestion\_DNI   | INT           | FK                | Empleado administrativo responsable |
| Precio         | DECIMAL(10,2) | NULL              | Valor de la entrada                 |

---

## Tabla: Especies

| Campo            | Tipo de Dato | Restricción  | Descripción                    |
| ---------------- | ------------ | ------------ | ------------------------------ |
| Especies\_ID     | INT          | PK, IDENTITY | Identificador único de especie |
| NombreVulgar     | VARCHAR(255) | NOT NULL     | Nombre común                   |
| NombreCientifico | VARCHAR(255) | INDEX        | Nombre científico              |
| TipoAnimal       | INT          | FK           | Tipo de clasificación animal   |

---

## Tabla: Especialidades

| Campo            | Tipo de Dato | Restricción  | Descripción                               |
| ---------------- | ------------ | ------------ | ----------------------------------------- |
| Especialidad\_ID | INT          | PK, IDENTITY | Identificador de especialidad             |
| Nombre           | VARCHAR(255) | NOT NULL     | Especialidad del personal de conservación |

---

## Tabla: PersonalConservacion

| Campo        | Tipo de Dato | Restricción | Descripción                         |
| ------------ | ------------ | ----------- | ----------------------------------- |
| Personal     | INT          | PK, FK      | Trabajador del área de conservación |
| Especialidad | INT          | FK          | Especialidad asignada               |

---

## Tabla: PersonalGestion

| Campo    | Tipo de Dato | Restricción | Descripción                 |
| -------- | ------------ | ----------- | --------------------------- |
| Personal | INT          | PK, FK      | Empleado administrativo     |
| CA\_ID   | INT          | FK          | Comunidad autónoma asignada |

---

## Tabla: PersonalParque

| Campo             | Tipo de Dato  | Restricción  | Descripción                  |
| ----------------- | ------------- | ------------ | ---------------------------- |
| DNI               | INT           | PK, IDENTITY | Identificador del trabajador |
| Nombre            | VARCHAR(255)  | NOT NULL     | Nombre completo              |
| CedulaProfesional | VARCHAR(255)  | NULL         | Documento profesional        |
| Area              | INT           | FK           | Área asignada                |
| Salario           | DECIMAL(10,2) | NOT NULL     | Salario del empleado         |

---

## Tabla: PersonalVigilancia

| Campo        | Tipo de Dato | Restricción | Descripción              |
| ------------ | ------------ | ----------- | ------------------------ |
| Personal     | INT          | PK, FK      | Trabajador de vigilancia |
| TipoVehiculo | INT          | FK          | Vehículo asignado        |
| Matricula    | VARCHAR(255) | NULL        | Matrícula del vehículo   |
| Area         | INT          | FK          | Área asignada            |

---

## Tabla: Parques

| Campo            | Tipo de Dato  | Restricción  | Descripción                  |
| ---------------- | ------------- | ------------ | ---------------------------- |
| Parque\_ID       | INT           | PK, IDENTITY | Identificador del parque     |
| Nombre           | VARCHAR(255)  | NOT NULL     | Nombre del parque natural    |
| FechaDeclaracion | DATE          | NOT NULL     | Fecha de declaración oficial |
| Extension        | DECIMAL(19,2) | NOT NULL     | Extensión territorial        |
| Provincias\_ID   | INT           | FK           | Provincia asociada                    |
| PrecioEntrada    | DECIMAL(10,2) | NOT NULL     | Precio actual de la entrada del parque|
---

## Tabla: Provincias

| Campo         | Tipo de Dato | Restricción  | Descripción                    |
| ------------- | ------------ | ------------ | ------------------------------ |
| Provincia\_ID | INT          | PK, IDENTITY | Identificador provincial       |
| Nombre        | VARCHAR(255) | NOT NULL     | Nombre de la provincia         |
| CA\_ID        | INT          | FK           | Comunidad autónoma relacionada |

---

## Tabla: Telefonos

| Campo         | Tipo de Dato | Restricción | Descripción                |
| ------------- | ------------ | ----------- | -------------------------- |
| ParqueDNI     | INT          | FK          | Trabajador asociado        |
| telefono      | VARCHAR(255) | NOT NULL    | Número o código telefónico |
| TipoTelefonos | INT          | FK          | Tipo de comunicación       |

---

## Tabla: TipoAnimal

| Campo          | Tipo de Dato | Restricción  | Descripción                   |
| -------------- | ------------ | ------------ | ----------------------------- |
| TipoAnimal\_ID | INT          | PK, IDENTITY | Identificador del tipo animal |
| Descripcion    | VARCHAR(255) | NOT NULL     | Clasificación biológica       |

---

## Tabla: TipoTelefonos

| Campo             | Tipo de Dato | Restricción  | Descripción                        |
| ----------------- | ------------ | ------------ | ---------------------------------- |
| TipoTelefonos\_ID | INT          | PK, IDENTITY | Identificador del tipo telefónico  |
| Descripcion       | VARCHAR(255) | NOT NULL     | Tipo de dispositivo o comunicación |

---

## Tabla: TipoVehiculo

| Campo            | Tipo de Dato | Restricción  | Descripción                    |
| ---------------- | ------------ | ------------ | ------------------------------ |
| TipoVehiculo\_ID | INT          | PK, IDENTITY | Identificador del vehículo     |
| Descripcion      | VARCHAR(255) | NOT NULL     | Tipo de vehículo de vigilancia |

---

## Tabla: Visitantes

| Campo  | Tipo de Dato | Restricción  | Descripción                 |
| ------ | ------------ | ------------ | --------------------------- |
| DNI    | INT          | PK, IDENTITY | Identificador del visitante |
| Nombre | VARCHAR(255) | NOT NULL     | Nombre del visitante        |

---

# Objetos Adicionales

## Vistas

### Vista\_ReporteEntradas

Permite visualizar el historial de entradas de visitantes a los parques naturales, relacionando visitantes, parques y personal administrativo encargado del registro.

### Vista\_AsignacionVigilancia

Muestra la asignación de personal de vigilancia junto con el vehículo utilizado, el área protegida y el parque natural correspondiente.

### Vista\_PoblacionEspecies

Presenta información consolidada sobre especies registradas en cada área protegida, incluyendo cantidad de individuos y clasificación biológica.

## Triggers

### Trigger de Validación de Cadena Alimenticia

Verifica que una especie no pueda registrarse como depredadora y presa de sí misma, garantizando coherencia biológica.

### Trigger de Auditoría de Personal

Registra automáticamente cambios realizados sobre la información del personal del parque para fines de control y seguimiento.

### Trigger de Seguridad de Entradas

Genera un registro automático de las operaciones relacionadas con entradas de visitantes para auditoría y trazabilidad.

## Procedimientos Almacenados

### Procedimiento de Ingresos por Parque

**Nombre SQL:** `GenerarIngresosPorParque`

Calcula los ingresos generados por cada parque natural a partir de las entradas registradas.

```sql
EXEC GenerarIngresosPorParque;
```



## Índices

- idx\_especie\_cientifico

---

# Autores

**Arturo Abella**

**Juldailis Cassares**

**Diego Rivera**\
Universidad del Magdalena\
Bases de Datos — 2026

