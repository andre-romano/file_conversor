// src\file_conversor\.web\static\js\alpine\drag_drop.js

/* global Alpine */

export function alpineConfigDragDrop() {
    let dragDropStore = Alpine.store('drag_drop');

    if (dragDropStore) return dragDropStore;

    Alpine.store('drag_drop', {
        files: [],

        init() {
            window.addEventListener('filesDropped', async (event) => {
                console.log('Files dropped:', event.detail.files);
                this.files = event.detail.files;
                // alpine next tick to ensure DOM is updated
                await Alpine.nextTick();
            });
        }
    });

    return Alpine.store('drag_drop');
}