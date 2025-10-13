# src/file_conversor/backend/gui/_api/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui._api.shutdown import api_shutdown


def routes():
    return [
        FlaskRoute(
            rule="/api/shutdown",
            handler=api_shutdown,
        ),
    ]


__all__ = ['routes']
