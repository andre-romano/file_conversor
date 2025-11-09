// src\file_conversor\.web\static\js\form.js

/* global Alpine, alpineConfigModal, alpineConfigStatusBar */

function alpineConfigForm() {
    let formStore = (Alpine.store('form'));

    if (formStore) return formStore;

    Alpine.store('form', {
        async submit(form, api_endpoint) {
            try {
                const method = 'POST';
                const body = new FormData(form);
                // Ensure unchecked checkboxes are sent as 'off'
                document.querySelectorAll('input[type="checkbox"]').forEach((input) => {
                    if (!body.has(input.name)) {
                        body.append(input.name, 'off');
                    }
                });
                const response = await fetch(api_endpoint, { method, body });
                /* Expects a JSON response with at least:
                {
                    "status_id": <int>,
                    "message": <string>,
                    "exception": <string> (optional)
                }
                */
                let data = {};
                try {
                    data = await response.json();
                } catch (err) {
                    console.warn("Submit - JSON parse error:", err);
                }
                console.log("Submit - Parsed data:", data);
                if (!response.ok) {
                    throw new Error(data.message || `${response.statusText} (${response.status}): ${api_endpoint} (${method})`);
                }
                let status_bar = alpineConfigStatusBar();
                await status_bar.start(data.id);
            } catch (error) {
                await alpineConfigModal().load({
                    title: 'Form Submit Error',
                    body: `${error.message}`,
                });
            }
        },
    });

    return Alpine.store('form');
}

document.addEventListener('alpine:init', () => {
    if (window.alpine_form_ready) return;
    window.alpine_form_ready = true;

    alpineConfigForm();
});
