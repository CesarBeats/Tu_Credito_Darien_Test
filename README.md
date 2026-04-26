# Prueba técnica, César Silva

## Requisitos para correr el proyecto
Los requisitos con su respectiva versión se encuentran en el archivo requirements.txt del proyecto.

## Pasos para levantarlo en local
Clonar el presente repositorio.

Correr make requirements dentro del entorno virtual con la version 3.11 de Python.

## Breve explicación de la solución
Se nos presenta el contexto de la empresa Tu Crédito, que requiere un sistema web basado en Django.
A continuación se presenta la implementación desde el Backend del mismo.

Primeramente, es necesario tener Python (3.11.9) y pip (26.0.1) instalados en el sistema.
Además, se instala con pip la versión deseada de Django (5).
Asimismo, tener Postgresql 18 instalado. El proyecto se desarrolló usando pgAdmin4 como manejador de BD.

Se crea un virtual environment con estas versiones corriendo, en el directorio deseado,
```
virtualenv -p python3.11 venv
```

Activar el venv.
Luego se crea el proyecto, el usuario de PSQL, librerías necesarias para PSQL, y finalmente la app "core":
```
django-admin startproject tu_credito
createuser -s postgres
psql -U postgres
pip install psycopg2
py manage.py startapp core
```
Se crean los modelos dentro de tu_credito/core/models.py.
Se agrega core dentro de los installed apps del settings.py.
Se cambian los valores de database de settings.py para conectar con psql.
Se agrega el requirements.txt con las versiones de Django y psycopg2.
Crear la base de datos en el pgAdmin, el nombre debe coincidir con el valor en settings.py.
Luego correr
```
python manage.py makemigrations
python manage.py migrate
```
Agregar las tablas al admin.py.
Crear el usuario para el admin y correr el servidor.
```
python manage.py createsuperuser
python manage.py runserver
```
Esto logra la base deseada.
Se instaló python-decouple para el manejo de variables de entorno en settings.py. Se agrega al requirements.txt
```
pip install python-decouple
```
Se hace el cambio de valores hardcoded al uso de un .env file con estos valores modificando el settings.py.
Se agrega el archivo .gitignore para evitar que el .env se suba al repositorio.

Ahora comienza la API REST básica. Instalamos DRF:
```
pip install djangorestframework
```
Y se agrega al requirements.txt.
Acá comienzo primero creando los serializers. Creo el archivo serializers.py dentro del directorio tu_credito/core/api (agrego de una vez el archivo init).
Agrego los serializers de los tres modelos.
Creo las vistas (el file views.py) dentro de este mismo directorio tu_credito/core/api (estas vistas cuentan con los fields queryset, serializer_class, search_fields, ordering_fields y ordering)
Creo el archivo urls.py dentro del directorio tu_credito/core/api.
Modifico el archivo urls.py de la base del proyecto para que reconozca las urls que viven dentro de tu_credito/core/api.
Prueba de endpoints exitosa.
Implemento los filtros de los tres modelos agregando el archivo filters.py dentro de tu_credito/core/api.
Instalo django-filters y lo agrego al requirements.txt:
```
pip install django-filter
```
Agrego rest_framework a las installed_apps.
Modifico el views.py para agregar los valores de filterset_class a las tres views.
Agrego la variable REST_FRAMEWORK al settings.py, y le agrego el valor DEFAULT_FILTER_BACKENDS con las variables correspondientes para el backend de filters, y el soporte tanto de search como ordering.

Para la paginación, agrego a la variable REST_FRAMEWORK de settings.py los valores de DEFAULT_PAGINATION_CLASS y PAGE_SIZE para que afecte a todas las vistas.

Para la documentación, es necesario instalar drf-spectacular con el comando
```
pip install django-filter
```
Se agrega a los requirements.txt
Agrego drf_spectacular a las installed apps del settings.py.
Agrego la variable DEFAULT_SCHEMA_CLASS en la variable REST_FRAMEWORK del settings.py.
Agrego la variable SPECTACULAR_SETTINGS en settings.py tal como menciona la documentación de Spectacular.
Dentro del urls.py de la base del proyecto, agrego las dos rutas ('api/schema/' y 'api/docs/') al urlpatterns, luego de importar SpectacularAPIView y SpectacularSwaggerView.

Para implementar CSP instalo el paquete y lo agrego a los requirements y a las installed apps.
```
pip install django-csp
```
Agrego el django-csp middleware como indica la documentación en el settings.
Agrego los valores de CONTENT_SECURITY_POLICY y CONTENT_SECURITY_POLICY_REPORT_ONLY como indica la documentación en el archivo settings.py.

Para configurar el Permissions Policy (antes Feature Policy) en Django, vamos a instalar la librería, agregarla al requirements y al installed apps.
``` 
pip install django-permissions-policy
```
Finalmente, agregamos el Middleware y la configuración en el settings.py de nuestro proyecto. Por defecto, dejamos todos los valores en blanco ya que no necesitamos acceder a ninguno de los permisos.

Adicionalmente, agregamos IsAuthenticated como clase por defecto de la permisología de cada view configurando la variable DEFAULT_PERMISSION_CLASSES en el valor de REST_FRAMEWORK de nuestro settings.py.

Para implementar autenticación con JWT, instalamos la librería de djangorestframework-simplejwt, e igual agregamos a installed apps y a nuestro requirements.txt.
``` 
pip install djangorestframework-simplejwt
```
Configuramos dentro de REST_FRAMEWORK la variable DEFAULT_AUTHENTICATION_CLASSES para que soporte JWTAuthentication y SessionAuthentication. Luego Agregamos settings básicas de JWT.

Para las pruebas unitarias, instalamos pytest.
pytest-9.0.3
## Uso de IA
Se usó Claude.
