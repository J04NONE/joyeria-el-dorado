document.addEventListener('DOMContentLoaded', () => {
    // Funcionalidad de galería de imágenes
    const mainImage = document.getElementById('mainImage');
    const thumbnails = document.querySelectorAll('.thumbnail');
    
    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', () => {
            // Remover clase active de todos los thumbnails
            thumbnails.forEach(t => t.classList.remove('active'));
            // Agregar clase active al thumbnail clickeado
            thumbnail.classList.add('active');
            // Cambiar imagen principal
            mainImage.src = thumbnail.dataset.image;
        });
    });

    // Funcionalidad de zoom
    const zoomBtn = document.querySelector('.zoom-btn');
    if (zoomBtn) {
        zoomBtn.addEventListener('click', () => {
            // Aquí se implementaría la funcionalidad de zoom
            alert('Funcionalidad de zoom en desarrollo');
        });
    }

    // Funcionalidad de selector de cantidad
    const qtyMinus = document.getElementById('qty-minus');
    const qtyPlus = document.getElementById('qty-plus');
    const quantityInput = document.getElementById('quantity');

    if (qtyMinus && qtyPlus && quantityInput) {
        qtyMinus.addEventListener('click', () => {
            const currentValue = parseInt(quantityInput.value);
            if (currentValue > 1) {
                quantityInput.value = currentValue - 1;
            }
        });

        qtyPlus.addEventListener('click', () => {
            const currentValue = parseInt(quantityInput.value);
            if (currentValue < 5) {
                quantityInput.value = currentValue + 1;
            }
        });
    }

    // Funcionalidad de botones de acción con muro de login
    const addToCartBtn = document.getElementById('add-to-cart');
    const buyNowBtn = document.getElementById('buy-now');

    function checkAuthAndExecute(action) {
        const userRole = localStorage.getItem('userRole') || 'invitado';
        
        if (userRole === 'invitado') {
            alert('Por favor, inicia sesión o crea una cuenta para continuar.');
            window.location.href = 'login.html';
            return false;
        }
        
        return true;
    }

    if (addToCartBtn) {
        addToCartBtn.addEventListener('click', (event) => {
            event.preventDefault();
            
            const userRole = localStorage.getItem('userRole') || 'invitado';

            if (userRole === 'invitado') {
                alert('Por favor, inicia sesión o crea una cuenta para añadir productos al carrito.');
                window.location.href = 'login.html';
            } else if (userRole === 'cliente') {
                // Recopilar información del producto de la página de detalle
                const producto = {
                    id: document.getElementById('product-id') ? document.getElementById('product-id').value : `prod-${Math.random().toString(36).substr(2, 9)}`,
                    nombre: document.querySelector('.product-header h1').textContent,
                    precio: parseFloat(document.querySelector('.current-price').textContent.replace('$', '').replace('.', '').replace(',', '.')),
                    imagen: document.getElementById('mainImage').src,
                    cantidad: parseInt(quantityInput.value) || 1
                };
                agregarAlCarrito(producto); // Llamada a la función global de carrito

                addToCartBtn.innerHTML = '<span class="btn-icon">✅</span> Añadido al Carrito';
                addToCartBtn.classList.add('added');
                setTimeout(() => {
                    addToCartBtn.innerHTML = '<span class="btn-icon">🛒</span> Agregar al Carrito';
                    addToCartBtn.classList.remove('added');
                }, 2000);
            } else {
                alert('Solo los clientes pueden añadir productos al carrito.');
            }
        });
    }

    if (buyNowBtn) {
        buyNowBtn.addEventListener('click', (event) => {
            event.preventDefault();
            
            if (checkAuthAndExecute('buy-now')) {
                const quantity = quantityInput ? quantityInput.value : 1;
                alert(`Redirigiendo al proceso de compra (Cantidad: ${quantity})`);
                // Aquí se redirigiría al proceso de compra
                // window.location.href = 'proceso_compra.html';
            }
        });
    }

    // Funcionalidad para botones de agregar al carrito en productos relacionados
    const relatedAddToCartButtons = document.querySelectorAll('.producto .btn-agregar-carrito');
    relatedAddToCartButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();
            
            const userRole = localStorage.getItem('userRole') || 'invitado';

            if (userRole === 'invitado') {
                alert('Por favor, inicia sesión o crea una cuenta para añadir productos al carrito.');
                window.location.href = 'login.html';
            } else if (userRole === 'cliente') {
                const productCard = button.closest('.producto');
                if (productCard) {
                    const producto = {
                        id: productCard.dataset.id || `prod-${Math.random().toString(36).substr(2, 9)}`,
                        nombre: productCard.querySelector('.producto-titulo').textContent,
                        precio: parseFloat(productCard.querySelector('.producto-precio').textContent.replace('$', '').replace('.', '').replace(',', '.')),
                        imagen: productCard.querySelector('img').src,
                        cantidad: 1
                    };
                    agregarAlCarrito(producto); // Llamada a la función global de carrito
                    
                    button.textContent = 'Añadido ✔';
                    button.classList.add('added');
                    setTimeout(() => {
                        button.textContent = 'Agregar';
                        button.classList.remove('added');
                    }, 2000);
                } else {
                    console.error("No se pudo encontrar la información del producto para añadir al carrito.");
                }
            } else {
                alert('Solo los clientes pueden añadir productos al carrito.');
            }
        });
    });
}); 