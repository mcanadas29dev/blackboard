// Inyectar CSRF token en todas las peticiones fetch POST
const csrfMeta = document.querySelector('meta[name="csrf-token"]');


document.addEventListener('DOMContentLoaded', () => {
    // Auto-ocultar flash messages después de 4s
    document.querySelectorAll('.flash').forEach(el => {
        setTimeout(() => {
            el.style.transition = 'opacity .5s';
            el.style.opacity = '0';
            setTimeout(() => el.remove(), 500);
        }, 4000);
    });
});
