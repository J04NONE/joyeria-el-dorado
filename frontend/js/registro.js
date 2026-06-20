// frontend/js/registro.js

document.addEventListener('DOMContentLoaded', () => {
    const registerForm = document.getElementById('register-form');

    if (registerForm) {
        registerForm.addEventListener('submit', (e) => {
            e.preventDefault(); // Prevenir el envío real del formulario

            // Obtener todos los valores del formulario
            const nombre = document.getElementById('nombre').value;
            const apellido = document.getElementById('apellido').value;
            const email = document.getElementById('email').value;
            const direccion = document.getElementById('direccion').value;
            const telefono = document.getElementById('telefono').value;
            const password = document.getElementById('password').value;
            const terms = document.getElementById('terms').checked;

            // Validaciones básicas
            if (!nombre || !apellido || !email || !password) {
                alert('Por favor, completa todos los campos obligatorios.');
                return;
            }

            if (password.length < 8) {
                alert('La contraseña debe tener al menos 8 caracteres.');
                return;
            }

            if (!terms) {
                alert('Debes aceptar los Términos y Condiciones para continuar.');
                return;
            }

            // Validación básica de email
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(email)) {
                alert('Por favor, ingresa un correo electrónico válido.');
                return;
            }

            // Simular proceso de registro exitoso
            alert('¡Cuenta creada exitosamente! Redirigiendo al login...');
            
            // Limpiar el formulario
            registerForm.reset();
            
            // Redirigir al login
            setTimeout(() => {
                window.location.href = 'login.html';
            }, 1000);
        });
    }

    // Validación en tiempo real para la contraseña
    const passwordInput = document.getElementById('password');
    if (passwordInput) {
        passwordInput.addEventListener('input', () => {
            const password = passwordInput.value;
            const minLength = 8;
            
            if (password.length > 0 && password.length < minLength) {
                passwordInput.style.borderColor = '#dc3545';
                passwordInput.title = `La contraseña debe tener al menos ${minLength} caracteres`;
            } else if (password.length >= minLength) {
                passwordInput.style.borderColor = '#28a745';
                passwordInput.title = 'Contraseña válida';
            } else {
                passwordInput.style.borderColor = '';
                passwordInput.title = '';
            }
        });
    }

    // Validación en tiempo real para el email
    const emailInput = document.getElementById('email');
    if (emailInput) {
        emailInput.addEventListener('input', () => {
            const email = emailInput.value;
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            
            if (email.length > 0 && !emailRegex.test(email)) {
                emailInput.style.borderColor = '#dc3545';
                emailInput.title = 'Por favor, ingresa un correo electrónico válido';
            } else if (email.length > 0 && emailRegex.test(email)) {
                emailInput.style.borderColor = '#28a745';
                emailInput.title = 'Correo electrónico válido';
            } else {
                emailInput.style.borderColor = '';
                emailInput.title = '';
            }
        });
    }
}); 