// src\file_conversor\.web\static\js\status_bar.js

/* global Alpine  */

import { alpineConfigModal } from "./modal.js";

export function alpineConfigStatusBar() {
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
            console.log("Starting status bar:", this, " - ID:", this.status_id);
            await this.update();
        },
        updateTime() {
            if (typeof this.time !== 'number') {
                this.time = 0;
            } else {
                this.time++;
            }
        },
        updateStatusMessage(data) {
            switch (data.status) {
                case 'ready':
                    this.message = 'Ready ...';
                    break;
                case 'processing':
                    this.message = 'Processing ...';
                    break;
                case 'completed':
                    this.message = 'Completed';
                    break;
                case 'failed':
                    this.message = 'Error';
                    throw new Error(data.exception || 'Unknown failure');
                case 'unknown':
                    this.message = 'Unknown';
                    throw new Error(data.exception || 'Unknown status id');
                default:
                    break;
            }
        },
        updateProgress(progress) {
            this.progress = progress;

            const progressBar = this.getProgressBarEl();
            if (this.progress && this.progress >= 0) {
                progressBar.value = this.progress;
            } else {
                progressBar.removeAttribute('value');
            }
        },
        async update() {
            try {
                const url = `/api/status?id=${this.status_id}`;
                const method = 'GET';
                const response = await fetch(url, { method });
                /* Expects a JSON response with at least:
                {
                    "status": <string>, // "processing", "completed", "failed"
                    "progress": <int>, // 0-100
                    "message": <string>,
                    "exception": <string> (optional)
                }
                */

                if (!response.ok) {
                    throw new Error(`${response.statusText} (${response.status}): ${url} (${method})`);
                }

                const data = await response.json();
                this.updateTime();
                this.updateProgress(data.progress);
                this.updateStatusMessage(data);

                if (data.status !== 'completed') {
                    setTimeout(() => this.update(), 1000);
                } else {
                    if (data.message) {
                        alpineConfigModal().load({
                            title: "Operation completed",
                            body: `${data.message || 'The operation has completed successfully.'}`,
                        });
                    }
                    this.success = true;
                    this.finished = true;
                }

            } catch (err) {
                this.failed = true;
                this.finished = true;
                console.error('Status update failed:', err);

                if (err.message.includes('Failed to fetch')) {
                    alpineConfigModal().load({
                        title: "Lost connection",
                        body: 'Lost connection to the server. Please check your internet connection and try again.',
                        closeable: false,
                    });
                } else {
                    alpineConfigModal().load({
                        title: "Operation failed",
                        body: `${err.message}`,
                    });
                }
            }
        },
    });
    return Alpine.store('status_bar');
}