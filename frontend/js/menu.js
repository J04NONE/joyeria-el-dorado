/*
 * Archivo: menu.js
 * Versión Definitiva: 6.0 - Estructura Anti-Errores de Alcance
 */
document.addEventListener('DOMContentLoaded', () => {

    // --- 1. DEFINICIÓN CENTRAL DE VARIABLES DE SESIÓN ---
    // Leemos las variables una sola vez al cargar la página.
    // Al ser declaradas aquí, son accesibles para TODAS las funciones dentro de este bloque.
    const userRoleRaw = localStorage.getItem('userRole') || 'invitado';
    const userRole = userRoleRaw.toLowerCase().replace(/es$/, '').replace(/s$/, '');
    const accessToken = localStorage.getItem('accessToken');

    console.log(`Auditoría Definitiva: Rol detectado -> '${userRole}'`);

    // --- 2. EJECUCIÓN DE LAS FUNCIONES PRINCIPALES ---
    actualizarVisibilidadUI(userRole);
    verificarAccesoPorRol(userRole, paginaActual());
    configurarLogout();
    configurarMenuMovil();

});

/**
 * Actualiza la visibilidad de los elementos del menú basado en el rol.
 * @param {string} role - El rol del usuario actual ('administrador', 'vendedor', etc.)
 */
function actualizarVisibilidadUI(role) {
    document.body.className = document.body.className.replace(/role-\w+/g, '').trim();
    document.body.classList.add(`role-${role}`);
}

/**
 * Verifica si el rol actual tiene permiso para ver la página actual.
 * @param {string} role - El rol del usuario actual.
 * @param {string} page - El nombre del archivo de la página actual.
 */
function verificarAccesoPorRol(role, page) {
    const permisos = {
        'administrador': [
            'administracion_de_usuarios.html',
            'reporte_ventas.html',
            'gestion_de_productos.html',
            'proceso_ventas.html',
            'dashboard.html',
            'lista_de_productos.html',
            'detallle_de_producto.html'
        ],
        'vendedor': [
            'gestion_de_productos.html',
            'proceso_ventas.html',
            'dashboard.html',
            'lista_de_productos.html',
            'detallle_de_producto.html'
        ],
        'cliente': [
            'historial_ordenes.html',
            'carrito.html',
            'dashboard.html',
            'lista_de_productos.html',
            'detallle_de_producto.html'
        ],
        'invitado': [
            'login.html',
            'registro_de_cliente.html',
            'dashboard.html',
            'index.html',
            '',
            'lista_de_productos.html',
            'detallle_de_producto.html'
        ]
    };

    const paginasPermitidas = permisos[role] || [];
    if (!paginasPermitidas.includes(page)) {
        alert('No tienes permisos para acceder a esta página. Serás redirigido.');
        window.location.href = 'dashboard.html';
    }
}

/**
 * Configura el enlace de "Cerrar Sesión".
 */
function configurarLogout() {
    const logoutLinkElement = document.querySelector('.nav-logout-link a');
    if (logoutLinkElement) {
        logoutLinkElement.addEventListener('click', (e) => {
            e.preventDefault();
            localStorage.clear();
            window.location.href = 'login.html';
        });
    }
}

/**
 * Configura el botón del menú hamburguesa para móviles.
 */
function configurarMenuMovil() {
    const mobileMenuButton = document.querySelector('.mobile-menu-toggle');
    const mainNav = document.querySelector('nav');
    if (mobileMenuButton && mainNav) {
        mobileMenuButton.addEventListener('click', () => {
            mainNav.classList.toggle('active');
        });
    }
}

/**
 * Obtiene el nombre del archivo de la página actual.
 * @returns {string}
 */
function paginaActual() {
    return (window.location.pathname.split('/').pop() || 'index.html').trim();
} 