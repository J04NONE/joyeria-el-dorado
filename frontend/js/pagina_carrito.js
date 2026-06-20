// frontend/js/pagina_carrito.js

document.addEventListener('DOMContentLoaded', () => {
    const itemsContainer = document.getElementById('cart-items-container');
    const summaryContainer = document.getElementById('cart-summary');

    /**
     * Renderiza el contenido del carrito en la página, incluyendo la tabla de productos y el resumen.
     */
    function renderizarPaginaCarrito() {
        const carrito = getCarrito(); // Función getCarrito viene de js/carrito.js

        if (carrito.length === 0) {
            itemsContainer.innerHTML = `
                <h3>Tu carrito está vacío.</h3>
                <p>¡Añade algunas joyas para verlas aquí!</p>
            `;
            if (summaryContainer) { // Asegurarse de que el summaryContainer exista
                summaryContainer.style.display = 'none'; // Ocultar resumen si no hay items
            }
            return;
        }
        
        // Mostrar el resumen si hay items
        if (summaryContainer) {
            summaryContainer.style.display = 'block';
        }
        itemsContainer.innerHTML = ''; // Limpiar el contenedor antes de re-renderizar
        
        const table = document.createElement('table');
        table.className = 'cart-items-table';
        table.innerHTML = `
            <thead>
                <tr>
                    <th>Producto</th>
                    <th>Precio</th>
                    <th>Cantidad</th>
                    <th>Subtotal</th>
                    <th></th>
                </tr>
            </thead>
        `;
        const tbody = document.createElement('tbody');
        let subtotalGeneral = 0;

        carrito.forEach(item => {
            const itemSubtotal = item.precio * item.cantidad;
            subtotalGeneral += itemSubtotal;

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>
                    <div class="product-info-cell">
                        <img src="${item.imagen}" alt="${item.nombre}">
                        <div>
                            <strong>${item.nombre}</strong>
                        </div>
                    </div>
                </td>
                <td>$${item.precio.toLocaleString('es-CO')} COP</td>
                <td>
                    <div class="quantity-control">
                        <button class="quantity-decrease" data-id="${item.id}">-</button>
                        <input type="text" value="${item.cantidad}" readonly>
                        <button class="quantity-increase" data-id="${item.id}">+</button>
                    </div>
                </td>
                <td>$${itemSubtotal.toLocaleString('es-CO')} COP</td>
                <td><button class="btn-icon-danger remove-item" data-id="${item.id}" aria-label="Eliminar producto"><i class="fas fa-trash-alt"></i></button></td>
            `;
            tbody.appendChild(tr);
        });

        table.appendChild(tbody);
        itemsContainer.appendChild(table);

        // Renderizar el resumen de la compra
        if (summaryContainer) {
            summaryContainer.innerHTML = `
                <h2>Resumen de la Compra</h2>
                <div class="summary-line">
                    <span>Subtotal:</span>
                    <span id="summary-subtotal">$${subtotalGeneral.toLocaleString('es-CO')} COP</span>
                </div>
                <div class="summary-line">
                    <span>Envío:</span>
                    <span>Gratis</span>
                </div>
                <hr>
                <div class="summary-total">
                    <span>Total:</span>
                    <span id="summary-total">$${subtotalGeneral.toLocaleString('es-CO')} COP</span>
                </div>
                <button class="btn btn-primary btn-full-width">Proceder al Pago</button>
            `;
        }

        // Añadir Event Listeners para los botones de cantidad y eliminar
        document.querySelectorAll('.quantity-increase').forEach(btn => btn.addEventListener('click', e => cambiarCantidad(e.target.dataset.id, 1)));
        document.querySelectorAll('.quantity-decrease').forEach(btn => btn.addEventListener('click', e => cambiarCantidad(e.target.dataset.id, -1)));
        document.querySelectorAll('.remove-item').forEach(btn => btn.addEventListener('click', e => {
            // Confirmación opcional: if (confirm('¿Estás seguro de eliminar este producto?')) { ... }
            eliminarDelCarrito(e.target.dataset.id); // Función de js/carrito.js
            renderizarPaginaCarrito(); // Re-renderizar después de la eliminación
        }));
    }

    /**
     * Maneja el cambio de cantidad de un producto en el carrito.
     * @param {string} productoId - ID del producto.
     * @param {number} cambio - Cantidad a añadir o restar (-1 o 1).
     */
    function cambiarCantidad(productoId, cambio) {
        const carrito = getCarrito();
        const item = carrito.find(p => p.id === productoId);
        if (item) {
            actualizarCantidad(productoId, item.cantidad + cambio); // Función de js/carrito.js
            renderizarPaginaCarrito(); // Re-renderizar después del cambio
        }
    }

    // Llamar a la función de renderizado al cargar la página
    renderizarPaginaCarrito();
}); 