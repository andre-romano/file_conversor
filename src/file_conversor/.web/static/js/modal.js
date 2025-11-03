// src\file_conversor\.web\static\js\modal.js

/* global Alpine */

function alpineConfigModal() {
    let modal = Alpine.store('modal');

    if (modal) return modal;

    Alpine.store('modal', {
        // modal state
        title: '',
        body: '',
        footer: '',
        show: false,
        closeable: true,
        load(opts) {
            console.log(opts);
            // placeholder for any loading logic if needed
            this.title = opts.title || '';
            this.body = opts.body || '';
            this.footer = opts.footer || '';
            this.closeable = opts.closeable !== undefined ? opts.closeable : true;
            this.show = true;
        }
    });
    return Alpine.store('modal');
}

document.addEventListener('alpine:init', () => {
    if (window.alpine_modal_ready) return;
    window.alpine_modal_ready = true;

    alpineConfigModal();
});