/**
 * @file Configuración global para la URL base de la API del backend.
 * Este archivo centraliza la URL para facilitar cambios en entornos de desarrollo y producción.
 * @author Joan Michael Murillo
 */

// URL base de la API de Django. Asegúrate que el puerto coincida con tu servidor Django.
// En desarrollo local, comúnmente es 8000 o 8001. Verifica tu 'manage.py runserver'
const API_BASE_URL = 'http://127.0.0.1:8001'; 
// Si tu servidor Django corre en el puerto 8001, cámbialo a:
// const API_BASE_URL = 'http://127.0.0.1:8001';

// Exportar la constante para que otros módulos JS puedan importarla si se usa ESM
// export { API_BASE_URL }; // Para módulos ES6
