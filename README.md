# Prueba técnica, César Silva

## Requisitos para correr el proyecto
Los requisitos con su respectiva versión se encuentran en el archivo requirements.txt del proyecto.

## Pasos para levantarlo en local
Clonar el presente repositorio.

El proyecto cuenta con un archivo `docker-compose` para levantar el backend y la base de datos, usando Python3.11 y Django 5. Sin embargo, es necesario configurar primeramente las variables de entorno. Para ello, está un archivo `.env.example` que debe ser transformado a su contraparte `.env`. Basta con correr el comando de copia para hacer el renombramiento:
```
make env
```
Seguidamente, se debe levantar el contenedor. Esto ya levanta la aplicación, configura la base de datos, y corre migraciones:
```
make run
```
Es necesario crear un superuser de Django para inciar sesión en el panel de admin. Para ello, se puede usar el comando correspondiente:
```
make superuser
```
Después de crear un usuario y contraseña, ya podemos abrir la aplicación. La misma se encuentra arriba en localhost, en el puerto 8000. 

Primeramente, iniciar sesión en el admin: http://localhost:8000/admin/.

Luego, se puede entrar a la interfaz por defecto de Django REST Framework a través de la ruta `/api`. Esta muestra los tres servicios disponibles: bancos, clientes y creditos.

## Explicación de la solución
Se nos presenta el contexto de la empresa Tu Crédito, que requiere un sistema web basado en Django.
A continuación se presenta la implementación desde el Backend del mismo.

----

### Para la base del proyecto:

Primeramente, es necesario tener Python (3.11.9) y pip (26.0.1) instalados en el sistema.
Además, se instala con pip la versión deseada de Django (5).
Asimismo, tener Postgresql instalado. El proyecto se desarrolló usando pgAdmin4 como manejador de BD.

Se crea un virtual environment con estas versiones corriendo, en el directorio deseado,
```
virtualenv -p python3.11 venv
```

Activar el venv.
Luego se crea el proyecto, el usuario de PSQL, librerías necesarias para PSQL, y finalmente la app `"core"`:
```
django-admin startproject tu_credito
createuser -s postgres
psql -U postgres
pip install psycopg2-binary
py manage.py startapp core
```
Se crean los modelos dentro de `tu_credito/core/models.py.`
Se agrega `core` dentro de los installed apps del `settings.py`.
Se cambian los valores de database de `settings.py` para conectar con psql.
Se agrega el `requirements.txt` con las versiones de Django y `psycopg2-binary`.
Crear la base de datos en el pgAdmin, el nombre debe coincidir con el valor en `settings.py`.
Luego, para aplicar los cambios a nivel de base de datos, se corren migraciones de Django:
```
python manage.py makemigrations
python manage.py migrate
```
Agregar las tablas al `admin.py` para que se puedan visualizar en su respectivo admin.
Crear el usuario para el admin y correr el servidor.
```
python manage.py createsuperuser
python manage.py runserver
```
Esto logra la base deseada.

Adicionalmente, se instala `python-decouple` para el manejo de variables de entorno en settings.py, de forma que vivan en un archivo `.env`. Acá se crea también el archivo `.gitignore` para evitar que se suba al repositorio.


-----------
### Para la API REST:
Se instala primeramente DRF, para después agregarlo a las `INSTALLED_APPS` de las settings de Django y al `requirements.txt`:
```
pip install djangorestframework
```

Acá comienzo primero creando los serializers. Creo el archivo `serializers.py` dentro del directorio `tu_credito/core/api` (agrego de una vez el archivo init).
Agrego los serializers de los tres modelos.
Creo las vistas (el file `views.py`) dentro de este mismo directorio `tu_credito/core/api` (estas vistas cuentan con los fields `queryset`, `serializer_class`, `search_fields`, `ordering_fields` y `ordering`).
Creo el archivo `urls.py` dentro del directorio `tu_credito/core/api`.
Modifico el archivo `urls.py` de la base del proyecto para que reconozca las urls que viven dentro de `tu_credito/core/api`.

Es en este punto donde se prueban los endpoints.

-----
### Para el resto de requerimientos
Cada vez que se instala alguna dependencia nueva, se agrega a las `INSTALLED_APPS` y al `requirements.txt`. Si aplica, se agregan las configuraciones.

#### Filtros:
Se usa `django-filter`. Implemento los filtros de los tres modelos agregando el archivo `filters.py` dentro de `tu_credito/core/api`.

Modifico el `views.py` para agregar los valores de `filterset_class` a las tres views.
Agrego la variable `REST_FRAMEWORK` al `settings.py`, y le agrego el valor `DEFAULT_FILTER_BACKENDS` con las variables correspondientes para el backend de filters, y el soporte tanto de search como ordering.

#### Paginación:
Para la paginación, agrego a la variable `REST_FRAMEWORK` de `settings.py` los valores de `DEFAULT_PAGINATION_CLASS` y `PAGE_SIZE` para que afecte a todas las vistas.

#### Documentación:
Se usa `drf-spectacular` para la documentación. Para ello, agrego la variable `DEFAULT_SCHEMA_CLASS` en la variable `REST_FRAMEWORK` del `settings.py`.
Agrego la variable `SPECTACULAR_SETTINGS` en `settings.py` tal como menciona la documentación de Spectacular.
Dentro del `urls.py` de la base del proyecto, agrego las dos rutas (`'api/schema/'` y `'api/docs/'`) al urlpatterns, luego de importar `SpectacularAPIView` y `SpectacularSwaggerView`.

#### Content Security Policy:
Para implementar CSP se usa `django-csp`. Se agrega el middleware correspondiente a su valor en `settings.py` como indica la documentación. Finalmente, agrego los valores de `CONTENT_SECURITY_POLICY` y `CONTENT_SECURITY_POLICY_REPORT_ONLY`.

#### Permissions Policy:
Para configurar el Permissions Policy (antes Feature Policy) en Django, se usa la librería `django-permissions-policy`. Agregamos el Middleware correspondiente y la configuración en el `settings.py` de nuestro proyecto. Por defecto, dejamos todos los valores en blanco ya que no necesitamos acceder a ninguno de los permisos.

Adicionalmente, agregamos `IsAuthenticated` como clase por defecto de la permisología de cada view configurando la variable `DEFAULT_PERMISSION_CLASSES` en el valor de `REST_FRAMEWORK` de nuestro `settings.py`.

#### JWT:
Se usa `djangorestframework-simplejwt` para implementar auth con JWT. Para ello, configuramos dentro de `REST_FRAMEWORK` la variable `DEFAULT_AUTHENTICATION_CLASSES` para que soporte `JWTAuthentication` y `SessionAuthentication`. Luego, agregamos settings básicas de JWT.

#### Unit tests:
Para las pruebas unitarias, se usa `pytest` y `pytest-django`. Se debe configurar el archivo `pytest.ini` en la base del proyecto, y se crea un directorio `/tests` dentro de la app. Se crean los fixtures dentro de este directorio en un archivo `conftest.py`, y finalmente se crean los archivos `test_main.py` y `api/test_api.py`. Para correr los tests, es suficiente con correr el comando (en su versión verbose):
```
python -m pytest -v
```

## Uso de IA
Para la realización del test, se usaron Claude y Gemini en distintos puntos. 

Primeramente, se usó Claude para la creación de los modelos, vistas, modeladmins, serializers y filters: esto ya que con sólo promptear el contexto de la aplicación se puede generar un grueso importante de la misma. De todas formas, todos estos fueron debidamente testeados, revisados y reescritos para cubrir detalles faltantes o deseables. Adicionalmente, las pruebas unitarias también se generaron usando Claude, para después ser probadas, adaptadas y reescritas consecuentemente; esto ya que una tarea larga como la escritura de pruebas unitarias puede ser tratada a través de estas herramientas logrando ahorrar una cantidad importante de tiempo y esfuerzo.

Mientras tanto, se usó Gemini para dudas puntuales a la hora del desarrollo. Entre las dudas se encuentran el uso de is not None en condicionales, la autenticación usando forceauthenticate para el `APIClient()` de los tests, los valores necesarios para el archivo `.gitignore`, y arreglos a ciertas pruebas unitarias que dependían de `fecha_registro`. Como desarrolladores, es muy común conseguirnos problemas y obstáculos, y usar LLMs es un buen punto de partida para resolverlos. De todas formas, toda la información y código resultante debe ser también consultado junto con documentación (de estar disponible) y recursos en internet que estén relacionados. Al final, es nuestro criterio el que toma la última decisión.

Finalmente, los archivos `docker-compose.yml` y `Dockerfile` fueron generados también con Claude a partir del contexto de la aplicación. Estos files fueron debidamente testeados y modificados acorde a lo necesario para que funcionen correctamente.

## Otros
El presente proyecto fue realizado por César Silva (CesarBeats en Github).
