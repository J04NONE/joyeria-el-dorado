# Auditoría y Documentación del Sistema de Vistas por Rol - Joyería El Dorado Frontend

Este documento detalla la implementación del sistema de vistas por rol en el frontend de la Joyería El Dorado. Se analiza cómo cada página HTML y los archivos CSS asociados contribuyen a la adaptación de la interfaz de usuario según el rol del usuario (`administrador`, `vendedor`, `cliente`, `invitado`).

---

## 1. Principio Arquitectónico del Sistema de Roles

Se reafirma el principio arquitectónico que rige la visibilidad por roles:
- **Backend es la Verdad:** El backend (API de Django) autentica al usuario y devuelve el rol en un formato estandarizado (ej., `"administrador"`, `"vendedor"`).
- **JavaScript (JS) es el Mensajero:** El script `menu.js` lee el rol de `localStorage` y aplica una única clase `role-[rol_en_minusculas]` al `<body>` del documento. También gestiona las redirecciones de acceso a páginas restringidas.
- **HTML es el Lienzo:** Los elementos HTML poseen clases específicas (`nav-admin-only`, `action-cliente-only`, etc.) que indican su visibilidad condicionada.
- **CSS es el Estilista:** Las reglas CSS (`body.role-[rol_en_minusculas] .clase-elemento`) controlan el `display` de los elementos, mostrándolos u ocultándolos según la clase del `<body>`.

---

## 2. Configuración Global de Roles (JS y CSS)

### 2.1. Gestión de Roles en JavaScript (`js/menu.js`)
- El archivo `menu.js` es responsable de leer el rol del usuario desde `localStorage` y aplicar la clase correspondiente al `<body>`. Esto permite que las reglas CSS actúen sobre los elementos según el rol.
- La función `verificarAccesoPorRol()` valida si el usuario tiene permiso para acceder a la página actual, redirigiendo a `dashboard.html` si no es así.

**Ejemplo de Código:**
```javascript
// Ejemplo de cómo se aplica la clase al body
const userRole = userRoleRaw ? userRoleRaw.toLowerCase().replace(/s$/, '') : 'invitado';
document.body.className = document.body.className.replace(/role-\w+/g, '').trim();
document.body.classList.add(`role-${userRole}`);
```

```javascript
// Ejemplo de la estructura de verificarAccesoPorRol
function verificarAccesoPorRol(userRole) {
    const paginaActual = window.location.pathname.split('/').pop() || 'index.html';
    const permisosDePaginas = { /* ... matriz de permisos ... */ };
    if (!paginasPermitidasParaRol.includes(paginaActual)) { /* ... redirección ... */ }
}
```

### 2.2. Reglas CSS Globales de Visibilidad (`css/base.css` y `css/header.css`)

- Las hojas de estilo principales definen reglas generales para ocultar por defecto los elementos restringidos y mostrarlos solo cuando el `<body>` tiene la clase de rol adecuada.

**Ejemplo de Código:**
```css
/* Ocultar por defecto los elementos de navegación restringidos */
.nav-admin-only,
.nav-admin-vendor-only,
.nav-cliente-only,
.nav-logout-link,
.cart-icon-wrapper {
    display: none !important;
}
.nav-login-link {
    display: list-item !important; /* Visible por defecto para invitados */
}

/* Mostrar para roles específicos */
body.role-administrador .nav-admin-only,
body.role-administrador .nav-admin-vendor-only,
body.role-administrador .nav-logout-link {
    display: list-item !important;
}
body.role-vendedor .nav-admin-vendor-only,
body.role-vendedor .nav-logout-link {
    display: list-item !important;
}
body.role-cliente .nav-cliente-only,
body.role-cliente .cart-icon-wrapper,
body.role-cliente .nav-logout-link {
    display: list-item !important;
}
body.role-cliente .cart-icon-wrapper {
    display: flex !important;
    align-items: center;
}
body.role-cliente .nav-login-link,
body.role-vendedor .nav-login-link,
body.role-administrador .nav-login-link {
    display: none !important;
}
```

---

## 3. Implementación de Vistas por Rol (Análisis por Página HTML)

### 3.1. Página: `dashboard.html`

- **Objetivo:** Página principal que se adapta al rol del usuario, mostrando información y acciones relevantes.
- **Configuración de Vistas por Rol (HTML):**
    - Se utilizan clases como `action-cliente-only`, `action-admin-only`, `action-vendedor-only`, `action-admin-vendedor-only` para controlar la visibilidad de secciones como "Acciones Rápidas", el carrusel de productos (`product-carousel`) y las estadísticas (`dashboard-stats`).
    - El menú de navegación utiliza clases `nav-admin-only`, `nav-admin-vendor-only`, `nav-cliente-only` para mostrar enlaces según el rol.
    - El ícono del carrito tiene la clase `cart-icon-wrapper nav-cliente-only`.
    - **Ejemplo de Código:**
      ```html
      <section class="product-carousel action-cliente-only">...</section>
      <section class="dashboard-stats action-admin-vendedor-only">...</section>
      <a href="reporte_ventas.html" class="accion-card action-admin-only">Ver Reportes</a>
      <li class="nav-admin-only"><a href="administracion_de_usuarios.html">Gestión de Usuarios</a></li>
      <div class="cart-icon-wrapper nav-cliente-only">...</div>
      ```
- **Archivos CSS Relevantes:** `css/dashboard.css` (controla el `display` de estas secciones).

### 3.2. Página: `login.html` y `registro_de_cliente.html`

- **Objetivo:** Páginas de autenticación y creación de cuenta.
- **Configuración de Vistas por Rol (HTML):**
    - El `<header>` es simplificado (`auth-header`), sin navegación de rol ni elementos condicionales.
    - El `<body>` no tiene clase de rol inicial; la visibilidad está controlada por la redirección de `menu.js`.
    - **Ejemplo de Código:**
      ```html
      <body class="auth-body">
        <header class="auth-header">...</header>
        <main class="login-container">...</main>
      </body>
      ```
- **Archivos CSS Relevantes:** `css/login.css`, `css/base.css`.

### 3.3. Página: `lista_de_productos.html`

- **Objetivo:** Catálogo de productos.
- **Configuración de Vistas por Rol (HTML):**
    - El menú de navegación en el `header` utiliza las clases de visibilidad por rol.
    - El botón "Agregar al Carrito" depende de la lógica JS para restringir a clientes.
    - **Ejemplo de Código:**
      ```html
      <li class="nav-cliente-only"><a href="historial_ordenes.html">Mis Pedidos</a></li>
      <button class="btn-producto btn-agregar-carrito">Agregar</button>
      ```
- **Archivos CSS Relevantes:** `css/catalogo.css`.

### 3.4. Página: `detalle_de_producto.html`

- **Objetivo:** Vista detallada de un producto.
- **Configuración de Vistas por Rol (HTML):**
    - El menú de navegación en el `header` utiliza las clases de visibilidad por rol.
    - El botón "Agregar al Carrito" depende de la lógica JS para restringir a clientes.
    - **Ejemplo de Código:**
      ```html
      <li class="nav-cliente-only"><a href="historial_ordenes.html">Mis Pedidos</a></li>
      <button class="btn btn-primary btn-large" id="add-to-cart">Agregar al Carrito</button>
      ```
- **Archivos CSS Relevantes:** `css/detalle_producto.css`.

### 3.5. Página: `carrito.html`

- **Objetivo:** Gestión del carrito de compras por el cliente.
- **Configuración de Vistas por Rol (HTML):**
    - El menú de navegación y el ícono del carrito utilizan las clases `nav-cliente-only` y `cart-icon-wrapper nav-cliente-only`.
    - El acceso está restringido a clientes mediante `menu.js`.
    - **Ejemplo de Código:**
      ```html
      <div class="cart-icon-wrapper nav-cliente-only">...</div>
      ```
- **Archivos CSS Relevantes:** `css/carrito.css`.

### 3.6. Página: `historial_ordenes.html`

- **Objetivo:** Visualización del historial de pedidos del cliente.
- **Configuración de Vistas por Rol (HTML):**
    - El menú de navegación utiliza la clase `nav-cliente-only` para el enlace "Mis Pedidos".
    - El acceso está restringido a clientes mediante `menu.js`.
    - **Ejemplo de Código:**
      ```html
      <li class="nav-cliente-only"><a href="historial_ordenes.html">Mis Pedidos</a></li>
      ```
- **Archivos CSS Relevantes:** `css/gestion.css`.

### 3.7. Página: `administracion_de_usuarios.html`

- **Objetivo:** Tabla para visualizar y buscar usuarios existentes (rol Admin).
- **Configuración de Vistas por Rol (HTML):**
    - El menú de navegación utiliza la clase `nav-admin-only` para el enlace "Gestión de Usuarios".
    - El acceso está restringido a administradores mediante `menu.js`.
    - **Ejemplo de Código:**
      ```html
      <li class="nav-admin-only"><a href="administracion_de_usuarios.html">Gestión de Usuarios</a></li>
      ```
- **Archivos CSS Relevantes:** `css/administracion_de_usuarios.css`.

### 3.8. Página: `actualizar_datos_usuario.html`

- **Objetivo:** Formulario para editar datos de un usuario específico (rol Admin).
- **Configuración de Vistas por Rol (HTML):**
    - No tiene enlace directo en la navegación principal; se accede desde la tabla de usuarios.
    - El acceso está restringido a administradores mediante `menu.js`.
    - **Ejemplo de Código:**
      ```html
      <body class="role-admin">...</body>
      ```
- **Archivos CSS Relevantes:** `css/administracion_de_usuarios.css`.

### 3.9. Página: `gestion_de_productos.html`

- **Objetivo:** Gestión unificada de productos (registro, búsqueda, actualización, eliminación) para Admin y Vendedor.
- **Configuración de Vistas por Rol (HTML):**
    - El menú de navegación utiliza la clase `nav-admin-vendedor-only` para el enlace "Gestión de Productos".
    - El acceso está restringido a administradores y vendedores mediante `menu.js`.
    - **Ejemplo de Código:**
      ```html
      <li class="nav-admin-vendedor-only"><a href="gestion_de_productos.html">Gestión de Productos</a></li>
      ```
- **Archivos CSS Relevantes:** `css/gestion_de_productos.css`.

### 3.10. Página: `proceso_ventas.html`

- **Objetivo:** Procesamiento de ventas (Admin y Vendedor).
- **Configuración de Vistas por Rol (HTML):**
    - El menú de navegación utiliza la clase `nav-admin-vendedor-only` para el enlace "Procesar Venta".
    - El acceso está restringido a administradores y vendedores mediante `menu.js`.
    - **Ejemplo de Código:**
      ```html
      <li class="nav-admin-vendedor-only"><a href="proceso_ventas.html">Procesar Venta</a></li>
      ```
- **Archivos CSS Relevantes:** `css/ventas.css`.

### 3.11. Página: `reporte_ventas.html`

- **Objetivo:** Generación y visualización de reportes de ventas (rol Admin).
- **Configuración de Vistas por Rol (HTML):**
    - El menú de navegación utiliza la clase `nav-admin-only` para el enlace "Reportes".
    - El acceso está restringido a administradores mediante `menu.js`.
    - **Ejemplo de Código:**
      ```html
      <li class="nav-admin-only"><a href="reporte_ventas.html">Reportes</a></li>
      ```
- **Archivos CSS Relevantes:** `css/reporte_ventas.css`.

---

## 4. Inconsistencias e Incompatibilidades Detectadas (Hallazgos de la Auditoría)

- **`menu.js`:** Revisar la línea `userRole.toLowerCase().replace(/s$/, '')` para asegurar que siempre maneje correctamente los nombres de roles singulares y en minúsculas provenientes del backend (ej. si el backend envía "Vendedores", que JavaScript lo convierta a "vendedor").
- **HTML - `header`:** Confirmar que el SVG del carrito y el formulario de búsqueda estén presentes en **todos** los `<header>` donde deberían estar (ya que la auditoría previa sugirió que algunos los tenían y otros no).
- **HTML - Dashboard `action-item`:** Asegurar que las clases de visibilidad (`action-admin-only`, etc.) en las "Acciones Rápidas" del dashboard sean las correctas y que no haya acciones de prueba.
- **CSS - Nomenclatura de Roles:** Reafirmar que **TODOS** los selectores `body.role-[rol]` en todos los archivos CSS estén **exactamente** en minúsculas (ej., `body.role-vendedor`, no `body.role-Vendedor` o `body.role-vendor`).
- **CSS - Reglas de `display`:** Verificar que las reglas de `display: none !important;` y `display: list-item !important;` (o `flex`, `block`) sean las correctas y no estén en conflicto para cada clase de visibilidad (`nav-*`, `cart-icon-wrapper`).
- **CSS - `product-carousel` y `dashboard-stats`:** Asegurar que el `display` de estas secciones en `dashboard.css` se controle **solo** por las clases `action-cliente-only` y `action-admin-vendedor-only` respectivamente, y no haya conflictos generales.

---
