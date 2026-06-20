// frontend/js/carrito.js

// --- Funciones de Bajo Nivel (interactúan directamente con localStorage) ---
function getCarrito() {
    try {
        const carritoJSON = localStorage.getItem('carrito');
        return carritoJSON ? JSON.parse(carritoJSON) : [];
    } catch (e) {
        console.error("Error al leer el carrito de localStorage:", e);
        return [];
    }
}

function guardarCarrito(carrito) {
    try {
        localStorage.setItem('carrito', JSON.stringify(carrito));
        actualizarIndicadorCarrito(); // Siempre actualiza el ícono al guardar
    } catch (e) {
        console.error("Error al guardar el carrito en localStorage:", e);
    }
}

// --- Funciones de Alto Nivel (Lógica de Negocio del Carrito) ---

/**
 * Agrega un producto al carrito. Solo permite a clientes agregar.
 * @param {object} producto - Objeto del producto con id, nombre, precio, imagen, cantidad.
 */
function agregarAlCarrito(producto) {
    // Solo los clientes autenticados (con la clase 'role-cliente' en el body) pueden agregar al carrito.
    if (document.body.classList.contains('role-cliente')) {
        let carrito = getCarrito();
        const itemExistente = carrito.find(item => item.id === producto.id);

        if (itemExistente) {
            itemExistente.cantidad += producto.cantidad;
        } else {
            carrito.push(producto);
        }
        guardarCarrito(carrito);
        alert(`"${producto.nombre}" ha sido añadido al carrito.`);
    } else {
        alert('Por favor, inicia sesión como cliente para añadir productos al carrito.');
        // Opcional: Redirigir al login si se intenta añadir como no-cliente
        // window.location.href = 'login.html';
    }
}

/**
 * Actualiza la cantidad de un producto específico en el carrito.
 * @param {string} productoId - ID del producto a actualizar.
 * @param {number} nuevaCantidad - Nueva cantidad para el producto.
 */
function actualizarCantidad(productoId, nuevaCantidad) {
    let carrito = getCarrito();
    const itemIndex = carrito.findIndex(item => item.id === productoId);

    if (itemIndex > -1) {
        if (nuevaCantidad > 0) {
            carrito[itemIndex].cantidad = nuevaCantidad;
        } else {
            // Si la cantidad es 0 o menos, elimina el item del carrito
            carrito.splice(itemIndex, 1);
        }
        guardarCarrito(carrito);
    }
}

/**
 * Elimina un producto del carrito.
 * @param {string} productoId - ID del producto a eliminar.
 */
function eliminarDelCarrito(productoId) {
    let carrito = getCarrito().filter(item => item.id !== productoId);
    guardarCarrito(carrito);
}

/**
 * Vacía completamente el carrito de compras.
 */
function limpiarCarrito() {
    localStorage.removeItem('carrito');
    guardarCarrito([]); // Llama a guardar para asegurar que el indicador se actualice a 0
}

// --- Funciones de UI ---

/**
 * Actualiza el contador de items en el icono del carrito en el header.
 * Solo muestra el indicador si el usuario es un cliente.
 */
function actualizarIndicadorCarrito() {
    const cartCountSpan = document.querySelector('.cart-count');
    
    // El indicador solo se muestra si el body tiene la clase 'role-cliente'
    if (!document.body.classList.contains('role-cliente')) {
        if (cartCountSpan) {
            cartCountSpan.classList.remove('visible'); // Asegurarse de que esté oculto
        }
        return; // Salir si no es cliente
    }

    const carrito = getCarrito();
    const totalItems = carrito.reduce((sum, item) => sum + item.cantidad, 0);

    if (cartCountSpan) {
        if (totalItems > 0) {
            cartCountSpan.textContent = totalItems;
            cartCountSpan.classList.add('visible');
        } else {
            cartCountSpan.classList.remove('visible');
        }
    }
}

// Inicializar el indicador del carrito al cargar cualquier página
document.addEventListener('DOMContentLoaded', actualizarIndicadorCarrito); 