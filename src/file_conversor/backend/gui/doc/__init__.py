# src/file_conversor/backend/gui/doc/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui.doc._index import doc_index

from file_conversor.backend.gui.doc.convert import doc_convert


def routes():
    return [
        FlaskRoute(
            rule="/doc",
            handler=doc_index
        ),
        FlaskRoute(
            rule="/doc/convert",
            handler=doc_convert
        ),
    ]


__all__ = [
    'doc_index',
    'doc_convert',

    'routes',
]
