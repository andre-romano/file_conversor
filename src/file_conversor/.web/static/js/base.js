// src\file_conversor\.web\static\js\base.js

/* eslint-disable no-unused-vars */
/* global Alpine  */

function set_zoom(zoom_level) {
    zoom_level = parseInt(zoom_level);
    document.body.style.zoom = `${zoom_level}%`;
    console.log('Set zoom level to:', zoom_level);
}

document.addEventListener('DOMContentLoaded', () => {
    if (window.dom_ready) return;
    window.dom_ready = true;

    console.log('DOMContentLoaded event fired');
});

document.addEventListener('alpine:init', () => {
    if (window.alpine_ready) return;
    window.alpine_ready = true;

    console.log('Alpine initialized');
});

window.addEventListener('pywebviewready', async () => {
    if (window.pywebview_ready) return;
    window.pywebview_ready = true;

    console.log('pywebview JS API is ready');

    // fix window title to reflect <title> tag
    const title = document.title;
    await window.pywebview.api.set_title({ title: title });
    console.log('Set window title:', title);
});
