# src/file_conversor/backend/gui/_api/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui._api.config import api_config
from file_conversor.backend.gui._api.status import api_status

# sub APIs
from file_conversor.backend.gui._api._component import routes as component_api_routes

from file_conversor.backend.gui._api.audio import routes as audio_api_routes
from file_conversor.backend.gui._api.doc import routes as doc_api_routes
from file_conversor.backend.gui._api.ppt import routes as ppt_api_routes
from file_conversor.backend.gui._api.xls import routes as xls_api_routes


def routes():
    return [
        # general APIs
        FlaskRoute(
            rule="/api/config",
            handler=api_config,
            methods=["GET", "POST"]
        ),
        FlaskRoute(
            rule="/api/status",
            handler=api_status,
        ),
        *component_api_routes(),

        # plugin APIs
        *audio_api_routes(),
        *doc_api_routes(),
        *ppt_api_routes(),
        *xls_api_routes(),
    ]


__all__ = ['routes']
