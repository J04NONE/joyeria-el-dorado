# Joyeria El Dorado - Backend Django

## Descripcion General

API RESTful desarrollada con **Django 5.2** y **Django REST Framework 3.16**.

---

## Estructura

```
backend/
├── joyeria_backend/      # Configuracion global (settings, urls, wsgi, asgi)
├── autenticacion/        # Registro, login, roles y JWT
├── clientes/             # Gestion de clientes (CRUD)
├── inventario/           # Productos, stock y categorias
├── ventas/               # Ventas, productos vendidos y garantias
├── proveedores/          # Gestion de proveedores (CRUD)
├── docs/                 # Documentacion tecnica y de flujos
├── env_joyeria/          # Entorno virtual (no versionar)
├── manage.py             # Comando principal Django
├── requirements.txt      # Dependencias
├── .env                  # Variables de entorno locales
└── README.md             # Este archivo
```

---

## Dependencias

- asgiref==3.8.1
- Django==5.2.3
- django-cors-headers==4.7.0
- djangorestframework==3.16.0
- djangorestframework_simplejwt==5.5.0
- pillow==11.3.0
- psycopg2-binary==2.9.10
- PyJWT==2.9.0
- python-dotenv==1.2.2
- sqlparse==0.5.3
- tzdata==2025.2

---

## Configuracion con Variables de Entorno

El backend usa `python-dotenv` para cargar configuracion desde `.env`.

| Variable | Default | Descripcion |
|----------|---------|-------------|
| SECRET_KEY | (dev) | Clave secreta de Django |
| DEBUG | True | Modo debug |
| DB_ENGINE | sqlite3 | Motor de BD |
| DB_NAME | db.sqlite3 | Nombre BD |

### Desarrollo local (SQLite - recomendado)

El archivo `.env` incluido ya configura SQLite.

---

## Instalacion

```bash
cd backend
python -m venv env_joyeria
# Windows: env_joyeria\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py setup_groups
python manage.py runserver
```

---

## Endpoints

| Endpoint | Metodo | Descripcion |
|----------|--------|-------------|
| /api/auth/login/ | POST | Login JWT |
| /api/auth/register/ | POST | Registro publico |
| /api/inventario/productos/ | GET,POST | Productos CRUD |
| /api/clientes/clientes/ | GET,POST | Clientes CRUD |
| /api/ventas/ventas/ | GET,POST | Ventas CRUD |
| /api/proveedores/proveedores/ | GET,POST | Proveedores CRUD |

---

## Tests

```bash
python manage.py test
```

Tests: autenticacion (4), inventario (6).

---

## Roles

| Grupo | Rol API | Permisos |
|-------|---------|----------|
| Administradores | administrador | Acceso total |
| Vendedores | vendedor | Productos y ventas |
| Clientes | cliente | Catalogo y compras |

---

**Estado:** Backend funcional con SQLite para desarrollo.
