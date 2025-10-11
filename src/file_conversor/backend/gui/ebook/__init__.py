# src/file_conversor/backend/gui/ebook/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui.ebook.index import ebook_index

routes = [
    FlaskRoute(
        rule="/ebook",
        handler=ebook_index
    )
]

__all__ = ['routes']
