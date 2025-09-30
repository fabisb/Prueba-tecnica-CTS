# CTS Turismo – Prueba Técnica

Aplicación Full Stack para gestionar un sorteo de San Valentín. El premio es una estadía de 2 noches todo pagado para una pareja en un hotel. La aplicación permite registrar participantes, verificar correos, activar cuentas y seleccionar al azar un ganador, enviando notificaciones automáticamente.

## Tecnologías

- Backend: Python 3.x, Django 5.2, Django REST Framework
- Tareas asíncronas: Celery + Redis
- Frontend: Vue.js
- Base de datos: SQLite (desarrollo)
- Correo electrónico: Gmail SMTP (con App Password)

## Instalación y ejecución

1. Clonar repositorio
git clone <https://github.com/fabisb/Prueba-tecnica-CTS>
cd Prueba-tecnica-CTS

2. Crear entorno virtual
python -m venv .venv
source .venv/bin/activate # Linux/macOS
.venv\Scripts\activate # Windows
pip install -r requirements.txt

3. Configurar variables de entorno en `.env` o `settings.py`
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password
FRONTEND_URL=http://localhost:5173

4. Levantar Redis (Docker)
docker run -d --name redis -p 6379:6379 redis:7

5. Migrar base de datos
python manage.py migrate

6. Ejecutar aplicación
- Django: `python manage.py runserver`
- Celery (Windows): `celery -A cts_turismo_backend worker --loglevel=info --pool=solo`
- Frontend: `cd frontend && npm install && npm run dev`

> En Linux/macOS no es necesario `--pool=solo`.

## Flujo del concurso

1. Inscripción del usuario (nombre, email, teléfono)
2. Validación de duplicados por email
3. Envío de correo con enlace de verificación
4. Creación de contraseña tras verificar el correo
5. Confirmación de participación
6. Selección de ganador aleatorio por admin
7. Notificación automática al ganador vía email

## Endpoints principales

**Registro participante:** `POST /api/participants/registrar/`  
Request: `{"first_name":"Juan","last_name":"Pérez","email":"juan@example.com","phone":"1234567890","password":"contraseña123"}`  
Response: `{"message":"¡Gracias por registrarte! Revisa tu correo para verificar tu cuenta."}`

**Verificación de correo:** `GET /api/participants/verify-email/<token>/`  
Response: `{"message":"Tu cuenta ha sido activada. Ya estás participando en el sorteo."}`

**Listado participantes (admin):** `GET /api/participants/admin/participants/?is_verified=true`  
Response: `[{"id":1,"first_name":"Juan","last_name":"Pérez","email":"juan@example.com","is_verified":true}]`

**Seleccionar ganador (admin):** `POST /api/participants/admin/participants/draw_winner/`  
Response: `{"winner":{"id":3,"first_name":"Ana","last_name":"Gómez","email":"ana@example.com"}}`

## Decisiones técnicas

- Celery + Redis para envío asíncrono de correos
- Django REST Framework para endpoints claros y manejo de serialización
- Email único como `USERNAME_FIELD` para evitar registros duplicados
- Contraseñas encriptadas, rutas protegidas para admin y token único de verificación
- En Windows, Celery usa `--pool=solo` para evitar errores de multiprocessing

## Formato para SMTP de Gmail

EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=tu_correo@gmail.com
EMAIL_HOST_PASSWORD=tu_app_password
DEFAULT_FROM_EMAIL=tu_correo@gmail.com
FRONTEND_URL=http://localhost:5173
