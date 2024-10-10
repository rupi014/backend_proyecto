# Backend para API de Gestión

Este proyecto es el **backend** de una aplicación de gestión de usuarios, productos, staff, pedidos y blogs. Está desarrollado utilizando **FastAPI** y se conecta a una base de datos MySQL alojada en **Clever Cloud**. 

El proyecto incluye todas las rutas necesarias para gestionar los diferentes recursos y utiliza **dotenv** para manejar las variables de entorno de manera segura.

## Tecnologías Utilizadas

- **FastAPI**: Framework web moderno y rápido para construir APIs con Python.
- **MySQL**: Sistema de gestión de bases de datos relacional, donde se almacenan los datos de la aplicación.
- **Clever Cloud**: Plataforma utilizada para el alojamiento de la base de datos.
- **Python-dotenv**: Utilizado para cargar las variables de entorno desde un archivo `.env`.

## Funcionalidades

### Gestión de Recursos

El backend proporciona las siguientes rutas y funcionalidades para interactuar con la base de datos:

- **Usuarios**: Crear, editar, eliminar y obtener usuarios registrados.
- **Productos**: Gestión de productos, incluyendo su creación, edición, eliminación y consulta.
- **Staff**: Rutas para gestionar miembros del staff, con operaciones de creación, edición, y eliminación.
- **Pedidos**: Administración de pedidos, permitiendo su creación, actualización y eliminación.
- **Blogs**: Rutas para crear, editar, eliminar y consultar entradas de blogs.

### Variables de Entorno

Este proyecto utiliza **dotenv** para almacenar y cargar las variables de entorno necesarias para la configuración del entorno de producción y desarrollo. Asegúrate de crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

    ```bash
      DB_HOST=<host-de-la-base-de-datos>
      DB_USER=<usuario-de-la-base-de-datos>
      DB_PASSWORD=<contraseña-de-la-base-de-datos>
      DB_NAME=<nombre-de-la-base-de-datos>
      SECRET_KEY=<clave-secreta-para-jwt>

## Instalación

Para ejecutar el backend localmente, sigue los siguientes pasos: 

1. Clona el repositorio:
   ```bash
   git clone https://github.com/rupi014/backend_proyecto.git

2. Accede al directorio:
   ```bash
   cd backend_proyecto

3. Crea y configura el archivo .env como se describe anteriormente.
   
4. Instala las dependencias necesarias
   ```bash
   pip install -r requirements.txt

5. Ejecuta la aplicación
   ```bash
   uvicorn main:app --reload

6. El backend esta disponible en http://localhost:8000

## Documentación de la API

FastAPI genera automáticamente la documentación interactiva de la API, que se puede acceder en las siguientes rutas cuando la aplicación está en funcionamiento:

- Documentación Swagger: http://localhost:8000/docs
- Documentación Redoc: http://localhost:8000/redoc

La documentación en la aplicación ya desplegada es accesible en https://vikingsdb.up.railway.app/docs

## Contribuciones.

Si deseas contribuir a este proyecto, siéntete libre de enviar pull requests. Antes de realizar cambios importantes, abre un issue para discutir lo que te gustaría modificar.
