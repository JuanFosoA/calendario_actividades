# API Visualizador de horario

Este proyecto es una API REST para visualizar las horas de actividades de estudiantes. La API proporciona endpoints para crear, leer, actualizar y eliminar (CRUD) registros, con ciertas operaciones restringidas solo a administradores.

## Tabla de Contenidos

- [Instalación](#instalación)
- [Uso](#uso)
- [Endpoints de la API](#endpoints-de-la-api)
  - [Endpoints de Estudiantes](#endpoints-de-estudiantes)
  - [Endpoints de Profesores](#endpoints-de-profesores)
  - [Endpoints de Cursos](#endpoints-de-cursos)
- [Restricciones de Administrador](#restricciones-de-administrador)

## Instalación

1. Clona el repositorio:
    ```sh
    git clone https://github.com/JuanFosoA/calendario_actividades.git
    ```

2. Navega al directorio del proyecto:
    ```sh
    cd calendario_actividades
    ```

3. Instala las dependencias:
    ```sh
    pip install -r requirements.txt
    ```

4. Ejecuta la aplicación:
    ```sh
    uvicorn main:app --reload
    ```

## Uso

La API proporciona los siguientes endpoints para gestionar estudiantes, profesores y cursos. Ten en cuenta que algunas operaciones están restringidas solo a administradores.

## Endpoints de la API

### Endpoints de Estudiantes

- **Obtener Todos los Estudiantes**
    - `GET /api/v1/student`
    - Respuesta: Lista de todos los estudiantes
    - **Solo Administrador**

- **Obtener un Estudiante por ID**
    - `GET /api/v1/student/{id}`
    - Parámetros:
        - `id` (entero): El ID del estudiante
    - Respuesta: Detalles del estudiante con el ID especificado
    - **Solo Administrador**

- **Actualizar un Estudiante**
    - `PUT /api/v1/student/{id}`
    - Parámetros:
        - `id` (entero): El ID del estudiante
    - Cuerpo de la Solicitud: Objeto JSON con los detalles actualizados del estudiante
    - Respuesta: Detalles actualizados del estudiante
    - **Solo Administrador**

- **Eliminar un Estudiante**
    - `DELETE /api/v1/student/{id}`
    - Parámetros:
        - `id` (entero): El ID del estudiante
    - Respuesta: Confirmación de la eliminación del estudiante
    - **Solo Administrador**

### Endpoints de Profesores

- **Obtener Todos los Profesores**
    - `GET /api/v1/teacher`
    - Respuesta: Lista de todos los profesores
    - **Solo Administrador**

- **Obtener un Profesor por ID**
    - `GET /api/v1/teacher/{id}`
    - Parámetros:
        - `id` (entero): El ID del profesor
    - Respuesta: Detalles del profesor con el ID especificado
    - **Solo Administrador**

- **Actualizar un Profesor**
    - `PUT /api/v1/teacher/{id}`
    - Parámetros:
        - `id` (entero): El ID del profesor
    - Cuerpo de la Solicitud: Objeto JSON con los detalles actualizados del profesor
    - Respuesta: Detalles actualizados del profesor
    - **Solo Administrador**

- **Eliminar un Profesor**
    - `DELETE /api/v1/teacher/{id}`
    - Parámetros:
        - `id` (entero): El ID del profesor
    - Respuesta: Confirmación de la eliminación del profesor
    - **Solo Administrador**

### Endpoints de Cursos

- **Obtener Todos los Cursos**
    - `GET /api/v1/course`
    - Respuesta: Lista de todos los cursos

- **Obtener un Curso por ID**
    - `GET /api/v1/course/{id}`
    - Parámetros:
        - `id` (entero): El ID del curso
    - Respuesta: Detalles del curso con el ID especificado

- **Actualizar un Curso**
    - `PUT /api/v1/course/{id}`
    - Parámetros:
        - `id` (entero): El ID del curso
    - Cuerpo de la Solicitud: Objeto JSON con los detalles actualizados del curso
    - Respuesta: Detalles actualizados del curso
    - **Solo Administrador**

- **Eliminar un Curso**
    - `DELETE /api/v1/course/{id}`
    - Parámetros:
        - `id` (entero): El ID del curso
    - Respuesta: Confirmación de la eliminación del curso
    - **Solo Administrador**

## Restricciones de Administrador

Para acceder a estos endpoints, debes estar autenticado como administrador. Los mecanismos de autenticación y autorización deben estar implementados en la API para hacer cumplir estas restricciones.

