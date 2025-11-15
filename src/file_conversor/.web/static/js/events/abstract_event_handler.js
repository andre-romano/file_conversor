// src\file_conversor\.web\static\js\events\abstract_event_handler.js

export class AbstractEventHandler {
    constructor(targetObject) {
        this._callbacks = {};
        this._executed_events = {};
        this._listeners_added = {};
        this._targetObject = targetObject;
    }

    on(event_name, callback) {
        if (!this._callbacks[event_name]) {
            this._callbacks[event_name] = [];
        }
        this._callbacks[event_name].push(callback);
        if (this._executed_events[event_name]) {
            this._run(event_name);
        }
        if (!this._listeners_added[event_name]) {
            this._addListener(event_name);
        }
    }

    _addListener(event_name) {
        this._targetObject.addEventListener(event_name, () => {
            console.log(`Window event '${event_name}' fired`);
            this._run(event_name);
        });
        this._listeners_added[event_name] = true;
    }

    _run(event_name) {
        if (!this._callbacks[event_name]) {
            this._callbacks[event_name] = [];
        }

        for (const callback of this._callbacks[event_name]) {
            try {
                callback();
            } catch (e) {
                console.error(`Error running callback for event '${event_name}':`, e);
            }
        }

        this._callbacks[event_name] = [];
        this._executed_events[event_name] = true;
    }
}
