# src/file_conversor/backend/gui/_api/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui._api.config import api_config
from file_conversor.backend.gui._api.shutdown import api_shutdown
from file_conversor.backend.gui._api.status import api_status

# operation APIs
from file_conversor.backend.gui._api.doc import routes as doc_api_routes


def routes():
    return [
        FlaskRoute(
            rule="/api/config",
            handler=api_config,
            methods=["GET", "POST"]
        ),
        FlaskRoute(
            rule="/api/shutdown",
            handler=api_shutdown,
        ),
        FlaskRoute(
            rule="/api/status",
            handler=api_status,
        ),
        # operation APIs
        *doc_api_routes(),
    ]


__all__ = ['routes']
