// src\file_conversor\.web\static\js\events\document_event_handler.js

import { AbstractEventHandler } from "./abstract_event_handler.js";

class DocumentEventHandler extends AbstractEventHandler {
    constructor() {
        super(document);
    }
}

export default new DocumentEventHandler();