# jhon_esteban-sport_x_inlazz

------
### Instalar dependencias y e iniciar el proyecto (Windows)

```
    # Crear un entorno virtual de python
    >>> python -m venv <nombre_entorno>

    # Activar el entorno (estar a la altura de la carpeta creada)
    >>> .\<nombre_entorno>\Scripts\activate (Windows)

    # A la altura del archivo requirements.txt del proyecto
    >>> pip install -r requirements.txt

    # Iniciar las migraciones a la base de datos
    >>> python manage.py makemigrations
    >>> python manage.py migrate

    # Crear superusuario
    >>> python manage.py createsuperuser

    # A la altura del archivo manage.py, iniciamos el servidor
    >>> python manage.py runserver
```
------

*Cada ruta tiene definidos sus códigos de estado para cada petición y valor retornado*

Tipos para el envío para el campo type_dni:         
- CC: cedula ciudadania
- TI: targeta de identidad
- CE: cedula de extranjeria

Tipos para el envio de campo ticket_type:
- DP: derecho de peticion
- FL: felicitacion
- PT: peticion
- QJ: queja
- RC: reclamo
- SG: sugerencia

## Rutas de aplicación PQRS

- (POST) Crear una PQR: http://127.0.0.1:8000/api/create-pqrs/
```
Envio de datos:
    {
        "dni": 000000,
        "type_dni": "CE",
        "name": "John",
        "lastname": "Doe",
        "email": "john@mail.com",
        "phone": 6040000000,
        "movil_phone": "+57 0000000001",
        "ticket_type": "SG",
        "title": "Prueba",
        "description": "Contenido de prueba"
    }

Obtienes una respuesta, de ser correcta, así:

    {
        "message_success": "PQR´s cargado correctamente."
    }

En caso de que algún dato sea inválido devolvera los campos y se verá algo así:

    {
        "movil_phone": [
            "Número no válido, debe ser: +indicativo número, ejmp: +57 3002001000"
        ],
        "dni": [
            "Número de documento no válido no válido."
        ]
    }
```

- (GET) listar todos: http://127.0.0.1:8000/api/list-pqrs/
- (GET) listar uno en detalle: http://127.0.0.1:8000/api/detail-pqrs/1/
- (GET) obtener para editar: http://127.0.0.1:8000/api/update-pqrs/1/
- (PUT) editar un PQRS: http://127.0.0.1:8000/api/update-pqrs/1/
```
Envio de datos:
    {
        "dni": 000000000,
        "type_dni": "CC",
        "name": "John",
        "lastname": "Doe",
        "email": "john@mail.com",
        "phone": 6040000000,
        "movil_phone": "+00 0000000000",
        "ticket_type": "RC",
        "title": "Prueba",
        "description": "Contenido de prueba editado"
    }

Obtienes una respuesta, de ser correcta, así:

    {
        "message_success": "PQR editado correctamente"
    }

En caso de que algún dato sea inválido devolvera los campos y se verá algo así:

    {
        "phone": [
            "Número no válido, debe ser: indicativo_ciudad número, ejmp: 6040000000"
        ],
        "dni": [
            "Número de documento no válido no válido."
        ]
    }

```

- (DELETE) eliminar: http://127.0.0.1:8000/api/delete-pqrs/1/
```
En caso de eliminar correctamente:

    {
        "message_success": "PQR eliminado correctamente"
    }

En caso no pueda eliminar:
    {
        "message_error": "PQR no encontrado"
    }
```

*Eliminar varios registros a la vez*
- (GET) eliminar (ver los PQRS disponibles para ser eliminados): http://127.0.0.1:8000/api/delete-severals-pqrs/
```
Obtiene los ids y nombre de los PQR's
    [
        {
            "id": 1,
            "title": "Prueba"
        },
        ...
    ]

En caso de no en contrar PQR´s envía el mensaje:
    {
        "message_info": "No hay PQR's disponibles para borrar"
    }
```

- (DELETE) eliminar: http://127.0.0.1:8000/api/delete-severals-pqrs/
```
Envio de datos:
    [
        {"id": 11},
        {"id": 12}
    ]

Mensaje obtenido en caso ser correcto:
    {
        "message_success": "PQR´s eliminados correctamente."
    }

En caso contrario:
    {
        "message_error": "Ha ocurrido un error por... Alguno de los/el id's pasados no existe."
    }
```