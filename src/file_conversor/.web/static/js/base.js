// src\file_conversor\.web\static\js\index.js

function configNavbar() {
    // Get all "navbar-burger" elements
    const burgers = Array.from(document.querySelectorAll('.navbar-burger'));

    burgers.forEach(el => {
        el.addEventListener('click', () => {
            const target = el.dataset.target;
            const menu = document.getElementById(target);

            // Toggle "is-active" class on both the "navbar-burger" and the "navbar-menu"
            el.classList.toggle('is-active');
            menu.classList.toggle('is-active');
        });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    configNavbar();
});