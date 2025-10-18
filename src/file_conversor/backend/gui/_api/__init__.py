# src/file_conversor/backend/gui/_api/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui._api.shutdown import api_shutdown
from file_conversor.backend.gui._api.config import api_config


def routes():
    return [
        FlaskRoute(
            rule="/api/shutdown",
            handler=api_shutdown,
        ),
        FlaskRoute(
            rule="/api/config",
            handler=api_config,
            methods=["GET", "POST"]
        ),
    ]


__all__ = ['routes']
