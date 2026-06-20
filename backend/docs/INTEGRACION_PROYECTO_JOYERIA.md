# Joyería El Dorado: Visión General del Proyecto y Estrategia de Integración

---

## 1. Introducción

**Joyería El Dorado** es una plataforma integral para la gestión y venta de productos de joyería, compuesta por un frontend moderno y un backend robusto basado en Django. El sistema está diseñado para ofrecer una experiencia de usuario fluida, segura y escalable, permitiendo la administración eficiente de productos, clientes, ventas y usuarios con distintos roles.

**Propósito:**
- Facilitar la venta y gestión de joyas y accesorios.
- Permitir la administración de inventario, clientes y ventas.
- Ofrecer autenticación y control de roles para distintos tipos de usuarios (clientes, vendedores, administradores).

---

## 2. Estructura del Proyecto Backend

```
joyeria_api/
├── autenticacion/      # Registro, login, roles y JWT
├── clientes/           # Gestión de clientes
├── inventario/         # Gestión de productos y stock
├── ventas/             # Gestión de ventas y garantías
├── proveedores/        # Gestión de proveedores
├── joyeria_backend/    # Configuración global, settings, urls, wsgi/asgi
├── docs/               # Documentación técnica y de flujos
├── env_joyeria/        # Entorno virtual Python (no versionar)
├── requirements.txt    # Manifiesto de dependencias
├── manage.py           # Comando principal Django
└── README.md           # Documentación principal
```

- **autenticacion/**: Serializers, views, urls y comandos para registro/login, gestión de roles y JWT. Incluye tests y comando `setup_groups` para crear roles.
- **clientes/**: Modelos, vistas y endpoints para CRUD de clientes.
- **inventario/**: Modelos y endpoints para productos, stock y categorías.
- **ventas/**: Modelos y endpoints para ventas, productos vendidos y garantías.
- **proveedores/**: CRUD de proveedores.
- **joyeria_backend/**: Configuración global (settings, urls, wsgi, asgi).
- **docs/**: Documentación de integración, flujos de autenticación y registro.
- **env_joyeria/**: Entorno virtual Python (no subir a git).

---

## 3. Componentes y Configuración Clave

- **INSTALLED_APPS**: Incluye todas las apps, `rest_framework`, `rest_framework_simplejwt`, `django-cors-headers`.
- **REST_FRAMEWORK**: Define autenticación JWT y permisos globales.
- **SIMPLE_JWT**: Controla la duración y seguridad de los tokens.
- **DATABASES**: Configuración para PostgreSQL.
- **MIDDLEWARE**: Seguridad, sesiones y autenticación.
- **CORS_ALLOW_ALL_ORIGINS**: Permite integración frontend-backend en desarrollo.

---

## 4. Ruteo y Endpoints Principales

| Recurso         | Endpoint Base           | Métodos Disponibles         |
|-----------------|------------------------|----------------------------|
| Productos       | /api/inventario/       | GET, POST, PUT, PATCH, DELETE |
| Clientes        | /api/clientes/         | GET, POST, PUT, PATCH, DELETE |
| Autenticación   | /api/auth/             | register, login, profile, admin/create-user, token/refresh |
| Ventas          | /api/ventas/           | ventas, venta-productos, garantias |
| Proveedores     | /api/proveedores/      | proveedores CRUD           |

---

## 5. Estrategia de Integración Frontend-Backend

- El frontend interactúa con el backend mediante peticiones HTTP (GET, POST, PUT, DELETE) a los endpoints REST definidos.
- El backend responde en formato JSON, facilitando el consumo desde JS.
- El frontend envía credenciales al endpoint `/api/auth/login/` y recibe un token JWT.
- El backend es la autoridad final sobre los roles y permisos, devolviendo esta información en el token JWT.
- El frontend usa el token para autorizar peticiones protegidas y mostrar/ocultar elementos según el rol.

---

## 6. Flujo de Autenticación y Registro

- **Login:** `/api/auth/login/` (POST)
- **Refresh:** `/api/auth/token/refresh/` (POST)
- **Registro público:** `/api/auth/register/` (POST)
- **Perfil:** `/api/auth/profile/` (GET)
- **Crear usuario (admin):** `/api/auth/admin/create-user/` (POST)

Ver detalles y ejemplos en `docs/FLUJO_AUTENTICACION_JWT.md` y `docs/FLUJO1_REGISTRO_PUBLICO.md`.

---

## 7. Inicialización y Comandos Útiles

1. **Crear entorno virtual:**
   ```
   python -m venv env_joyeria
   ```
2. **Activar entorno:**
   - Windows: `env_joyeria\Scripts\activate`
   - Linux/Mac: `source env_joyeria/bin/activate`
3. **Instalar dependencias:**
   ```
   pip install -r requirements.txt
   ```
4. **Migraciones:**
   ```
   python manage.py migrate
   ```
5. **Crear grupos y roles:**
   ```
   python manage.py setup_groups
   ```
6. **Crear superusuario:**
   ```
   python manage.py createsuperuser
   ```
7. **Correr servidor:**
   ```
   python manage.py runserver
   ```

---

**Estado del Proyecto:**
- Backend y frontend listos para integración real.
- Base de código robusta, mantenible y preparada para escalar.
- Documentación y buenas prácticas implementadas. 