# src/file_conversor/backend/gui/config/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui.config.index import config_index

routes = [
    FlaskRoute(
        rule="/config",
        handler=config_index
    )
]

__all__ = ['routes']
