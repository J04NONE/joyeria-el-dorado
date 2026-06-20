/**
 * @file Configuración global para la URL base de la API del backend.
 * Este archivo centraliza la URL para facilitar cambios en entornos de desarrollo y producción.
 * @author Joan Michael Murillo
 */

// URL base de la API de Django. Asegúrate que el puerto coincida con tu servidor Django.
// 'manage.py runserver' usa el puerto 8000 por defecto.
const API_BASE_URL = 'http://127.0.0.1:8000';

// Exportar la constante para que otros módulos JS puedan importarla si se usa ESM
// export { API_BASE_URL }; // Para módulos ES6
