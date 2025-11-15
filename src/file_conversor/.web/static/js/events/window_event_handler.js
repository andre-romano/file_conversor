// src\file_conversor\.web\static\js\events\window_event_handler.js

import { AbstractEventHandler } from "./abstract_event_handler.js";

class WindowEventHandler extends AbstractEventHandler {
    constructor() {
        super(window);
    }
}

export default new WindowEventHandler();