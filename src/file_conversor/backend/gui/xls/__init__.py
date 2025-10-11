# src/file_conversor/backend/gui/xls/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui.xls.index import xls_index

routes = [
    FlaskRoute(
        rule="/xls",
        handler=xls_index
    )
]

__all__ = ['routes']
