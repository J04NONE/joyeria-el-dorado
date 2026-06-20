/**
 * Realiza una petición fetch añadiendo automáticamente el token de autenticación.
 * También maneja la redirección al login si el token es inválido o ha expirado.
 * @param {string} url - El endpoint de la API al que se va a llamar.
 * @param {object} options - El objeto de opciones para la petición fetch (method, body, etc.).
 * @returns {Promise<Response>} - La promesa con la respuesta del servidor.
 */
async function fetchWithAuth(url, options = {}) {
    // 1. Obtener el token de acceso desde localStorage.
    const token = localStorage.getItem('accessToken');

    // 2. Configurar los encabezados (headers) por defecto.
    const headers = {
        'Content-Type': 'application/json',
        ...options.headers, // Permite que la llamada original añada o sobreescriba headers.
    };

    // 3. Si existe un token, añadirlo al encabezado de Autorización.
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    // 4. Realizar la petición fetch con la URL y las opciones configuradas.
    const response = await fetch(url, { ...options, headers });

    // 5. Manejar el caso común de un token expirado (error 401 Unauthorized).
    if (response.status === 401) {
        // En una aplicación más compleja, aquí intentaríamos refrescar el token.
        // Por simplicidad para este proyecto, limpiaremos los datos de sesión y redirigiremos al login.
        console.error('No autorizado o token expirado. Redirigiendo al login.');
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        localStorage.removeItem('userRole');
        localStorage.removeItem('userName');
        window.location.href = 'login.html';
        // Lanzamos un error para detener la ejecución del código que hizo la llamada.
        throw new Error('No autorizado');
    }

    // 6. Devolver la respuesta para que sea manejada por quien llamó a la función.
    return response;
} 