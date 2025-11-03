// src\file_conversor\.web\static\js\form.js

/* global Alpine, alpineConfigModal, alpineConfigStatusBar */

function alpineConfigForm() {
    let formStore = (Alpine.store('form'));

    if (formStore) return formStore;

    Alpine.store('form', {
        async submit(form, api_endpoint) {
            try {
                const response = await fetch(api_endpoint, {
                    method: 'POST',
                    body: new FormData(form),
                });
                /* Expects a JSON response with at least:
                {
                    "status_id": <int>,
                    "message": <string>,
                    "exception": <string> (optional)
                }
                */
                const data = await response.json();
                if (!response.ok) {
                    await alpineConfigModal().load(
                        `${response.statusText}`,
                        `${data.exception || 'Unknown error'}: ${data.message || ''}`,
                        '',
                        true,
                    );
                    return;
                }
                let status_bar = alpineConfigStatusBar();
                await status_bar.start(data.status_id);
            } catch (error) {
                await alpineConfigModal().load(
                    'Error',
                    `An error occurred: ${error.message}`,
                    '',
                    true,
                );
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
