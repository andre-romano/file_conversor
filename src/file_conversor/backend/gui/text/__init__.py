# src/file_conversor/backend/gui/text/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui.text.index import text_index

routes = [
    FlaskRoute(
        rule="/text",
        handler=text_index
    )
]

__all__ = ['routes']
