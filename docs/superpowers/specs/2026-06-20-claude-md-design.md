# Diseño: CLAUDE.md del proyecto

**Fecha:** 2026-06-20
**Objetivo:** reducir el consumo de tokens al iniciar sesiones de Claude Code en este
repositorio, evitando que cada sesión nueva tenga que re-explorar el proyecto
(README, settings.py, requirements.txt, estructura de carpetas) para orientarse.

## Problema

Hoy no existe un `CLAUDE.md` en la raíz. Cada sesión nueva de Claude Code:
- Re-deriva el stack, la estructura y las convenciones leyendo varios archivos.
- No tiene memoria de gotchas ya resueltos (ej. el comportamiento del pooler de
  Neon con `python manage.py test`).

## Alcance

Un único archivo `CLAUDE.md` en la **raíz real del repositorio git** — la carpeta
que contiene `backend/`, `docs/` y `.git/` (que en disco se llama, confusamente,
`frontend`, por el nombre de la carpeta del proyecto). **No** se refiere a la
subcarpeta anidada `frontend/` que existe dentro de esa raíz (el cliente web,
con `assets/` y `pages/`). El archivo final queda en
`<raíz del repo>/CLAUDE.md`, autocontenido y corto (~1 pantalla), en español,
cargado automáticamente por Claude Code al iniciar sesión en este directorio.

**Fuera de alcance:** RAG / vector DB / indexado de embeddings. Para un proyecto
de ~90 archivos, el costo de mantener un índice semántico supera el ahorro de
tokens. Claude Code ya cuenta con Grep/Glob para exploración puntual on-demand;
lo que falta es el resumen persistente de alto nivel, que es exactamente lo que
resuelve un CLAUDE.md.

## Contenido del CLAUDE.md

1. **Qué es el proyecto** — 1-2 líneas: Joyería El Dorado, backend Django 5.2 +
   DRF + JWT, frontend HTML/CSS/JS vanilla.
2. **Estructura real** — rutas clave tal como están hoy en disco (no la
   estructura "objetivo" de `task_plan.md`, que quedó parcialmente aplicada):
   `backend/` (apps: autenticacion, clientes, inventario, ventas, proveedores);
   `css/` y `js/` en la raíz del repo; `frontend/` (subcarpeta anidada) con
   `assets/` y `pages/`; `docs/` con documentación adicional.
3. **Comandos esenciales** — activar venv, `migrate`, `test` (con nota de
   `--keepdb` para Neon), `runserver`, `setup_groups`.
4. **Base de datos** — SQLite por defecto; Neon vía `DATABASE_URL` (con
   `sslmode=require`, pooler, `CONN_HEALTH_CHECKS`). Gotcha: el pooler de Neon
   bloquea el `DROP DATABASE` al finalizar los tests sin `--keepdb`.
5. **Convenciones** — roles del sistema (administrador, vendedor, cliente,
   invitado), autenticación JWT vía `/api/auth/`.
6. **Gotchas conocidos** — encoding de consola en Windows (emojis en
   `stdout.write` rompen con cp1252; usar `PYTHONIOENCODING=utf-8` si aparece
   `UnicodeEncodeError`).

## Mantenimiento

Este archivo se actualiza a mano cuando se descubre un gotcha nuevo o cambia
la estructura del proyecto. No se genera ni se sincroniza automáticamente.
