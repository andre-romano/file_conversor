# src/file_conversor/backend/gui/_api/component/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

# operation APIs
from file_conversor.backend.gui._api.component.modal import api_component_modal


def routes():
    return [
        FlaskRoute(
            rule="/api/component/modal",
            handler=api_component_modal,
        ),
    ]


__all__ = ['routes']
