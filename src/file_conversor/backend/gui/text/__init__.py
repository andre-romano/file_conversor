# src/file_conversor/backend/gui/text/__init__.py

from file_conversor.backend.gui.flask_route import FlaskRoute

from file_conversor.backend.gui.text._index import text_index

from file_conversor.backend.gui.text.check import text_check
from file_conversor.backend.gui.text.compress import text_compress
from file_conversor.backend.gui.text.convert import text_convert


def routes():
    return [
        FlaskRoute(
            rule="/text",
            handler=text_index,
        ),
        FlaskRoute(
            rule="/text/check",
            handler=text_check,
        ),
        FlaskRoute(
            rule="/text/compress",
            handler=text_compress,
        ),
        FlaskRoute(
            rule="/text/convert",
            handler=text_convert,
        ),
    ]


__all__ = [
    'text_index',
    'text_check',
    'text_compress',
    'text_convert',

    'routes',
]
