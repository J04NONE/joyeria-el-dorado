/**
 * Servicio centralizado para llamadas a la API de Django.
 * Todas las funciones devuelven una promesa.
 */

// Asegúrate de que API_BASE_URL esté disponible globalmente (por config.js)
const BASE_URL = typeof API_BASE_URL !== 'undefined' ? API_BASE_URL : 'http://127.0.0.1:8001';

// Función genérica para peticiones GET
function apiGet(endpoint) {
    return fetch(`${BASE_URL}${endpoint}`, {
        credentials: 'include', // útil si usas sesiones/cookies en Django
    })
    .then(response => response.json());
}

// Función genérica para peticiones POST
function apiPost(endpoint, data) {
    return fetch(`${BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(data),
    })
    .then(response => response.json());
}

// Puedes agregar apiPut, apiDelete, etc. según lo necesites

// Ejemplo de exportación para módulos ES6 (si los usas)
// export { apiGet, apiPost };
