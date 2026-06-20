# 📋 Plan de Reestructuración - Joyería "El Dorado"

**Objetivo:** Organizar, documentar y preparar el proyecto para desarrollo continuo.

---

## Fase 1: 🛠️ Diagnóstico y Reparación Urgente

- [ ] **1.1** Reparar archivos corruptos (`login.js`, `gestion_de_productos.js`, `requirements.txt`)
- [ ] **1.2** Configurar `.gitignore` para Python/Django (agregar `__pycache__`, `*.pyc`, `env_joyeria/`, `media/`, `.env`)
- [ ] **1.3** Crear `.env.example` con configuración base
- [ ] **1.4** Cambiar settings.py para leer desde variables de entorno
- [ ] **1.5** Cambiar a SQLite como BD por defecto (con opción PostgreSQL)

## Fase 2: 📂 Reestructuración del Proyecto

- [ ] **2.1** Crear estructura estándar:
  ```
  proyecto/
  ├── backend/           ← joyeria_api/ movido aquí
  │   ├── joyeria_backend/
  │   ├── autenticacion/
  │   ├── clientes/
  │   ├── inventario/
  │   ├── ventas/
  │   ├── proveedores/
  │   └── docs/
  ├── frontend/          ← Todo lo que no es backend
  │   ├── pages/         ← Archivos HTML
  │   ├── css/
  │   ├── js/
  │   └── assets/
  ├── .env.example
  ├── .gitignore
  ├── README.md
  └── LICENSE
  ```
- [ ] **2.2** Mover `joyeria_api/` a `backend/`
- [ ] **2.3** Mover HTML a `frontend/pages/`
- [ ] **2.4** Consolidar assets en `frontend/assets/`
- [ ] **2.5** Eliminar carpeta `frontend/` duplicada (solo tenía `roles.md`)
- [ ] **2.6** Actualizar rutas en archivos HTML y JS

## Fase 3: 📚 Documentación Completa

- [ ] **3.1** Reescribir `README.md` principal (visión general)
- [ ] **3.2** Crear `backend/README.md`
- [ ] **3.3** Crear `frontend/README.md`
- [ ] **3.4** Crear `docs/ARCHITECTURE.md` (diagrama de arquitectura)
- [ ] **3.5** Crear `docs/API_REFERENCE.md` (todos los endpoints)
- [ ] **3.6** Crear `docs/SETUP_GUIDE.md` (guía de instalación unificada)
- [ ] **3.7** Actualizar `CHANGELOG.md`

## Fase 4: 🧪 Unificación y Limpieza

- [ ] **4.1** Unificar `api.js` y `apiService.js`
- [ ] **4.2** Corregir `menu.js` (bug de expresiones regulares)
- [ ] **4.3** Estandarizar `API_BASE_URL` (puerto consistente)
- [ ] **4.4** Agregar migraciones faltantes si es necesario

## Fase 5: ✅ Verificación

- [ ] **5.1** Verificar que el backend migre con SQLite
- [ ] **5.2** Verificar que los tests del backend pasen
- [ ] **5.3** Revisión final de código

---

**Estado Actual:** ⏳ En progreso
**Última Actualización:** Julio 2025
