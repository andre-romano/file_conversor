// src\file_conversor\.web\static\js\base.js

/* global Alpine  */

import alpineStoreConfig from "./alpine/__init__.js";

import { windowEventHandler, documentEventHandler } from "./events/__init__.js";

// Expose event handlers globally
window.windowEventHandler = windowEventHandler;
window.documentEventHandler = documentEventHandler;

export function set_zoom(zoom_level) {
    zoom_level = parseInt(zoom_level);
    document.body.style.zoom = `${zoom_level}%`;
    console.log('Set zoom level to:', zoom_level);
}

documentEventHandler.on('alpine:init', () => {
    alpineStoreConfig();
    console.log('Alpine stores configured');
});

windowEventHandler.on('pywebviewready', async () => {
    // fix window title to reflect <title> tag
    const title = document.title;
    await window.pywebview.api.set_title({ title: title });
    console.log('Set window title:', title);
    // set window icon
    await window.pywebview.api.set_icon();
    console.log('Set window icon');
});

windowEventHandler.on('beforeunload', async () => {
    setTimeout(() => {
        try {
            const modal = Alpine.store('modal');
            modal.load({
                title: 'Loading ...',
                body: 'The application is loading next page. Please wait ...',
                footer: `
                <div class="is-flex is-justify-content-flex-end is-full-width">
                <button class="button is-success is-loading" disabled>Loading...</button>
                </div>
                `,
                closeable: false,
            });
            document.body.classList.add('is-cursor-wait');
        } catch (e) {
            console.log("No modal available:", e);
        }
    }, 150);
});
