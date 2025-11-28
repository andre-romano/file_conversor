# src/file_conversor/backend/gui/ebook/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui.ebook._index import ebook_index

from file_conversor.backend.gui.ebook.convert import ebook_convert


def routes():
    return [
        FlaskRoute(
            rule="/ebook",
            handler=ebook_index
        ),
        FlaskRoute(
            rule="/ebook/convert",
            handler=ebook_convert
        ),
    ]


__all__ = [
    'ebook_index',
    'ebook_convert',

    'routes',
]
