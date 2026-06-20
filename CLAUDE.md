# Joyería El Dorado — Contexto del Proyecto

Sistema de gestión full-stack para una joyería. Backend Django 5.2 + Django
REST Framework 3.16 + JWT (SimpleJWT). Frontend HTML5 + CSS3 + JavaScript
(ES6+) vanilla, sin framework.

## Estructura real (tal como está hoy en disco)

- `backend/` — proyecto Django. Apps: `autenticacion`, `clientes`,
  `inventario`, `ventas`, `proveedores`. Config principal en
  `backend/joyeria_backend/`.
- `css/` y `js/` — en la **raíz del repo** (no dentro de `frontend/`).
- `frontend/` — subcarpeta anidada con `assets/` y `pages/` (los `.html`).
- `docs/` — documentación adicional (`findings.md`, `task_plan.md`,
  `progress.md`, `roles.md`). Nota: `task_plan.md` describe una reorganización
  de carpetas que quedó parcialmente aplicada — no asumir que `css/`/`js/` ya
  están movidos dentro de `frontend/`.

## Comandos esenciales

```bash
cd backend
env_joyeria\Scripts\activate        # Windows
pip install -r requirements.txt
python manage.py migrate
python manage.py setup_groups       # crea grupos Administradores/Empleados/Clientes
python manage.py runserver
python manage.py test --keepdb      # ver gotcha de Neon abajo
```

Frontend (servidor estático simple):
```bash
cd frontend  # o la raíz, según desde dónde se sirvan los HTML
python -m http.server 8000
```

## Base de datos

- **Por defecto:** SQLite (`backend/db.sqlite3`), sin configuración extra.
- **Neon (PostgreSQL serverless):** se activa definiendo `DATABASE_URL` en
  `backend/.env`. Si esa variable existe, tiene prioridad sobre SQLite (ver
  `backend/joyeria_backend/settings.py:104-113`). Usa `dj_database_url.config()`
  con `ssl_require=True` y `conn_health_checks=True`, más
  `DISABLE_SERVER_SIDE_CURSORS = True` agregado a mano (requerido por el
  connection pooler de Neon).
- **Gotcha:** el pooler de Neon puede mantener una sesión abierta y bloquear
  el `DROP DATABASE` al final de `python manage.py test`. Si aparece
  `database "test_..." is being accessed by other users`, correr con
  `python manage.py test --keepdb`.

## Convenciones

- **Roles del sistema:** administrador, vendedor, cliente, invitado (ver
  `docs/roles.md` para el detalle de accesos por rol).
- **Autenticación:** JWT vía `/api/auth/` (login, register, profile,
  token/refresh).
- **Documentación interactiva de la API:** Swagger UI en
  `/api/schema/swagger-ui/`, ReDoc en `/api/schema/redoc/` (drf-spectacular).

## Gotchas conocidos

- **Encoding en consola de Windows:** algunos comandos de gestión (ej.
  `setup_groups`) escriben emojis a stdout. La consola de Windows usa cp1252
  por defecto y puede fallar con `UnicodeEncodeError`. Si pasa, correr con
  `PYTHONIOENCODING=utf-8` antes del comando.

## Mantenimiento de este archivo

Se actualiza a mano cuando se descubre un gotcha nuevo o cambia la estructura
real del proyecto. No se genera ni se sincroniza automáticamente.
