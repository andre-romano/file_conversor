// src\file_conversor\.web\static\js\alpine\__init__.js

import { alpineConfigDragDrop } from "./drag_drop.js";
import { alpineConfigForm } from "./form.js";
import { alpineConfigModal } from "./modal.js";
import { alpineConfigStatusBar } from "./status_bar.js";

export default function alpineStoreConfig() {
    alpineConfigDragDrop();
    alpineConfigForm();
    alpineConfigModal();
    alpineConfigStatusBar();
}
