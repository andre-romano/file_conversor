# src/file_conversor/backend/gui/ppt/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui.ppt.index import ppt_index


routes = [
    FlaskRoute(
        rule="/ppt",
        handler=ppt_index
    )
]

__all__ = ['routes']
