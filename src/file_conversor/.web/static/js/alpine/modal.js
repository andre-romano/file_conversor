// src\file_conversor\.web\static\js\modal.js

/* global Alpine */

export function alpineConfigModal() {
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
            this.footer = opts.footer || `
                <div class="buttons is-right is-full-width">
                    <button class="button is-primary" 
                            :class="{ 'is-hidden': !$store.modal.closeable }"        
                            @click="$store.modal.show = false" 
                            >
                        Close
                    </button>
                </div>        
            `;
            this.closeable = opts.closeable !== undefined ? opts.closeable : true;
            this.show = true;
        },
        init() {
            const thisObj = this;
            // Close modal on ESC key press
            document.addEventListener("keydown", (event) => {
                if (event.key === "Escape") {
                    thisObj.show = thisObj.closeable ? false : thisObj.show;
                }
            });
        }
    });
    return Alpine.store('modal');
}