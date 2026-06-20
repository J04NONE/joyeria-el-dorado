# Joyería "El Dorado" — Sistema de Gestión Full-Stack

**Autor:** Joan Michael Murillo  
**Estado:** ✅ Completo — 56 tests pasando, documentación OpenAPI integrada, soporte para PostgreSQL (Neon). Auditoría frontend 2026-06-20: rutas CSS/JS y puerto de API corregidos, código y assets duplicados eliminados (ver §9).

---

## 1. Descripción General

Sistema web full-stack para la gestión integral de la **Joyería El Dorado**. Permite administrar inventario de productos, clientes, proveedores, procesar ventas y controlar acceso mediante un sistema de roles (administrador, vendedor, cliente).

- **Backend:** API RESTful con Django 5.2 + Django REST Framework 3.16 + JWT
- **Frontend:** HTML5 semántico + CSS3 (Flexbox/Grid) + JavaScript (ES6+)
- **Documentación API:** Swagger UI + ReDoc + OpenAPI 3.0.3 (via drf-spectacular)

---

## 2. Estructura del Proyecto

```
joyeria/
├── backend/                  # API Django REST
│   ├── joyeria_backend/      # Configuración (settings, urls, wsgi/asgi)
│   ├── autenticacion/        # Registro, login, roles JWT
│   ├── clientes/             # CRUD de clientes
│   ├── inventario/           # Productos, stock y categorías
│   ├── ventas/               # Ventas, productos vendidos, garantías
│   ├── proveedores/          # CRUD de proveedores
│   ├── docs/                 # Documentación de flujos
│   ├── manage.py             # Comando principal Django
│   ├── requirements.txt      # Dependencias Python
│   ├── .env                  # Variables de entorno (no versionar)
│   └── env_joyeria/          # Entorno virtual (no versionar)
│
├── frontend/                 # Cliente web
│   ├── pages/                # Archivos HTML (14 páginas)
│   ├── css/                  # Hojas de estilo (16 archivos)
│   ├── js/                   # Scripts JS
│   └── assets/               # Imágenes y recursos
│
├── docs/                     # Documentación global
│   ├── findings.md           # Diagnóstico del proyecto
│   ├── task_plan.md          # Plan de trabajo
│   ├── progress.md           # Registro de progreso
│   └── roles.md              # Auditoría del sistema de roles
│
├── .env.example              # Plantilla de variables de entorno
├── .gitignore                # Ignorados (Python + Django + IDE)
├── .stylelintrc.json         # Configuración de Stylelint
├── CREDENCIALES_PRUEBA.md    # Credenciales de prueba
├── LICENSE                   # Licencia MIT
└── README.md                 # Este archivo
```

---

## 3. Tecnologías

### Backend
| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.8+ | Lenguaje base |
| Django | 5.2.3 | Framework web |
| Django REST Framework | 3.16.0 | API REST |
| SimpleJWT | 5.5.0 | Autenticación JWT |
| django-cors-headers | 4.7.0 | CORS |
| Pillow | 11.3.0 | Procesamiento de imágenes |
| drf-spectacular | 0.29.0 | Documentación OpenAPI/Swagger |
| SQLite / PostgreSQL (Neon) | — | Base de datos |
| dj-database-url | 2.3.0 | Parseo de `DATABASE_URL` para Neon |

### Frontend
| Tecnología | Propósito |
|------------|-----------|
| HTML5 | Estructura semántica |
| CSS3 (Flexbox + Grid) | Diseño responsivo |
| JavaScript (ES6+) | Interactividad, consumo de API |
| Font Awesome (CDN) | Iconografía |
| localStorage | Persistencia de sesión/carrito |

---

## 4. Instalación Rápida

### Prerrequisitos
- Python 3.8+
- Navegador web moderno

### Backend
```bash
cd backend

# Crear y activar entorno virtual
python -m venv env_joyeria
# Windows:
env_joyeria\Scripts\activate
# Linux/Mac:
source env_joyeria/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos y grupos
python manage.py migrate
python manage.py setup_groups

# Iniciar servidor
python manage.py runserver
```

### Frontend
```bash
python -m http.server 8080
```

Abrir en el navegador: `http://localhost:8080/frontend/pages/dashboard.html`

### Credenciales de Prueba
Ver `CREDENCIALES_PRUEBA.md` para usuarios de prueba.

---

## 5. API Endpoints

| Recurso | Endpoint Base | Métodos |
|---------|--------------|---------|
| Productos | `/api/inventario/productos/` | GET, POST, PUT, PATCH, DELETE |
| Clientes | `/api/clientes/` | GET, POST, PUT, PATCH, DELETE |
| Proveedores | `/api/proveedores/` | GET, POST, PUT, PATCH, DELETE |
| Ventas | `/api/ventas/` | GET, POST, PUT, PATCH, DELETE |
| Productos de Venta | `/api/ventas/productos/` | GET, POST, PUT, PATCH, DELETE |
| Garantías | `/api/ventas/garantias/` | GET, POST, PUT, PATCH, DELETE |
| Autenticación | `/api/auth/` | login, register, profile, token/refresh |

### Documentación Interactiva
Una vez el servidor esté corriendo:
- **Swagger UI:** `http://localhost:8000/api/schema/swagger-ui/`
- **ReDoc:** `http://localhost:8000/api/schema/redoc/`
- **Schema OpenAPI:** `http://localhost:8000/api/schema/`

---

## 6. Tests

El proyecto cuenta con **56 tests unitarios** que cubren todas las apps del backend:

| App | Tests | Cobertura |
|-----|-------|-----------|
| Autenticación | 6 | Registro, login, JWT, roles |
| Clientes | 12 | Modelo + API CRUD + validaciones |
| Inventario | 5 | Productos, stock, permisos |
| Proveedores | 11 | Modelo + API CRUD + validaciones |
| Ventas | 22 | Ventas, Garantías, VentaProducto |

```bash
cd backend
env_joyeria\Scripts\activate
python manage.py test
```

---

## 7. Roles del Sistema

| Rol | Acceso |
|-----|--------|
| **Administrador** | Gestión usuarios, productos, ventas, reportes |
| **Vendedor** | Gestión productos, procesar ventas |
| **Cliente** | Catálogo, carrito, historial de pedidos |
| **Invitado** | Solo ver catálogo |

---

## 8. Variables de Entorno

Copiar `.env.example` a `.env` dentro de `backend/` y configurar:

```env
SECRET_KEY=tu-clave-secreta
DEBUG=True
DB_ENGINE=django.db.backends.sqlite3
CORS_ALLOW_ALL_ORIGINS=True
```

Por defecto usa **SQLite** para desarrollo. Para PostgreSQL, configurar:
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=joyeria_db
DB_USER=postgres
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=5432
```

### Neon (PostgreSQL serverless)

Si se define `DATABASE_URL`, tiene prioridad sobre la configuración anterior:
```env
DATABASE_URL=postgresql://usuario:password@host.neon.tech/dbname?sslmode=require
```

> **Nota sobre tests:** Neon usa un *connection pooler* que puede mantener una sesión
> abierta y bloquear el `DROP DATABASE` al finalizar `python manage.py test`. Si ves
> `database "test_..." is being accessed by other users`, corré los tests con
> `python manage.py test --keepdb` (reutiliza la base de prueba en vez de borrarla).

---

## 9. Documentación Adicional

- `CLAUDE.md` — Contexto resumido del proyecto (stack, estructura, comandos,
  gotchas conocidos) para asistentes de IA como Claude Code
- `docs/roles.md` — Auditoría del sistema de vistas por rol
- `docs/findings.md` — Diagnóstico completo del proyecto
- `docs/task_plan.md` — Plan de trabajo detallado
- `backend/docs/FLUJO_AUTENTICACION_JWT.md` — Flujo JWT
- `backend/docs/FLUJO1_REGISTRO_PUBLICO.md` — Registro público
- `backend/docs/INTEGRACION_PROYECTO_JOYERIA.md` — Integración general

### Auditoría frontend (2026-06-20)

El proyecto quedó con una reorganización de carpetas incompleta desde su
desarrollo original (más de un año atrás). Auditoría con Playwright MCP contra
el backend en ejecución encontró y corrigió:

- **Rutas CSS/JS rotas:** `css/` y `js/` vivían en la raíz del repo, pero las
  14 páginas HTML los referenciaban como `../css/`, `../js/` (rutas relativas
  a `frontend/pages/`), causando 404 en todas las páginas. Se movieron ambas
  carpetas a `frontend/css/` y `frontend/js/`.
- **Puerto incorrecto de la API:** `frontend/js/config.js` apuntaba a
  `http://127.0.0.1:8001`, pero `manage.py runserver` usa el puerto `8000` por
  defecto — rompía login y toda llamada a la API. Corregido a `8000`.
- **Limpieza de duplicados/código muerto:** se eliminó un `assets/` huérfano
  en la raíz del repo (idéntico byte a byte a `frontend/assets/`) y
  `js/apiService.js` (no referenciado por ninguna página; todas usan
  `js/api.js`).

---

## 10. Licencia

MIT License — Ver `LICENSE` para más detalles.
