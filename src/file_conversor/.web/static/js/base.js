// src\file_conversor\.web\static\js\index.js

/* global Alpine */

async function loadModal(title, msg, closeable = true) {
    try {
        const response = await fetch(`/api/component/modal?title=${title}&msg=${msg}&closeable=${closeable}`, {
            method: 'GET',
        });
        if (!response.ok) {
            throw new Error(`${response.status} ${response.statusText}`);
        }
        const data = await response.text();
        document.body.insertAdjacentHTML('beforeend', data);
    } catch (error) {
        console.error('Error loading modal:', error);
    }
}

function alpineConfigStatusBar() {
    let status_bar = Alpine.store('status_bar');

    if (status_bar) return status_bar;

    Alpine.store('status_bar', {
        // state flags
        started: false,
        finished: false,

        // state completion flags
        success: false,
        failed: false,

        // status info
        message: null,
        progress: null,
        time: null,

        // backend status identifier
        status_id: 0,

        getProgressBarEl() {
            return document.querySelector('.status-progress-bar');
        },
        async start(status_id) {
            this.started = true;
            this.finished = false;

            this.success = false;
            this.failed = false;

            this.time = 0;

            this.status_id = status_id;
            await this.update();
        },
        async update() {
            try {
                // console.log('Progress:', this.progress);
                if (typeof this.time !== 'number') {
                    this.time = 0;
                } else {
                    this.time++;
                }

                const response = await fetch(`/api/status?status_id=${this.status_id}`, {
                    method: 'GET',
                });
                /* Expects a JSON response with at least:
                {
                    "status": <string>, // "processing", "completed", "failed"
                    "progress": <int>, // 0-100
                    "message": <string>,
                    "exception": <string> (optional)
                }
                */

                if (!response.ok) {
                    throw new Error(`${response.status} ${response.statusText}`);
                }

                const data = await response.json();
                this.message = data.message;
                this.progress = data.progress;

                const progressBar = this.getProgressBarEl();
                if (this.progress && this.progress >= 0) {
                    progressBar.value = this.progress;
                } else {
                    progressBar.removeAttribute('value');
                }

                if (data.status === 'failed') {
                    throw new Error(data.exception || 'Unknown failure');
                }

                if (data.status !== 'completed') {
                    setTimeout(() => this.update(), 1000);
                } else {
                    this.success = true;
                    this.finished = true;
                }

            } catch (err) {
                this.failed = true;
                this.finished = true;
                console.error('Status update failed:', err);

                if (err.message.includes('Failed to fetch')) {
                    await loadModal(
                        "Lost connection",
                        'Lost connection to the server. Please check your internet connection and try again.',
                        false,
                    );
                } else {
                    await loadModal(
                        "Operation failed",
                        `An error occurred during the operation:<br><pre>${err.message}</pre>`,
                        true,
                    );
                }
            }
        },
    });
    return Alpine.store('status_bar');
}

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
                    await loadModal(
                        `${response.statusText}`,
                        `${data.exception || 'Unknown error'}: ${data.message || ''}`,
                        true,
                    );
                    return;
                }
                let status_bar = alpineConfigStatusBar();
                await status_bar.start(data.status_id);
            } catch (error) {
                await loadModal(
                    'Error',
                    `An error occurred: ${error.message}`,
                    true,
                );
            }
        },
    });

    return Alpine.store('form');
}

function alpineFileDialogConfig() {
    let fileDialogStore = (Alpine.store('file_dialog'));

    if (fileDialogStore) return fileDialogStore;

    Alpine.store('file_dialog', {
        openFolderDialog() {
            // TODO Logic to open the folder dialog
            console.log('Open folder dialog request');
        },
        openFileDialog(extensions = [], multiple = false) {
            // TODO Logic to open the file dialog
            console.log('Open file dialog request');
            console.log('Extensions:', extensions);
            console.log('Multiple:', multiple);
        },
    });

    return Alpine.store('file_dialog');
}

document.addEventListener('DOMContentLoaded', () => {
    console.log('DOMContentLoaded event fired');
});

document.addEventListener('alpine:init', () => {
    console.log('Alpine initialized');
    alpineConfigStatusBar();
    alpineConfigForm();
    alpineFileDialogConfig();
});
