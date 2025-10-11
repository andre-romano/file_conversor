# src/file_conversor/backend/gui/hash/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui.hash.index import hash_index

routes = [
    FlaskRoute(
        rule="/hash",
        handler=hash_index
    )
]

__all__ = ['routes']
