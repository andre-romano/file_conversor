# src/file_conversor/backend/gui/doc/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui.doc.index import doc_index

routes = [
    FlaskRoute(
        rule="/doc",
        handler=doc_index
    )
]

__all__ = ['routes']
