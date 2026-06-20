/*
 * Archivo: catalogo.js
 * Propósito: Maneja la carga y renderización dinámica de productos en la página del catálogo (`lista_de_productos.html`)
 * conectándose a la API de Django.
 * Última Modificación: Julio 2025 - Conexión inicial con API de productos.
 */

document.addEventListener('DOMContentLoaded', () => {
    cargarYRenderizarProductos();
});

/**
 * @async
 * @function cargarYRenderizarProductos
 * @description Obtiene la lista de productos de la API de inventario y los muestra dinámicamente en la página del catálogo.
 * Muestra mensajes de carga, éxito o error.
 */
async function cargarYRenderizarProductos() {
    const grid = document.getElementById('producto-grid');
    if (!grid) {
        console.error("Error: Contenedor #producto-grid no encontrado en lista_de_productos.html");
        return;
    }
    grid.innerHTML = '<p class="mensaje-carga">Cargando joyas de nuestro catálogo...</p>';
    try {
        const url = `${API_BASE_URL}/api/inventario/productos/`;
        console.log(`Intentando cargar productos desde: ${url}`);
        const response = await fetch(url);
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Error HTTP: ${response.status} - ${errorText}`);
        }
        const productos = await response.json();
        console.log("Productos recibidos de la API:", productos);
        grid.innerHTML = '';
        if (!Array.isArray(productos) || productos.length === 0) {
            grid.innerHTML = '<p class="mensaje-info">No hay productos disponibles en este momento. ¡Vuelve pronto!</p>';
            return;
        }
        productos.forEach(producto => {
            const productoCardHTML = crearTarjetaProducto(producto);
            grid.insertAdjacentHTML('beforeend', productoCardHTML);
        });
    } catch (error) {
        console.error("Error al cargar y renderizar productos:", error);
        grid.innerHTML = '<p class="mensaje-error">No se pudieron cargar los productos. Por favor, intente recargar la página más tarde.</p>';
    }
}

/**
 * @function crearTarjetaProducto
 * @description Crea el código HTML para una sola tarjeta de producto, utilizando los datos de un producto.
 * @param {object} producto - Un objeto que representa un producto (ej. {id, nombre, precio, imagen_url, descripcion}).
 * @returns {string} - La cadena de texto HTML para la tarjeta del producto.
 */
function crearTarjetaProducto(producto) {
    const precioFormateado = parseFloat(producto.precio).toLocaleString('es-CO', {
        style: 'currency',
        currency: 'COP',
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    });
    // Usar la imagen del backend si existe, si no un placeholder
    const imagenUrl = producto.imagen ? `${API_BASE_URL}${producto.imagen}` : '../assets/placeholder_joya.png';
    return `
        <div class="producto">
            <img src="${imagenUrl}" alt="${producto.nombre || 'Producto sin nombre'}">
            <div class="producto-info">
                <h4 class="producto-titulo">${producto.nombre || 'Nombre no disponible'}</h4>
                <div class="producto-precio">${precioFormateado}</div>
                <p class="producto-descripcion">${(producto.descripcion && producto.descripcion.substring(0, 80) + '...') || 'Sin descripción.'}</p>
                <div class="producto-acciones">
                    <a href="detalle_de_producto.html?id=${producto.id}" class="btn-producto btn-ver-detalle">Ver Detalle</a>
                    <button class="btn-producto btn-agregar-carrito" data-id="${producto.id}"
                            data-nombre="${producto.nombre}"
                            data-precio="${producto.precio}"
                            data-imagen="${imagenUrl}">Agregar al Carrito</button>
                </div>
            </div>
        </div>
    `;
}

// Funcionalidad de filtros
const aplicarFiltrosBtn = document.getElementById('apply-filters-btn');
if (aplicarFiltrosBtn) {
    aplicarFiltrosBtn.addEventListener('click', () => {
        const categoria = document.getElementById('category-filter').value;
        const material = document.getElementById('material-filter').value;
        const precio = document.getElementById('price-filter').value;
        const orden = document.getElementById('sort-filter').value;
        
        console.log('Filtros aplicados:', {
            categoria,
            material,
            precio,
            orden
        });
        
        // Aquí se implementaría la lógica de filtrado
        // Por ahora solo mostramos un mensaje
        alert('Filtros aplicados correctamente. La funcionalidad de filtrado real se implementará más adelante.');
    });
}

// Funcionalidad de agregar al carrito con muro de login
const addToCartButtons = document.querySelectorAll('.btn-agregar-carrito, .add-to-cart-btn');
addToCartButtons.forEach(button => {
    button.addEventListener('click', function(event) {
        event.preventDefault(); // Prevenir cualquier acción por defecto del enlace o botón

        const userRole = localStorage.getItem('userRole') || 'invitado'; // Obtener el rol actual

        if (userRole === 'invitado') {
            // Si es un invitado, alertar y redirigir
            alert('Por favor, inicia sesión o crea una cuenta para añadir productos al carrito.');
            window.location.href = 'login.html'; // Redirigir a la página de login
        } else if (userRole === 'cliente') {
            // Lógica para AÑADIR AL CARRITO (Rol Cliente)
            // Debes asegurarte de que el botón o su padre contenga los datos del producto
            const productCard = button.closest('.producto'); // Ajusta según tu estructura HTML
            if (productCard) {
                const producto = {
                    id: productCard.dataset.id || `prod-${Math.random().toString(36).substr(2, 9)}`, // Asegúrate de que el producto tenga un ID único, quizás en un data-attribute
                    nombre: productCard.querySelector('.producto-titulo').textContent,
                    precio: parseFloat(productCard.querySelector('.producto-precio').textContent.replace('$', '').replace('.', '').replace(',', '.')), // Limpiar el precio y convertir a número
                    imagen: productCard.querySelector('img').src,
                    cantidad: 1 // Por defecto, se añade 1 unidad
                };
                agregarAlCarrito(producto); // Llamada a la función global de carrito
                
                button.textContent = 'Añadido ✔';
                button.classList.add('added');
                setTimeout(() => {
                    button.textContent = 'Agregar al Carrito';
                    button.classList.remove('added');
                }, 2000);
            } else {
                console.error("No se pudo encontrar la información del producto para añadir al carrito.");
            }
        } else {
            // Si el rol es vendedor o admin, quizás un mensaje diferente o simplemente no se permite
            alert('Solo los clientes pueden añadir productos al carrito. Usa "Procesar Venta" para crear pedidos.');
        }
    });
}); 